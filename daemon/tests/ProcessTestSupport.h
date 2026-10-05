#pragma once

// Support for tests that start the real holderd and holderctl as separate processes. POSIX
// only: the tests that use it are compiled out on Windows.
#ifndef _WIN32

#include "TestCommand.h"
#include "http_test_helpers.h"

#include <nlohmann/json.hpp>

#include <csignal>
#include <sys/types.h>
#include <unistd.h>

#include <chrono>
#include <filesystem>
#include <fstream>
#include <optional>
#include <sstream>
#include <string>
#include <thread>
#include <vector>

namespace holder::test {

struct CtlRun {
  int exit_code = -1;
  nlohmann::json json;
  std::string stdout_text;
  std::string stderr_text;
};

struct DaemonInfo {
  long long pid = 0;
  std::string bind;
  unsigned short port = 0;
  std::string token;
};

inline bool process_alive(long long pid) {
  return pid > 0 && ::kill(static_cast<pid_t>(pid), 0) == 0;
}

inline void stop_process(long long pid) {
  if (!process_alive(pid)) return;
  ::kill(static_cast<pid_t>(pid), SIGTERM);
  for (int i = 0; i < 100 && process_alive(pid); ++i) {
    std::this_thread::sleep_for(std::chrono::milliseconds(50));
  }
  if (process_alive(pid)) ::kill(static_cast<pid_t>(pid), SIGKILL);
}

inline std::string read_file(const std::filesystem::path& path) {
  std::ifstream in(path);
  std::ostringstream text;
  text << in.rdbuf();
  return text.str();
}

// Waits for a condition, polling, and returns whether it became true in time.
template <typename Condition>
bool wait_until(std::chrono::milliseconds limit, Condition condition) {
  const auto deadline = std::chrono::steady_clock::now() + limit;
  while (std::chrono::steady_clock::now() < deadline) {
    if (condition()) return true;
    std::this_thread::sleep_for(std::chrono::milliseconds(50));
  }
  return condition();
}

// A private home, so a test never sees (or starts) the developer's real daemon. Any daemon or
// stand-in process a test leaves behind is stopped when the scope ends.
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
    for (const auto pid : tracked_)
      stop_process(pid);
    if (const auto info = daemon_info()) stop_process(info->pid);
    std::error_code ec;
    std::filesystem::remove_all(root_, ec);
  }

  void track(long long pid) { tracked_.push_back(pid); }

  const std::filesystem::path& root() const { return root_; }
  // The daemon source directory, where holderd finds its schema and configuration.
  static std::filesystem::path source_root() {
    return std::filesystem::path(__FILE__).parent_path().parent_path();
  }
  std::filesystem::path info_path() const {
    return root_ / "data" / "holder" / "server" / "holder.json";
  }
  std::filesystem::path start_log_path() const {
    return root_ / "cache" / "holder" / "holderd-start.log";
  }

  std::optional<DaemonInfo> daemon_info() const {
    std::ifstream in(info_path());
    if (!in) return std::nullopt;
    try {
      const auto json = nlohmann::json::parse(in);
      DaemonInfo info;
      info.pid = json.value("pid", 0LL);
      info.bind = json.value("bind", std::string("127.0.0.1"));
      info.port = static_cast<unsigned short>(json.value("port", 0));
      info.token = json.value("auth_token", std::string());
      if (info.pid <= 0 || info.port == 0) return std::nullopt;
      return info;
    } catch (const std::exception&) {
      return std::nullopt;
    }
  }

  std::optional<DaemonInfo> wait_for_daemon_info(std::chrono::milliseconds limit) const {
    std::optional<DaemonInfo> info;
    wait_until(limit, [&]() {
      info = daemon_info();
      return info.has_value();
    });
    return info;
  }

  // `holderctl ensure --json ARGUMENTS`.
  CtlRun run(const std::string& arguments) const { return run_ctl("ensure", arguments, true); }

  // `holderctl SUBCOMMAND [--json] ARGUMENTS`. With json, standard output is parsed.
  CtlRun run_ctl(const std::string& subcommand, const std::string& arguments, bool json = true)
      const {
    CtlRun result;
    const auto out = root_ / "stdout.txt";
    const auto err = root_ / "stderr.txt";
    const std::string command = "\"" + std::string(HOLDER_CTL_PATH) + "\" " + subcommand +
                                (json ? " --json " : " ") + arguments + " > \"" + out.string() +
                                "\" 2> \"" + err.string() + "\"";
    result.exit_code = holder::test::run_system_command(command);
    result.stderr_text = read_file(err);
    result.stdout_text = read_file(out);
    if (json && !result.stdout_text.empty())
      result.json = nlohmann::json::parse(result.stdout_text);
    return result;
  }

  // The real daemon on a free port, run from the source tree so it finds its resources.
  std::string daemon_arguments() const {
    return "--daemon \"" + std::string(HOLDER_BIN_PATH) + "\" --workdir \"" +
           source_root().string() + "\" --daemon-arg --port --daemon-arg 0 --timeout 60";
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

} // namespace holder::test

#endif
