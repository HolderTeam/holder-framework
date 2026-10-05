#pragma once

#include "platform/Paths.h"

#include <nlohmann/json.hpp>

#include <chrono>
#include <filesystem>
#include <optional>
#include <string>
#include <vector>

namespace holder::cli {

// Exit codes of `holderctl ensure`. 0 means a compatible daemon is running.
inline constexpr int kEnsureExitUsage = 2;
inline constexpr int kEnsureExitApiIncompatible = 10;
inline constexpr int kEnsureExitNotRunning = 11;
inline constexpr int kEnsureExitStartFailed = 12;
inline constexpr int kEnsureExitTimeout = 13;
inline constexpr int kEnsureExitDaemonNotFound = 14;
// Only for `holderctl start`: the running daemon will stop itself when idle.
inline constexpr int kEnsureExitEphemeral = 15;

// The daemon API versions a caller supports: minimum is inclusive, maximum_exclusive is the
// first unsupported version. An empty bound is not checked.
struct ApiRange {
  std::string minimum;
  std::string maximum_exclusive;
};

// "0.1" -> {0, 1}. Only dot-separated decimal numbers are accepted.
std::optional<std::vector<unsigned long>> parse_api_version(const std::string& text);

// -1, 0 or 1. Missing trailing components count as zero, so "1" equals "1.0".
int compare_api_versions(const std::vector<unsigned long>& a, const std::vector<unsigned long>& b);

struct ApiCompatibility {
  bool compatible = true;
  std::string reason;
};

ApiCompatibility check_api_compatibility(
    const std::string& daemon_api_version,
    const ApiRange& range
);

enum class EnsureMode { Auto, Service, Spawn };

struct EnsureOptions {
  ApiRange api;
  EnsureMode mode = EnsureMode::Auto;
  bool allow_start = true;
  std::chrono::milliseconds timeout{60000};
  // Explicit holderd to start (implies spawning); empty looks beside holderctl, then on PATH.
  std::filesystem::path daemon_path;
  // Working directory for a spawned holderd; empty picks the installed data directory.
  std::filesystem::path working_dir;
  std::vector<std::string> daemon_args;
  // Start a spawned daemon with --idle-exit, so it stops itself after this many seconds without
  // activity. Not used for the systemd service, which stays running.
  std::optional<int> idle_exit_seconds;
  // The caller needs a daemon that stays running (`holderctl start`): a healthy daemon that was
  // started with --idle-exit is refused with kEnsureExitEphemeral instead of accepted.
  bool keep_running = false;
  // The running holderctl, used to find a holderd installed beside it.
  std::filesystem::path holderctl_path;
};

struct EnsureResult {
  bool ok = false;
  std::string state; // "running", "started" or "failed"
  std::string mode; // "existing", "service" or "spawned"; empty if nothing was started
  int exit_code = 0;
  std::string error_code; // set on failure
  std::string message;
  nlohmann::json daemon = nlohmann::json::object(); // pid, url, api_version, server_version
  long long spawned_pid = 0; // the holderd this call started, if any
  int idle_exit_seconds = 0; // set when the spawned daemon was started with --idle-exit
  std::string log_path;
  long long elapsed_ms = 0;
};

// Throws CliError (exit code kEnsureExitUsage) for invalid options. argv[2..] are the options.
EnsureOptions parse_ensure_options(int argc, char* argv[]);

// Where a daemon started by ensure runs. It looks for its data (schema, config) in its working
// directory, so this is the directory that holds them in each layout: share/holder-daemon in an
// installed layout, Contents/Resources in a macOS app bundle, and otherwise beside the binary.
std::filesystem::path default_daemon_working_dir(const std::filesystem::path& daemon);

EnsureResult ensure_daemon(const holder::core::Paths& paths, const EnsureOptions& options);

nlohmann::json ensure_result_to_json(const EnsureResult& result);

} // namespace holder::cli
