#include "cli/commands/Ensure.h"

#include "cli/commands/Commands.h"
#include "cli/commands/Common.h"
#include "platform/DetachedProcess.h"

#include <boost/beast/http.hpp>

#include <algorithm>
#include <cctype>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <thread>
#include <utility>

namespace holder::cli {

namespace {

using Clock = std::chrono::steady_clock;

[[maybe_unused]] constexpr const char* kServiceUnit = "holder-daemon.service";

[[noreturn]] void usage_error(const std::string& message) {
  throw CliError("usage", message, nlohmann::json::object(), "", kEnsureExitUsage);
}

bool take_value(
    const std::string& arg,
    const char* name,
    int argc,
    char* argv[],
    int& index,
    std::string* value
) {
  if (arg == name) {
    if (index + 1 >= argc) usage_error(std::string("Option ") + name + " needs a value");
    *value = argv[++index];
    return true;
  }
  const std::string prefix = std::string(name) + "=";
  if (arg.rfind(prefix, 0) == 0) {
    *value = arg.substr(prefix.size());
    return true;
  }
  return false;
}

void require_api_version(const std::string& value, const char* option) {
  if (!parse_api_version(value)) {
    usage_error(std::string("Option ") + option + " needs a version such as 0.1, got '" + value + "'");
  }
}

struct Probe {
  bool healthy = false;
  std::string detail;
  int pid = 0;
  std::string url;
  std::string api_version;
  std::string server_version;
};

Probe probe_daemon(const holder::core::Paths& paths) {
  Probe probe;
  std::error_code exists_error;
  if (!std::filesystem::exists(paths.info_path(), exists_error)) {
    probe.detail = "no daemon info file at " + paths.info_path().string();
    return probe;
  }
  try {
    const auto connection = read_secure_daemon_connection(paths);
    const auto& info = connection.info.json;
    probe.pid = json_int(info, "pid");
    probe.url = "http://" + connection.bind + ":" + std::to_string(connection.port);
    probe.api_version = json_string(info, "api_version");
    probe.server_version = json_string(info, "server_version");
    if (!is_process_running(probe.pid)) {
      probe.detail = "process " + std::to_string(probe.pid) + " is not running";
      return probe;
    }
    const auto response = http_json_request(
        connection,
        boost::beast::http::verb::get,
        "/health",
        std::chrono::seconds(2)
    );
    if (response.status != boost::beast::http::status::ok) {
      probe.detail = "HTTP " + std::to_string(static_cast<unsigned>(response.status));
      return probe;
    }
    if (!response.payload.value("ok", false)) {
      probe.detail = "the daemon reported that it is not ok";
      return probe;
    }
    probe.healthy = true;
    probe.detail = "ok";
  } catch (const std::exception& ex) {
    probe.detail = ex.what();
  }
  return probe;
}

nlohmann::json daemon_json(const Probe& probe) {
  return {
      {"pid", probe.pid},
      {"url", probe.url},
      {"api_version", probe.api_version},
      {"server_version", probe.server_version},
  };
}

#if defined(__linux__)
// Runs a short program to completion and returns its exit status, or nullopt if it cannot
// be started or does not finish within the limit.
std::optional<int> run_to_completion(
    const std::filesystem::path& program,
    std::vector<std::string> args,
    std::chrono::milliseconds limit
) {
  holder::platform::DetachedProcessRequest request;
  request.executable = program;
  request.args = std::move(args);
  std::string error;
  auto process = holder::platform::DetachedProcess::start(request, &error);
  if (!process) return std::nullopt;
  const auto deadline = Clock::now() + limit;
  int code = 0;
  while (!process->has_exited(&code)) {
    if (Clock::now() >= deadline) return std::nullopt;
    std::this_thread::sleep_for(std::chrono::milliseconds(20));
  }
  return code;
}

std::filesystem::path systemctl_path() {
  return holder::platform::find_executable_on_path("systemctl");
}

bool service_unit_installed() {
  const auto systemctl = systemctl_path();
  if (systemctl.empty()) return false;
  const auto code = run_to_completion(
      systemctl,
      {"--user", "cat", kServiceUnit},
      std::chrono::seconds(5)
  );
  return code.has_value() && *code == 0;
}

bool service_unit_failed() {
  const auto systemctl = systemctl_path();
  if (systemctl.empty()) return false;
  const auto code = run_to_completion(
      systemctl,
      {"--user", "is-failed", "--quiet", kServiceUnit},
      std::chrono::seconds(5)
  );
  return code.has_value() && *code == 0;
}
#endif

// Spawn runs a holderd we find; service uses the systemd user unit. The unit is only
// chosen automatically when the caller did not name a daemon and is not running from an
// AppImage, which brings its own holderd.
EnsureMode resolve_mode(const EnsureOptions& options) {
  if (options.mode != EnsureMode::Auto) return options.mode;
  if (!options.daemon_path.empty()) return EnsureMode::Spawn;
#if defined(__linux__)
  if (std::getenv("APPDIR") != nullptr) return EnsureMode::Spawn;
  if (service_unit_installed()) return EnsureMode::Service;
#endif
  return EnsureMode::Spawn;
}

// The program is run after changing directory, so a relative path must be made absolute first.
std::filesystem::path absolute_path(const std::filesystem::path& path) {
  std::error_code ec;
  const auto absolute = std::filesystem::absolute(path, ec);
  return ec ? path : absolute;
}

std::filesystem::path locate_daemon(const EnsureOptions& options) {
  std::error_code ec;
  if (!options.daemon_path.empty()) {
    return std::filesystem::is_regular_file(options.daemon_path, ec) ? absolute_path(options.daemon_path)
                                                                       : std::filesystem::path();
  }
#ifdef _WIN32
  const char* name = "holderd.exe";
#else
  const char* name = "holderd";
#endif
  if (!options.holderctl_path.empty()) {
    const auto sibling = options.holderctl_path.parent_path() / name;
    if (std::filesystem::is_regular_file(sibling, ec)) return absolute_path(sibling);
  }
  const auto found = holder::platform::find_executable_on_path(name);
  return found.empty() ? found : absolute_path(found);
}

// Installed layouts keep the daemon's data (schema, config, docs) in ../share/holder-daemon.
// Elsewhere the daemon looks in its working directory, so start it beside its binary.
std::filesystem::path default_working_dir(const std::filesystem::path& daemon) {
  std::error_code ec;
  const auto installed = daemon.parent_path().parent_path() / "share" / "holder-daemon";
  if (std::filesystem::is_directory(installed, ec)) return installed;
  return daemon.parent_path();
}

std::string describe_seconds(std::chrono::milliseconds value) {
  const double seconds = static_cast<double>(value.count()) / 1000.0;
  std::string text = std::to_string(seconds);
  while (!text.empty() && text.back() == '0') text.pop_back();
  if (!text.empty() && text.back() == '.') text.pop_back();
  return text;
}

void print_ensure_usage(std::ostream& out) {
  out << "Usage: holderctl ensure [options]\n"
      << "\n"
      << "Make sure a compatible Holder daemon is running, starting one if needed.\n"
      << "\n"
      << "Options:\n"
      << "  --json                        Print one JSON object on standard output\n"
      << "  --api-min VERSION             Lowest daemon API version the caller supports\n"
      << "  --api-max-exclusive VERSION   First daemon API version the caller does not support\n"
      << "  --no-start                    Check only; do not start a daemon\n"
      << "  --timeout SECONDS             How long to wait for the daemon (default 60)\n"
      << "  --mode auto|service|spawn     How to start it (default auto)\n"
      << "  --daemon PATH                 Start this holderd (implies --mode spawn)\n"
      << "  --daemon-arg ARG              Pass ARG to holderd; may be repeated\n"
      << "  --workdir PATH                Working directory for a started holderd\n"
      << "\n"
      << "Exit codes:\n"
      << "   0  a compatible daemon is running\n"
      << "   2  invalid options\n"
      << "  10  the running daemon's API version is outside the supported range\n"
      << "  11  no daemon is running (with --no-start)\n"
      << "  12  the daemon could not be started\n"
      << "  13  the daemon did not become healthy in time\n"
      << "  14  holderd was not found\n";
}

} // namespace

std::optional<std::vector<unsigned long>> parse_api_version(const std::string& text) {
  if (text.empty()) return std::nullopt;
  std::vector<unsigned long> parts;
  std::string::size_type start = 0;
  for (;;) {
    const auto dot = text.find('.', start);
    const auto piece = text.substr(start, dot == std::string::npos ? std::string::npos : dot - start);
    if (piece.empty() || piece.size() > 9) return std::nullopt;
    if (!std::all_of(piece.begin(), piece.end(), [](char ch) {
          return std::isdigit(static_cast<unsigned char>(ch)) != 0;
        })) {
      return std::nullopt;
    }
    parts.push_back(std::stoul(piece));
    if (dot == std::string::npos) break;
    start = dot + 1;
  }
  return parts;
}

int compare_api_versions(const std::vector<unsigned long>& a, const std::vector<unsigned long>& b) {
  const auto count = std::max(a.size(), b.size());
  for (std::size_t i = 0; i < count; ++i) {
    const unsigned long left = i < a.size() ? a[i] : 0;
    const unsigned long right = i < b.size() ? b[i] : 0;
    if (left < right) return -1;
    if (left > right) return 1;
  }
  return 0;
}

ApiCompatibility check_api_compatibility(const std::string& daemon_api_version, const ApiRange& range) {
  if (range.minimum.empty() && range.maximum_exclusive.empty()) return {true, ""};

  const auto actual = parse_api_version(daemon_api_version);
  if (!actual) {
    return {
        false,
        daemon_api_version.empty()
            ? "the daemon did not report an API version"
            : "the daemon reported an unrecognised API version '" + daemon_api_version + "'",
    };
  }
  if (!range.minimum.empty()) {
    const auto minimum = parse_api_version(range.minimum);
    if (!minimum) return {false, "invalid minimum API version '" + range.minimum + "'"};
    if (compare_api_versions(*actual, *minimum) < 0) {
      return {
          false,
          "the daemon API version " + daemon_api_version + " is older than the minimum supported " +
              range.minimum,
      };
    }
  }
  if (!range.maximum_exclusive.empty()) {
    const auto maximum = parse_api_version(range.maximum_exclusive);
    if (!maximum) return {false, "invalid maximum API version '" + range.maximum_exclusive + "'"};
    if (compare_api_versions(*actual, *maximum) >= 0) {
      return {
          false,
          "the daemon API version " + daemon_api_version + " is not supported; it must be below " +
              range.maximum_exclusive,
      };
    }
  }
  return {true, ""};
}

EnsureOptions parse_ensure_options(int argc, char* argv[]) {
  EnsureOptions options;
  for (int i = 2; i < argc; ++i) {
    const std::string arg = argv[i];
    std::string value;
    if (arg == "--json") {
      continue;
    } else if (arg == "--no-start") {
      options.allow_start = false;
    } else if (take_value(arg, "--api-min", argc, argv, i, &value)) {
      require_api_version(value, "--api-min");
      options.api.minimum = value;
    } else if (take_value(arg, "--api-max-exclusive", argc, argv, i, &value)) {
      require_api_version(value, "--api-max-exclusive");
      options.api.maximum_exclusive = value;
    } else if (take_value(arg, "--timeout", argc, argv, i, &value)) {
      double seconds = 0;
      try {
        std::size_t used = 0;
        seconds = std::stod(value, &used);
        if (used != value.size()) throw std::invalid_argument("trailing characters");
      } catch (const std::exception&) {
        usage_error("Option --timeout needs a number of seconds, got '" + value + "'");
      }
      if (!(seconds > 0.0) || seconds > 3600.0) {
        usage_error("Option --timeout must be above 0 and at most 3600 seconds");
      }
      options.timeout = std::chrono::milliseconds(static_cast<long long>(seconds * 1000.0));
    } else if (take_value(arg, "--mode", argc, argv, i, &value)) {
      if (value == "auto") {
        options.mode = EnsureMode::Auto;
      } else if (value == "service") {
        options.mode = EnsureMode::Service;
      } else if (value == "spawn") {
        options.mode = EnsureMode::Spawn;
      } else {
        usage_error("Option --mode must be auto, service or spawn, got '" + value + "'");
      }
    } else if (take_value(arg, "--daemon", argc, argv, i, &value)) {
      options.daemon_path = value;
    } else if (take_value(arg, "--daemon-arg", argc, argv, i, &value)) {
      options.daemon_args.push_back(value);
    } else if (take_value(arg, "--workdir", argc, argv, i, &value)) {
      options.working_dir = value;
    } else {
      usage_error("Unknown ensure option: " + arg);
    }
  }
  return options;
}

EnsureResult ensure_daemon(const holder::core::Paths& paths, const EnsureOptions& options) {
  const auto started_at = Clock::now();
  const auto elapsed_ms = [&]() {
    return static_cast<long long>(
        std::chrono::duration_cast<std::chrono::milliseconds>(Clock::now() - started_at).count()
    );
  };

  EnsureResult result;
  const auto log_path = paths.cache_dir / "holderd-start.log";

  const auto fail = [&](const std::string& code, int exit_code, const std::string& message) {
    result.ok = false;
    result.state = "failed";
    result.error_code = code;
    result.exit_code = exit_code;
    result.message = message;
    result.elapsed_ms = elapsed_ms();
    return result;
  };

  // A healthy daemon: accept it only if its API version is one the caller supports.
  const auto accept = [&](const Probe& probe, const std::string& state, const std::string& mode) {
    result.daemon = daemon_json(probe);
    const auto compatibility = check_api_compatibility(probe.api_version, options.api);
    if (!compatibility.compatible) {
      return fail("api_incompatible", kEnsureExitApiIncompatible, compatibility.reason);
    }
    result.ok = true;
    result.state = state;
    result.mode = mode;
    result.exit_code = 0;
    result.elapsed_ms = elapsed_ms();
    return result;
  };

  auto probe = probe_daemon(paths);
  if (probe.healthy) return accept(probe, "running", "existing");

  if (!options.allow_start) {
    return fail(
        "not_running",
        kEnsureExitNotRunning,
        "no healthy Holder daemon is running (" + probe.detail + ")"
    );
  }

  const auto mode = resolve_mode(options);
  std::optional<holder::platform::DetachedProcess> child;
  std::string mode_name;

  if (mode == EnsureMode::Spawn) {
    const auto daemon = locate_daemon(options);
    if (daemon.empty()) {
      return fail(
          "daemon_not_found",
          kEnsureExitDaemonNotFound,
          options.daemon_path.empty()
              ? "holderd was not found beside holderctl or on PATH"
              : "holderd was not found at " + options.daemon_path.string()
      );
    }
    holder::platform::DetachedProcessRequest request;
    request.executable = daemon;
    request.args = options.daemon_args;
    request.working_dir =
        options.working_dir.empty() ? default_working_dir(daemon) : options.working_dir;
    request.log_path = log_path;
    result.log_path = log_path.string();
    std::string error;
    child = holder::platform::DetachedProcess::start(request, &error);
    if (!child) return fail("start_failed", kEnsureExitStartFailed, error);
    result.spawned_pid = child->pid();
    mode_name = "spawned";
  } else {
#if defined(__linux__)
    const auto systemctl = systemctl_path();
    if (systemctl.empty()) {
      return fail("start_failed", kEnsureExitStartFailed, "systemctl was not found");
    }
    const auto code = run_to_completion(
        systemctl,
        {"--user", "start", kServiceUnit},
        std::chrono::seconds(30)
    );
    if (!code.has_value() || *code != 0) {
      return fail(
          "start_failed",
          kEnsureExitStartFailed,
          std::string("systemctl --user start ") + kServiceUnit + " failed" +
              (code.has_value() ? " with status " + std::to_string(*code) : "")
      );
    }
    mode_name = "service";
#else
    return fail(
        "start_failed",
        kEnsureExitStartFailed,
        "service mode needs systemd, which is only available on Linux"
    );
#endif
  }

  const auto deadline = started_at + options.timeout;
#if defined(__linux__)
  auto last_service_check = Clock::now();
#endif
  for (;;) {
    probe = probe_daemon(paths);
    if (probe.healthy) return accept(probe, "started", mode_name);

    int exit_status = 0;
    if (child && child->has_exited(&exit_status)) {
      // Another client may have started the daemon first, so ours stopped on the lock.
      probe = probe_daemon(paths);
      if (probe.healthy) return accept(probe, "running", "existing");
      return fail(
          "start_failed",
          kEnsureExitStartFailed,
          "holderd exited with status " + std::to_string(exit_status) +
              " before becoming healthy; see " + log_path.string()
      );
    }

#if defined(__linux__)
    if (mode == EnsureMode::Service && Clock::now() - last_service_check >= std::chrono::seconds(1)) {
      last_service_check = Clock::now();
      if (service_unit_failed()) {
        return fail(
            "start_failed",
            kEnsureExitStartFailed,
            std::string(kServiceUnit) + " failed; see 'journalctl --user -u " + kServiceUnit + "'"
        );
      }
    }
#endif

    if (Clock::now() >= deadline) {
      return fail(
          "timeout",
          kEnsureExitTimeout,
          "the Holder daemon did not become healthy within " + describe_seconds(options.timeout) +
              " seconds (" + probe.detail + ")"
      );
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
  }
}

nlohmann::json ensure_result_to_json(const EnsureResult& result) {
  nlohmann::json out = {
      {"ok", result.ok},
      {"state", result.state},
      {"started", result.state == "started"},
      {"exit_code", result.exit_code},
      {"elapsed_ms", result.elapsed_ms},
  };
  if (!result.mode.empty()) out["mode"] = result.mode;
  if (!result.daemon.empty()) out["daemon"] = result.daemon;
  if (result.spawned_pid > 0) out["spawned_pid"] = result.spawned_pid;
  if (!result.log_path.empty()) out["log"] = result.log_path;
  if (!result.ok) out["error"] = {{"code", result.error_code}, {"message", result.message}};
  return out;
}

int command_ensure(const holder::core::Paths& paths, int argc, char* argv[]) {
  for (int i = 2; i < argc; ++i) {
    const std::string arg = argv[i];
    if (arg == "--help" || arg == "-h") {
      print_ensure_usage(std::cout);
      return 0;
    }
  }

  const bool json_output = json_output_requested(argc, argv);
  auto options = parse_ensure_options(argc, argv);
  options.holderctl_path = holder::platform::current_executable_path();
  if (options.holderctl_path.empty() && argc > 0 && argv[0] != nullptr && *argv[0] != '\0') {
    std::error_code ec;
    options.holderctl_path = std::filesystem::absolute(argv[0], ec);
  }

  const auto result = ensure_daemon(paths, options);
  if (json_output) {
    std::cout << ensure_result_to_json(result).dump(2) << "\n";
    return result.exit_code;
  }

  if (result.ok) {
    std::cout << "Holder daemon: " << result.state << "\n";
    if (!result.mode.empty()) std::cout << "Mode: " << result.mode << "\n";
    std::cout << "URL: " << result.daemon.value("url", "") << "\n"
              << "API version: " << result.daemon.value("api_version", "") << "\n"
              << "Server version: " << result.daemon.value("server_version", "") << "\n";
    return 0;
  }

  std::cerr << "Holder daemon: failed (" << result.error_code << "): " << result.message << "\n";
  if (!result.log_path.empty()) std::cerr << "Log: " << result.log_path << "\n";
  return result.exit_code;
}

} // namespace holder::cli
