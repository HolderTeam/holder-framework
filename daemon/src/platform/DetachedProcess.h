#pragma once

#include <filesystem>
#include <memory>
#include <optional>
#include <string>
#include <vector>

namespace holder::platform {

struct DetachedProcessRequest {
  // Full path of the program to run.
  std::filesystem::path executable;
  // Arguments after the program name.
  std::vector<std::string> args;
  // Working directory for the child; empty inherits ours.
  std::filesystem::path working_dir;
  // Standard output and error are appended to this file; empty discards them.
  std::filesystem::path log_path;
};

// A child started so that it keeps running after this process exits: it gets its own
// session on POSIX, and its own process group without a console window on Windows.
// Destroying the object releases our handle to the child; it never stops it.
class DetachedProcess {
 public:
  DetachedProcess(DetachedProcess&&) noexcept;
  DetachedProcess& operator=(DetachedProcess&&) noexcept;
  DetachedProcess(const DetachedProcess&) = delete;
  DetachedProcess& operator=(const DetachedProcess&) = delete;
  ~DetachedProcess();

  // Returns nullopt and sets *error when the program cannot be started, including when
  // the executable is missing or not runnable.
  static std::optional<DetachedProcess> start(
      const DetachedProcessRequest& request,
      std::string* error
  );

  long long pid() const;

  // Never blocks. True once the child has exited; *exit_code then receives its status
  // (128 plus the signal number if a signal ended it, -1 if it is not known).
  bool has_exited(int* exit_code = nullptr);

 private:
  struct Impl;
  explicit DetachedProcess(std::unique_ptr<Impl> impl);
  std::unique_ptr<Impl> impl_;
};

// Searches PATH (and the executable extensions on Windows) for a program; empty if not found.
std::filesystem::path find_executable_on_path(const std::string& name);

// Path of the running program, or empty if the platform cannot tell.
std::filesystem::path current_executable_path();

} // namespace holder::platform
