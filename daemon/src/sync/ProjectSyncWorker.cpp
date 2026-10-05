#include "sync/ProjectSyncWorker.h"
#include "core/ActivityTracker.h"

#include "git/GitOps.h"
#include "git/RepoSyncMetrics.h"
#include "index/FtsIndexer.h"
#include "platform/Db.h"
#include "project/ProjectRepo.h"
#include "project/ProjectSyncRepo.h"
#include "sync/ProjectSyncOperation.h"
#include "sync/ProjectSyncPolicy.h"

#include <git2.h>
#include <spdlog/spdlog.h>

#include <atomic>
#include <chrono>
#include <exception>
#include <thread>

namespace holder::sync {
namespace {

std::atomic<bool> g_fail_post_pull_metrics_for_tests{false};
std::atomic<bool> g_fail_post_push_metrics_for_tests{false};

holder::project::ProjectSyncActivityUpdate activity_update_from_metrics(
    const holder::git::RepoSyncMetrics& metrics,
    long long now
) {
  return {
      .uncommitted_changes_count = metrics.uncommitted_changes_count,
      .unpushed_commits_count = metrics.unpushed_commits_count,
      .updated_at = now
  };
}

// True when the repository's current branch has a remote-tracking ref for `remote`. Without one
// the unpushed-commit count is unknown rather than zero, so a final push cannot rely on it.
bool has_remote_tracking_ref(const std::filesystem::path& repo_dir, const std::string& remote) {
  git_libgit2_init();
  bool found = false;
  git_repository* repo = nullptr;
  git_reference* head = nullptr;
  git_reference* tracking = nullptr;
  if (git_repository_open(&repo, repo_dir.string().c_str()) == 0 &&
      git_repository_head(&head, repo) == 0) {
    const char* branch = nullptr;
    if (git_branch_name(&branch, head) == 0 && branch != nullptr) {
      const std::string name = "refs/remotes/" + remote + "/" + branch;
      found = git_reference_lookup(&tracking, repo, name.c_str()) == 0;
    }
  }
  if (tracking != nullptr) git_reference_free(tracking);
  if (head != nullptr) git_reference_free(head);
  if (repo != nullptr) git_repository_free(repo);
  git_libgit2_shutdown();
  return found;
}

} // namespace

ProjectSyncWorker::ProjectSyncWorker(
    std::filesystem::path db_path,
    ProjectSyncWorkerIntervals intervals
)
    : db_path_(std::move(db_path)),
      push_interval_seconds_(intervals.push_interval_seconds),
      pull_interval_seconds_(intervals.pull_interval_seconds),
      poll_interval_seconds_(intervals.poll_interval_seconds) {}

void ProjectSyncWorker::run(const holder::core::SignalHandler& signals) {
  {
    // Syncing is work: a daemon started with --idle-exit must not stop in the middle of it.
    const auto activity_scope = holder::core::activity().begin();
    try {
      run_startup_pull_pass();
    } catch (const std::exception& ex) {
      spdlog::warn("sync worker startup pull pass failed: {}", ex.what());
    }
  }

  while (!signals.is_requested()) {
    {
      const auto activity_scope = holder::core::activity().begin();
      try {
        run_push_cycle();
      } catch (const std::exception& ex) {
        spdlog::warn("sync worker push cycle failed: {}", ex.what());
      }
    }

    int slept = 0;
    while (!signals.is_requested() && slept < poll_interval_seconds_) {
      std::this_thread::sleep_for(std::chrono::seconds(1));
      slept += 1;
    }
  }
}

void ProjectSyncWorker::set_fail_post_pull_metrics_for_tests(bool enabled) {
  g_fail_post_pull_metrics_for_tests.store(enabled, std::memory_order_relaxed);
}

void ProjectSyncWorker::set_fail_post_push_metrics_for_tests(bool enabled) {
  g_fail_post_push_metrics_for_tests.store(enabled, std::memory_order_relaxed);
}

long long ProjectSyncWorker::now_epoch_seconds() const {
  return std::chrono::duration_cast<std::chrono::seconds>(
             std::chrono::system_clock::now().time_since_epoch()
  )
      .count();
}

void ProjectSyncWorker::run_startup_pull_pass() {
  holder::platform::Db db;
  db.open(db_path_);
  holder::index::FtsIndexer fts(db);
  holder::project::ProjectRepo projects(db);
  holder::project::ProjectSyncRepo sync(db);
  holder::git::RealGitOps git;

  const auto now = now_epoch_seconds();
  for (const auto& project : projects.list()) {
    if (!project.git_remote_url.has_value() || project.git_remote_url->empty()) {
      continue;
    }
    {
      auto operation = git.lock_operation(project.root_path);
      try {
        git.open_or_init(project.root_path);
        git.set_remote("origin", project.git_remote_url.value());
        const auto metrics = holder::git::inspect_repo_sync_metrics(project.root_path, "origin");
        sync.update_activity_counts(project.project_id, activity_update_from_metrics(metrics, now));
      } catch (const std::exception& ex) {
        // LCOV_EXCL_START: exercised failure path; spdlog compiles to an uncovered inline guard.
        spdlog::warn(
            "sync worker startup metrics refresh failed for {}: {}",
            project.project_id,
            ex.what()
        );
        // LCOV_EXCL_STOP
      }
    }
    const auto current = sync.get(project.project_id);
    if (current.has_value() && current->last_pull_at.has_value()) {
      continue;
    }
    (void)holder::sync::run_project_sync(
        db,
        &fts,
        git,
        project.project_id,
        {.pull = true,
         .push = false,
         .push_after_failed_pull = false,
         .branch = "", // LCOV_EXCL_LINE: aggregate-initializer cleanup duplicate.
         .set_upstream = true,
         .now = now}
    );
    try {
      auto operation = git.lock_operation(project.root_path);
      const auto metrics = holder::git::inspect_repo_sync_metrics(project.root_path, "origin");
      sync.update_activity_counts(project.project_id, activity_update_from_metrics(metrics, now));
    } catch (const std::exception& ex) {
      // LCOV_EXCL_START: exercised failure path; spdlog compiles to an uncovered inline guard.
      spdlog::warn(
          "sync worker startup post-pull metrics refresh failed for {}: {}",
          project.project_id,
          ex.what()
      );
      // LCOV_EXCL_STOP
    }
  }
}

int ProjectSyncWorker::run_final_push() { return run_push_cycle(true); }

int ProjectSyncWorker::run_push_cycle(bool final_push) {
  int pushes_attempted = 0;
  holder::platform::Db db;
  db.open(db_path_);
  holder::index::FtsIndexer fts(db);
  holder::project::ProjectRepo projects(db);
  holder::project::ProjectSyncRepo sync(db);
  holder::git::RealGitOps git;

  const auto now = now_epoch_seconds();
  for (const auto& project : projects.list()) {
    if (!project.git_remote_url.has_value() || project.git_remote_url->empty()) {
      continue;
    }
    int unpushed_commits = 0;
    bool push_state_known = false;
    {
      auto operation = git.lock_operation(project.root_path);
      try {
        git.open_or_init(project.root_path);
        git.set_remote("origin", project.git_remote_url.value());
        const auto metrics = holder::git::inspect_repo_sync_metrics(project.root_path, "origin");
        unpushed_commits = metrics.unpushed_commits_count;
        push_state_known = final_push && has_remote_tracking_ref(project.root_path, "origin");
        sync.update_activity_counts(project.project_id, activity_update_from_metrics(metrics, now));
      } catch (const std::exception& ex) {
        // LCOV_EXCL_START: exercised failure path; spdlog compiles to an uncovered inline guard.
        spdlog::warn(
            "sync worker metrics refresh failed for {}: {}",
            project.project_id,
            ex.what()
        );
        // LCOV_EXCL_STOP
        continue;
      }
    }

    const auto state = sync.get(project.project_id);
    const bool pull_due = !final_push &&
                          should_attempt_pull( // LCOV_EXCL_LINE: aggregate initializer bookkeeping.
                              {.last_pull_at = state.has_value() ? state->last_pull_at
                                                                 : std::optional<long long>{},
                               .next_pull_retry_at = state.has_value() ? state->next_pull_retry_at
                                                                       : std::optional<long long>{},
                               .now = now,
                               .pull_interval_seconds = pull_interval_seconds_}
                          );
    // A final push ignores the interval, since the daemon is about to stop, but not the back-off
    // after a failed push. It skips a project only when the count of unpushed commits is known
    // and zero; with no remote-tracking ref the count says nothing, so the push decides.
    const bool push_due =
        (!final_push || unpushed_commits > 0 || !push_state_known) &&
        should_attempt_push( // LCOV_EXCL_LINE: aggregate initializer bookkeeping.
            {.last_push_at = state.has_value() ? state->last_push_at : std::optional<long long>{},
             .next_retry_at = state.has_value() ? state->next_retry_at : std::optional<long long>{},
             .now = now,
             .push_interval_seconds = final_push ? 0 : push_interval_seconds_}
        );
    if (!pull_due && !push_due) continue;

    if (final_push) {
      spdlog::info(
          "final push: pushing project {} before exiting ({} unpushed commit(s) known).",
          project.project_id,
          unpushed_commits
      );
    }
    if (push_due) ++pushes_attempted;

    const auto sync_result = holder::sync::run_project_sync(
        db,
        &fts,
        git,
        project.project_id,
        {.pull = pull_due,
         .push = push_due,
         .push_after_failed_pull = true,
         .branch = "", // LCOV_EXCL_LINE: aggregate-initializer cleanup duplicate.
         .set_upstream = true,
         .now = now}
    );

    if (final_push && push_due) {
      const auto status = sync_result.push.status;
      if (status == holder::git::PushStatus::Pushed ||
          status == holder::git::PushStatus::UpToDate) {
        spdlog::info("final push of project {} done.", project.project_id);
      } else {
        spdlog::warn(
            "final push of project {} did not complete ({}): {}. The commits stay local and will be pushed on the next run.",
            project.project_id,
            holder::git::push_status_name(status),
            sync_result.push.error_message.value_or("no details")
        );
      }
    }

    if (pull_due) {
      try {
        if (g_fail_post_pull_metrics_for_tests.load(std::memory_order_relaxed)) {
          throw std::runtime_error("forced post-pull metrics failure for tests");
        }
        auto operation = git.lock_operation(project.root_path);
        const auto metrics = holder::git::inspect_repo_sync_metrics(project.root_path, "origin");
        sync.update_activity_counts(project.project_id, activity_update_from_metrics(metrics, now));
      } catch (const std::exception& ex) {
        // LCOV_EXCL_START: exercised failure path; spdlog compiles to an uncovered inline guard.
        spdlog::warn(
            "sync worker post-pull metrics refresh failed for {}: {}",
            project.project_id,
            ex.what()
        );
        // LCOV_EXCL_STOP
      }
    }

    if (!push_due) continue;
    try {
      if (g_fail_post_push_metrics_for_tests.load(std::memory_order_relaxed)) {
        throw std::runtime_error("forced post-push metrics failure for tests");
      }
      auto operation = git.lock_operation(project.root_path);
      const auto metrics = holder::git::inspect_repo_sync_metrics(project.root_path, "origin");
      sync.update_activity_counts(project.project_id, activity_update_from_metrics(metrics, now));
    } catch (const std::exception& ex) {
      // LCOV_EXCL_START: exercised failure path; spdlog compiles to an uncovered inline guard.
      spdlog::warn(
          "sync worker post-push metrics refresh failed for {}: {}",
          project.project_id,
          ex.what()
      );
      // LCOV_EXCL_STOP
    }
  }
  return pushes_attempted;
}

} // namespace holder::sync
