#include "TestCommand.h"
#include "http_test_helpers.h"

#include "cli/commands/Common.h"
#include "cli/commands/Ensure.h"

#include <catch2/catch_test_macros.hpp>
#include <nlohmann/json.hpp>

#include <chrono>
#include <filesystem>
#include <fstream>
#include <optional>
#include <sstream>
#include <string>
#include <thread>
#include <vector>

#ifndef _WIN32
#include <csignal>
#include <sys/types.h>
#include <unistd.h>
#endif

namespace {

using holder::cli::ApiRange;
using holder::cli::check_api_compatibility;
using holder::cli::compare_api_versions;
using holder::cli::parse_api_version;

std::vector<unsigned long> version(const std::string& text) {
  const auto parsed = parse_api_version(text);
  REQUIRE(parsed.has_value());
  return *parsed;
}

} // namespace

TEST_CASE("ensure parses dotted API versions", "[ensure]") {
  REQUIRE(parse_api_version("0.1") == std::optional<std::vector<unsigned long>>({0, 1}));
  REQUIRE(parse_api_version("1") == std::optional<std::vector<unsigned long>>({1}));
  REQUIRE(parse_api_version("12.0.345") == std::optional<std::vector<unsigned long>>({12, 0, 345}));

  for (const char* bad : {"", ".", "1.", ".1", "1..2", "a", "1.x", "1.2-rc.1", "v1", " 1", "1 ", "-1", "1234567890"}) {
    INFO("input: '" << bad << "'");
    REQUIRE_FALSE(parse_api_version(bad).has_value());
  }
}

TEST_CASE("ensure compares API versions numerically", "[ensure]") {
  REQUIRE(compare_api_versions(version("0.9"), version("0.10")) < 0);
  REQUIRE(compare_api_versions(version("0.10"), version("0.9")) > 0);
  REQUIRE(compare_api_versions(version("1"), version("1.0")) == 0);
  REQUIRE(compare_api_versions(version("1.0.0"), version("1")) == 0);
  REQUIRE(compare_api_versions(version("1.0.1"), version("1")) > 0);
  REQUIRE(compare_api_versions(version("2"), version("10")) < 0);
}

TEST_CASE("ensure checks the supported API range", "[ensure]") {
  SECTION("no bounds accepts anything, even an unknown version") {
    REQUIRE(check_api_compatibility("0.1", ApiRange{}).compatible);
    REQUIRE(check_api_compatibility("", ApiRange{}).compatible);
    REQUIRE(check_api_compatibility("not-a-version", ApiRange{}).compatible);
  }

  SECTION("the minimum is inclusive") {
    const ApiRange range{"0.2", ""};
    REQUIRE_FALSE(check_api_compatibility("0.1", range).compatible);
    REQUIRE(check_api_compatibility("0.2", range).compatible);
    REQUIRE(check_api_compatibility("1.0", range).compatible);
  }

  SECTION("the maximum is exclusive") {
    const ApiRange range{"", "1.0"};
    REQUIRE(check_api_compatibility("0.9", range).compatible);
    REQUIRE_FALSE(check_api_compatibility("1.0", range).compatible);
    REQUIRE_FALSE(check_api_compatibility("1.1", range).compatible);
  }

  SECTION("both bounds together") {
    const ApiRange range{"0.1", "0.3"};
    REQUIRE_FALSE(check_api_compatibility("0.0", range).compatible);
    REQUIRE(check_api_compatibility("0.1", range).compatible);
    REQUIRE(check_api_compatibility("0.2", range).compatible);
    REQUIRE_FALSE(check_api_compatibility("0.3", range).compatible);
  }

  SECTION("an unusable version is rejected only when a bound applies") {
    const ApiRange range{"0.1", ""};
    const auto missing = check_api_compatibility("", range);
    REQUIRE_FALSE(missing.compatible);
    REQUIRE(missing.reason.find("did not report") != std::string::npos);
    const auto garbled = check_api_compatibility("dev-build", range);
    REQUIRE_FALSE(garbled.compatible);
    REQUIRE(garbled.reason.find("dev-build") != std::string::npos);
  }

  SECTION("the reason names the offending and the required version") {
    const auto result = check_api_compatibility("0.1", ApiRange{"0.2", ""});
    REQUIRE(result.reason.find("0.1") != std::string::npos);
    REQUIRE(result.reason.find("0.2") != std::string::npos);
  }
}

