#pragma once

#include <git2.h>

#include <filesystem>

namespace holder::test {

// Creates an empty bare repository, to use as a remote that really accepts pushes.
inline void init_bare_repo(const std::filesystem::path& path) {
  git_libgit2_init();
  git_repository* repo = nullptr;
  if (git_repository_init(&repo, path.string().c_str(), 1) == 0) git_repository_free(repo);
  git_libgit2_shutdown();
}

// True when the bare repository `remote` has the branch that `local` has checked out, pointing
// at the same commit: that is, the local HEAD has been pushed.
inline bool remote_has_local_head(
    const std::filesystem::path& local,
    const std::filesystem::path& remote
) {
  git_libgit2_init();
  git_repository* local_repo = nullptr;
  git_repository* remote_repo = nullptr;
  git_reference* head = nullptr;
  bool pushed = false;
  if (git_repository_open(&local_repo, local.string().c_str()) == 0 &&
      git_repository_open(&remote_repo, remote.string().c_str()) == 0 &&
      git_repository_head(&head, local_repo) == 0) {
    git_oid remote_oid;
    if (git_reference_name_to_id(&remote_oid, remote_repo, git_reference_name(head)) == 0) {
      pushed = git_oid_equal(&remote_oid, git_reference_target(head)) != 0;
    }
  }
  if (head != nullptr) git_reference_free(head);
  if (remote_repo != nullptr) git_repository_free(remote_repo);
  if (local_repo != nullptr) git_repository_free(local_repo);
  git_libgit2_shutdown();
  return pushed;
}

} // namespace holder::test