namespace {

holder::cli::EnsureOptions parse(std::vector<std::string> args) {
  std::vector<std::string> storage = {"holderctl", "ensure"};
  storage.insert(storage.end(), args.begin(), args.end());
  std::vector<char*> argv;
  for (auto& item : storage) argv.push_back(item.data());
  return holder::cli::parse_ensure_options(static_cast<int>(argv.size()), argv.data());
}

int usage_exit_code(std::vector<std::string> args) {
  try {
    parse(std::move(args));
  } catch (const holder::cli::CliError& error) {
    return error.exit_code();
  }
  return -1;
}

} // namespace

TEST_CASE("ensure parses its options", "[ensure]") {
  SECTION("defaults") {
    const auto options = parse({});
    REQUIRE(options.allow_start);
    REQUIRE(options.mode == holder::cli::EnsureMode::Auto);
    REQUIRE(options.timeout == std::chrono::milliseconds(60000));
    REQUIRE(options.api.minimum.empty());
    REQUIRE(options.api.maximum_exclusive.empty());
    REQUIRE(options.daemon_args.empty());
  }

  SECTION("every option, in both spellings") {
    const auto options = parse({
        "--json",
        "--api-min", "0.1",
        "--api-max-exclusive=2",
        "--no-start",
        "--timeout", "2.5",
        "--mode=spawn",
        "--daemon", "/opt/holder/bin/holderd",
        "--daemon-arg", "--port",
        "--daemon-arg=0",
        "--workdir", "/opt/holder/share/holder-daemon",
    });
    REQUIRE_FALSE(options.allow_start);
    REQUIRE(options.api.minimum == "0.1");
    REQUIRE(options.api.maximum_exclusive == "2");
    REQUIRE(options.timeout == std::chrono::milliseconds(2500));
    REQUIRE(options.mode == holder::cli::EnsureMode::Spawn);
    REQUIRE(options.daemon_path == std::filesystem::path("/opt/holder/bin/holderd"));
    REQUIRE(options.daemon_args == std::vector<std::string>({"--port", "0"}));
    REQUIRE(options.working_dir == std::filesystem::path("/opt/holder/share/holder-daemon"));
  }

  SECTION("invalid options are usage errors with exit code 2") {
    REQUIRE(usage_exit_code({"--bogus"}) == holder::cli::kEnsureExitUsage);
    REQUIRE(usage_exit_code({"--api-min"}) == holder::cli::kEnsureExitUsage);
    REQUIRE(usage_exit_code({"--api-min", "one"}) == holder::cli::kEnsureExitUsage);
    REQUIRE(usage_exit_code({"--api-max-exclusive", "1."}) == holder::cli::kEnsureExitUsage);
    REQUIRE(usage_exit_code({"--timeout", "0"}) == holder::cli::kEnsureExitUsage);
    REQUIRE(usage_exit_code({"--timeout", "-3"}) == holder::cli::kEnsureExitUsage);
    REQUIRE(usage_exit_code({"--timeout", "soon"}) == holder::cli::kEnsureExitUsage);
    REQUIRE(usage_exit_code({"--timeout", "99999"}) == holder::cli::kEnsureExitUsage);
    REQUIRE(usage_exit_code({"--mode", "magic"}) == holder::cli::kEnsureExitUsage);
    REQUIRE(usage_exit_code({"--daemon"}) == holder::cli::kEnsureExitUsage);
  }
}

TEST_CASE("ensure renders the documented JSON shape", "[ensure]") {
  holder::cli::EnsureResult started;
  started.ok = true;
  started.state = "started";
  started.mode = "spawned";
  started.daemon = {{"pid", 42}, {"url", "http://127.0.0.1:1"}, {"api_version", "0.1"}, {"server_version", "0.2.1"}};
  started.spawned_pid = 42;
  started.log_path = "/tmp/holderd-start.log";
  started.elapsed_ms = 120;

  const auto ok_json = holder::cli::ensure_result_to_json(started);
  REQUIRE(ok_json["ok"] == true);
  REQUIRE(ok_json["state"] == "started");
  REQUIRE(ok_json["started"] == true);
  REQUIRE(ok_json["mode"] == "spawned");
  REQUIRE(ok_json["exit_code"] == 0);
  REQUIRE(ok_json["spawned_pid"] == 42);
  REQUIRE(ok_json["daemon"]["api_version"] == "0.1");
  REQUIRE(ok_json["log"] == "/tmp/holderd-start.log");
  REQUIRE_FALSE(ok_json.contains("error"));

  holder::cli::EnsureResult failed;
  failed.state = "failed";
  failed.exit_code = holder::cli::kEnsureExitTimeout;
  failed.error_code = "timeout";
  failed.message = "slow";

  const auto failed_json = holder::cli::ensure_result_to_json(failed);
  REQUIRE(failed_json["ok"] == false);
  REQUIRE(failed_json["started"] == false);
  REQUIRE(failed_json["exit_code"] == 13);
  REQUIRE(failed_json["error"]["code"] == "timeout");
  REQUIRE(failed_json["error"]["message"] == "slow");
  REQUIRE_FALSE(failed_json.contains("daemon"));
  REQUIRE_FALSE(failed_json.contains("mode"));
  REQUIRE_FALSE(failed_json.contains("spawned_pid"));
}

#ifndef _WIN32

namespace {

struct CtlRun {
  int exit_code = -1;
  nlohmann::json json;
  std::string stderr_text;
};

bool process_alive(long long pid) { return pid > 0 && ::kill(static_cast<pid_t>(pid), 0) == 0; }

void stop_process(long long pid) {
  if (!process_alive(pid)) return;
  ::kill(static_cast<pid_t>(pid), SIGTERM);
  for (int i = 0; i < 100 && process_alive(pid); ++i) {
    std::this_thread::sleep_for(std::chrono::milliseconds(50));
  }
  if (process_alive(pid)) ::kill(static_cast<pid_t>(pid), SIGKILL);
}

std::string read_file(const std::filesystem::path& path) {
  std::ifstream in(path);
  std::ostringstream text;
  text << in.rdbuf();
  return text.str();
}

// A private home, so a test never sees (or starts) the developer's real daemon. Any
// daemon or stand-in process a test leaves behind is stopped when the scope ends.
class IsolatedHome {
 public:
  IsolatedHome()
      : root_(holder::test::make_temp_dir()),
        home_("HOME", (root_ / "home").string()),
        data_("XDG_DATA_HOME", (root_ / "data").string()),
        config_("XDG_CONFIG_HOME", (root_ / "config").string()),
        cache_("XDG_CACHE_HOME", (root_ / "cache").string()),
        keystore_("HOLDER_TEST_KEYSTORE_DIR", (root_ / "keystore").string()) {
    std::filesystem::create_directories(root_ / "home");
  }
  IsolatedHome(const IsolatedHome&) = delete;
  IsolatedHome& operator=(const IsolatedHome&) = delete;

  ~IsolatedHome() {
    for (const auto pid : tracked_) stop_process(pid);
    if (const auto pid = recorded_daemon_pid()) stop_process(*pid);
    std::error_code ec;
    std::filesystem::remove_all(root_, ec);
  }

  void track(long long pid) { tracked_.push_back(pid); }

  std::filesystem::path info_path() const { return root_ / "data" / "holder" / "server" / "holder.json"; }
  std::filesystem::path start_log_path() const { return root_ / "cache" / "holder" / "holderd-start.log"; }

  std::optional<long long> recorded_daemon_pid() const {
    std::ifstream in(info_path());
    if (!in) return std::nullopt;
    try {
      const auto info = nlohmann::json::parse(in);
      return info.value("pid", 0LL);
    } catch (const std::exception&) {
      return std::nullopt;
    }
  }

  CtlRun run(const std::string& arguments) const {
    CtlRun result;
    const auto out = root_ / "stdout.txt";
    const auto err = root_ / "stderr.txt";
    const std::string command = "\"" + std::string(HOLDER_CTL_PATH) + "\" ensure --json " + arguments +
                                " > \"" + out.string() + "\" 2> \"" + err.string() + "\"";
    result.exit_code = holder::test::run_system_command(command);
    result.stderr_text = read_file(err);
    const auto text = read_file(out);
    if (!text.empty()) result.json = nlohmann::json::parse(text);
    return result;
  }

  // The real daemon on a free port, run from the source tree so it finds its resources.
  std::string daemon_arguments() const {
    const auto repo_root = std::filesystem::path(__FILE__).parent_path().parent_path();
    return "--daemon \"" + std::string(HOLDER_BIN_PATH) + "\" --workdir \"" + repo_root.string() +
           "\" --daemon-arg --port --daemon-arg 0 --timeout 60";
  }

 private:
  std::filesystem::path root_;
  holder::test::EnvGuard home_;
  holder::test::EnvGuard data_;
  holder::test::EnvGuard config_;
  holder::test::EnvGuard cache_;
  holder::test::EnvGuard keystore_;
  std::vector<long long> tracked_;
};

} // namespace

TEST_CASE("ensure reports that nothing is running with --no-start", "[ensure][process]") {
  IsolatedHome home;
  const auto run = home.run("--no-start");
  REQUIRE(run.exit_code == holder::cli::kEnsureExitNotRunning);
  REQUIRE(run.json["ok"] == false);
  REQUIRE(run.json["state"] == "failed");
  REQUIRE(run.json["error"]["code"] == "not_running");
  REQUIRE(run.json["exit_code"] == 11);
  REQUIRE_FALSE(run.json.contains("spawned_pid"));
}

TEST_CASE("ensure reports a missing holderd", "[ensure][process]") {
  IsolatedHome home;
  const auto run = home.run("--daemon \"" + (std::filesystem::temp_directory_path() / "no-such-holderd").string() + "\"");
  REQUIRE(run.exit_code == holder::cli::kEnsureExitDaemonNotFound);
  REQUIRE(run.json["error"]["code"] == "daemon_not_found");
}

TEST_CASE("ensure notices a daemon that exits before becoming healthy", "[ensure][process]") {
  IsolatedHome home;
  // holderctl itself stands in for a daemon that stops at once.
  const auto started = std::chrono::steady_clock::now();
  const auto run = home.run("--daemon \"" + std::string(HOLDER_CTL_PATH) + "\" --daemon-arg version --timeout 30");
  const auto elapsed = std::chrono::steady_clock::now() - started;
  REQUIRE(run.exit_code == holder::cli::kEnsureExitStartFailed);
  REQUIRE(run.json["error"]["code"] == "start_failed");
  REQUIRE(run.json["error"]["message"].get<std::string>().find("exited") != std::string::npos);
  REQUIRE(elapsed < std::chrono::seconds(20));
}

TEST_CASE("ensure times out on a daemon that never becomes healthy", "[ensure][process]") {
  IsolatedHome home;
  // A long sleep stands in for a daemon that starts but never serves.
  const auto run = home.run("--daemon /bin/sleep --daemon-arg 30 --timeout 1");
  REQUIRE(run.json.contains("spawned_pid"));
  home.track(run.json["spawned_pid"].get<long long>());
  REQUIRE(run.exit_code == holder::cli::kEnsureExitTimeout);
  REQUIRE(run.json["error"]["code"] == "timeout");
  // ensure leaves the process alone; the caller decides what to do with spawned_pid.
  REQUIRE(process_alive(run.json["spawned_pid"].get<long long>()));
}

TEST_CASE("ensure starts a detached daemon, reuses it, and enforces the API range", "[ensure][process]") {
  IsolatedHome home;

  const auto first = home.run(home.daemon_arguments());
  REQUIRE(first.exit_code == 0);
  REQUIRE(first.json["ok"] == true);
  REQUIRE(first.json["state"] == "started");
  REQUIRE(first.json["mode"] == "spawned");
  const auto pid = first.json["daemon"]["pid"].get<long long>();
  REQUIRE(pid > 0);
  REQUIRE(first.json["spawned_pid"].get<long long>() == pid);
  REQUIRE(first.json["daemon"]["url"].get<std::string>().rfind("http://127.0.0.1:", 0) == 0);
  REQUIRE_FALSE(first.json["daemon"]["api_version"].get<std::string>().empty());
  REQUIRE(std::filesystem::exists(home.start_log_path()));

  // It outlived holderctl, and it has its own session and process group.
  REQUIRE(process_alive(pid));
  REQUIRE(::getsid(static_cast<pid_t>(pid)) == static_cast<pid_t>(pid));
  REQUIRE(::getpgid(static_cast<pid_t>(pid)) == static_cast<pid_t>(pid));

  const std::string api = first.json["daemon"]["api_version"].get<std::string>();

  SECTION("a second call finds the running daemon and does not start another") {
    const auto again = home.run("");
    REQUIRE(again.exit_code == 0);
    REQUIRE(again.json["state"] == "running");
    REQUIRE(again.json["mode"] == "existing");
    REQUIRE(again.json["daemon"]["pid"].get<long long>() == pid);
    REQUIRE_FALSE(again.json.contains("spawned_pid"));
  }

  SECTION("a supported range is accepted") {
    const auto in_range = home.run("--api-min 0 --api-max-exclusive 1000");
    REQUIRE(in_range.exit_code == 0);
    REQUIRE(in_range.json["state"] == "running");
  }

  SECTION("an unsupported range is refused and the daemon is left running") {
    const auto too_new = home.run("--api-min 999");
    REQUIRE(too_new.exit_code == holder::cli::kEnsureExitApiIncompatible);
    REQUIRE(too_new.json["error"]["code"] == "api_incompatible");
    REQUIRE(too_new.json["daemon"]["api_version"] == api);
    REQUIRE(process_alive(pid));

    const auto too_old = home.run("--api-max-exclusive 0.0");
    REQUIRE(too_old.exit_code == holder::cli::kEnsureExitApiIncompatible);
  }

  SECTION("--no-start sees the running daemon") {
    const auto check = home.run("--no-start");
    REQUIRE(check.exit_code == 0);
    REQUIRE(check.json["state"] == "running");
  }
}

TEST_CASE("ensure copes with a stale info file from a daemon that has gone", "[ensure][process]") {
  IsolatedHome home;
  const auto first = home.run(home.daemon_arguments());
  REQUIRE(first.exit_code == 0);
  const auto pid = first.json["daemon"]["pid"].get<long long>();

  // Kill it without letting it tidy up, leaving its info file behind.
  ::kill(static_cast<pid_t>(pid), SIGKILL);
  for (int i = 0; i < 100 && process_alive(pid); ++i) {
    std::this_thread::sleep_for(std::chrono::milliseconds(50));
  }
  REQUIRE(std::filesystem::exists(home.info_path()));

  const auto check = home.run("--no-start");
  REQUIRE(check.exit_code == holder::cli::kEnsureExitNotRunning);

  const auto restarted = home.run(home.daemon_arguments());
  REQUIRE(restarted.exit_code == 0);
  REQUIRE(restarted.json["state"] == "started");
  REQUIRE(restarted.json["daemon"]["pid"].get<long long>() != pid);
}

#endif
