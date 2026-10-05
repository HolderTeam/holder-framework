#include "platform/DetachedProcess.h"

#include <boost/asio/io_context.hpp>
#include <boost/process/v2/process.hpp>
#include <boost/process/v2/start_dir.hpp>
#include <boost/process/v2/stdio.hpp>
#include <boost/system/system_error.hpp>

#include <cstdlib>
#include <string>
#include <system_error>
#include <utility>
#include <vector>

#ifdef _WIN32
#include <boost/process/v2/windows/creation_flags.hpp>
#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#else
#include <cerrno>
#include <cstring>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#if defined(__APPLE__)
#include <mach-o/dyld.h>
#endif
#endif

namespace holder::platform {

namespace bp = boost::process::v2;

// The child is started through Boost.Process v2, which reports a failed start (a missing
// program or start directory, a program that cannot be run) as an exception. Boost's own
// destructor would terminate a child it still owns, so ours always lets go of it first.
struct DetachedProcess::Impl {
  boost::asio::io_context context;
  std::optional<bp::process> process;
  bool exited = false;
  int exit_code = 0;

  Impl() = default;
  Impl(const Impl&) = delete;
  Impl& operator=(const Impl&) = delete;
  ~Impl() {
    if (process.has_value()) process->detach();
  }
};

#ifdef _WIN32

namespace {

std::wstring utf8_to_wide(const std::string& text) {
  if (text.empty()) return {};
  const int size =
      MultiByteToWideChar(CP_UTF8, 0, text.data(), static_cast<int>(text.size()), nullptr, 0);
  if (size <= 0) return {};
  std::wstring wide(static_cast<size_t>(size), L'\0');
  MultiByteToWideChar(CP_UTF8, 0, text.data(), static_cast<int>(text.size()), wide.data(), size);
  return wide;
}

std::string windows_error_message(DWORD code) {
  char* buffer = nullptr;
  const DWORD length = FormatMessageA(
      FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
      nullptr,
      code,
      0,
      reinterpret_cast<char*>(&buffer),
      0,
      nullptr
  );
  std::string text;
  if (length > 0 && buffer != nullptr) {
    text.assign(buffer, length);
    while (!text.empty() && (text.back() == '\r' || text.back() == '\n' || text.back() == ' ')) {
      text.pop_back();
    }
  }
  if (buffer != nullptr) LocalFree(buffer);
  if (text.empty()) text = "error " + std::to_string(code);
  return text;
}

class HandleGuard {
 public:
  explicit HandleGuard(HANDLE handle = INVALID_HANDLE_VALUE)
      : handle_(handle) {}
  HandleGuard(const HandleGuard&) = delete;
  HandleGuard& operator=(const HandleGuard&) = delete;
  ~HandleGuard() {
    if (valid()) CloseHandle(handle_);
  }

  HANDLE get() const { return handle_; }
  bool valid() const { return handle_ != INVALID_HANDLE_VALUE && handle_ != nullptr; }

 private:
  HANDLE handle_;
};

// Detached from our console and in its own process group, so a Ctrl-C or the console closing
// does not reach it, and no console window appears for it.
constexpr DWORD kDetached = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP;

} // namespace

std::optional<DetachedProcess> DetachedProcess::start(
    const DetachedProcessRequest& request,
    std::string* error
) {
  auto fail = [&](const std::string& message) -> std::optional<DetachedProcess> {
    if (error != nullptr) *error = message;
    return std::nullopt;
  };

  // Standard output and error go to the log file when there is one, otherwise to NUL.
  std::error_code ec;
  std::optional<HandleGuard> opened;
  if (!request.log_path.empty()) {
    std::filesystem::create_directories(request.log_path.parent_path(), ec);
    SECURITY_ATTRIBUTES inheritable{};
    inheritable.nLength = sizeof(inheritable);
    inheritable.bInheritHandle = TRUE;
    opened.emplace(CreateFileW(
        request.log_path.c_str(),
        FILE_APPEND_DATA,
        FILE_SHARE_READ | FILE_SHARE_WRITE,
        &inheritable,
        OPEN_ALWAYS,
        FILE_ATTRIBUTE_NORMAL,
        nullptr
    ));
    if (!opened->valid()) {
      return fail(
          "cannot open log file " + request.log_path.string() + ": " +
          windows_error_message(GetLastError())
      );
    }
  }

  std::vector<std::wstring> args;
  args.reserve(request.args.size());
  for (const auto& arg : request.args)
    args.push_back(utf8_to_wide(arg));

  const auto working_dir = request.working_dir.empty() ? std::filesystem::current_path(ec)
                                                       : request.working_dir;

  if (!request.working_dir.empty() && !std::filesystem::is_directory(working_dir, ec)) {
    return fail(
        "cannot start " + request.executable.string() + ": the working directory " +
        working_dir.string() + " does not exist"
    );
  }

  auto impl = std::make_unique<Impl>();
  auto launch = [&](auto flags) {
    if (opened.has_value()) {
      const HANDLE log = opened->get();
      impl->process.emplace(
          impl->context.get_executor(),
          request.executable.native(),
          args,
          bp::process_start_dir(working_dir.native()),
          bp::process_stdio{nullptr, log, log},
          flags
      );
    } else {
      impl->process.emplace(
          impl->context.get_executor(),
          request.executable.native(),
          args,
          bp::process_start_dir(working_dir.native()),
          bp::process_stdio{nullptr, nullptr, nullptr},
          flags
      );
    }
  };

  try {
    // Try to leave any job we are in, so the child outlives it. A job that forbids breakaway
    // makes the start fail with access denied; start again without it.
    try {
      launch(bp::windows::process_creation_flags<kDetached | CREATE_BREAKAWAY_FROM_JOB>{});
    } catch (const boost::system::system_error& breakaway) {
      if (breakaway.code().value() != ERROR_ACCESS_DENIED) throw;
      launch(bp::windows::process_creation_flags<kDetached>{});
    }
  } catch (const boost::system::system_error& failure) {
    return fail("cannot start " + request.executable.string() + ": " + failure.code().message());
  }
  return DetachedProcess(std::move(impl));
}

std::filesystem::path find_executable_on_path(const std::string& name) {
  const std::wstring wide = utf8_to_wide(name);
  std::vector<wchar_t> buffer(MAX_PATH);
  for (;;) {
    const DWORD length = SearchPathW(
        nullptr,
        wide.c_str(),
        L".exe",
        static_cast<DWORD>(buffer.size()),
        buffer.data(),
        nullptr
    );
    if (length == 0) return {};
    if (length < buffer.size()) return std::filesystem::path(std::wstring(buffer.data(), length));
    buffer.resize(length + 1);
  }
}

std::filesystem::path current_executable_path() {
  std::vector<wchar_t> buffer(MAX_PATH);
  for (;;) {
    const DWORD length =
        GetModuleFileNameW(nullptr, buffer.data(), static_cast<DWORD>(buffer.size()));
    if (length == 0) return {};
    if (length < buffer.size()) return std::filesystem::path(std::wstring(buffer.data(), length));
    buffer.resize(buffer.size() * 2);
  }
}

#else // POSIX

namespace {

// Standard descriptors must not be reused for our own files: dup2 onto the same number
// is a no-op and would leave close-on-exec set on a descriptor the child needs.
int move_above_stdio(int fd) {
  if (fd < 0 || fd > STDERR_FILENO) return fd;
  const int moved = ::fcntl(fd, F_DUPFD_CLOEXEC, STDERR_FILENO + 1);
  ::close(fd);
  return moved;
}

// Runs in the child between fork and exec: a session of its own, so a signal sent to the
// starter's process group (Ctrl-C in a terminal, for one) does not reach it. A failure is
// reported to the caller the same way a failed exec is.
struct NewSession {
  template <typename Launcher, typename Path>
  boost::system::error_code on_exec_setup(Launcher&, const Path&, const char* const*&) const {
    if (::setsid() == -1) return boost::system::error_code(errno, boost::system::system_category());
    return {};
  }
};

} // namespace

std::optional<DetachedProcess> DetachedProcess::start(
    const DetachedProcessRequest& request,
    std::string* error
) {
  auto fail = [&](const std::string& message) -> std::optional<DetachedProcess> {
    if (error != nullptr) *error = message;
    return std::nullopt;
  };

  const std::string exe = request.executable.string();

  int log_fd = -1;
  std::error_code ec;
  if (!request.log_path.empty()) {
    std::filesystem::create_directories(request.log_path.parent_path(), ec);
    log_fd = move_above_stdio(
        ::open(request.log_path.c_str(), O_WRONLY | O_CREAT | O_APPEND | O_CLOEXEC, 0600)
    );
    if (log_fd < 0) {
      return fail(
          "cannot open log file " + request.log_path.string() + ": " + std::strerror(errno)
      );
    }
  }

  const auto working_dir = request.working_dir.empty() ? std::filesystem::current_path(ec)
                                                       : request.working_dir;

  if (!request.working_dir.empty() && !std::filesystem::is_directory(working_dir, ec)) {
    return fail(
        "cannot start " + request.executable.string() + ": the working directory " +
        working_dir.string() + " does not exist"
    );
  }

  auto impl = std::make_unique<Impl>();
  auto launch = [&]() {
    if (log_fd >= 0) {
      impl->process.emplace(
          impl->context.get_executor(),
          request.executable.native(),
          request.args,
          bp::process_start_dir(working_dir.native()),
          bp::process_stdio{nullptr, log_fd, log_fd},
          NewSession{}
      );
    } else {
      impl->process.emplace(
          impl->context.get_executor(),
          request.executable.native(),
          request.args,
          bp::process_start_dir(working_dir.native()),
          bp::process_stdio{nullptr, nullptr, nullptr},
          NewSession{}
      );
    }
  };

  std::string failure;
  try {
    launch();
  } catch (const boost::system::system_error& error_in_launch) {
    failure = error_in_launch.code().message();
  }
  if (log_fd >= 0) ::close(log_fd);
  if (!failure.empty()) return fail("cannot start " + exe + ": " + failure);
  return DetachedProcess(std::move(impl));
}

std::filesystem::path find_executable_on_path(const std::string& name) {
  if (name.empty()) return {};
  if (name.find('/') != std::string::npos) {
    return ::access(name.c_str(), X_OK) == 0 ? std::filesystem::path(name)
                                             : std::filesystem::path();
  }
  const char* path_env = std::getenv("PATH");
  if (path_env == nullptr) return {};
  const std::string search = path_env;
  std::string::size_type start = 0;
  while (start <= search.size()) {
    auto end = search.find(':', start);
    if (end == std::string::npos) end = search.size();
    const std::string directory = search.substr(start, end - start);
    if (!directory.empty()) {
      const std::filesystem::path candidate = std::filesystem::path(directory) / name;
      std::error_code ec;
      if (std::filesystem::is_regular_file(candidate, ec) &&
          ::access(candidate.c_str(), X_OK) == 0) {
        return candidate;
      }
    }
    start = end + 1;
  }
  return {};
}

std::filesystem::path current_executable_path() {
#if defined(__linux__)
  std::error_code ec;
  const auto path = std::filesystem::read_symlink("/proc/self/exe", ec);
  return ec ? std::filesystem::path() : path;
#elif defined(__APPLE__)
  uint32_t size = 0;
  _NSGetExecutablePath(nullptr, &size);
  std::string buffer(size, '\0');
  if (_NSGetExecutablePath(buffer.data(), &size) != 0) return {};
  buffer.resize(std::strlen(buffer.c_str()));
  std::error_code ec;
  const auto canonical = std::filesystem::weakly_canonical(buffer, ec);
  return ec ? std::filesystem::path(buffer) : canonical;
#else
  return {};
#endif
}

#endif

long long DetachedProcess::pid() const {
  return impl_ && impl_->process.has_value() ? static_cast<long long>(impl_->process->id()) : 0;
}

bool DetachedProcess::has_exited(int* exit_code) {
  if (!impl_ || !impl_->process.has_value()) return true;
  if (!impl_->exited) {
    boost::system::error_code ec;
    if (impl_->process->running(ec) && !ec) return false;
    impl_->exited = true;
    if (ec) {
      impl_->exit_code = -1;
    } else {
      const auto status = impl_->process->native_exit_code();
#ifdef _WIN32
      impl_->exit_code = static_cast<int>(status);
#else
      if (WIFEXITED(status)) {
        impl_->exit_code = WEXITSTATUS(status);
      } else if (WIFSIGNALED(status)) {
        impl_->exit_code = 128 + WTERMSIG(status);
      } else {
        impl_->exit_code = -1;
      }
#endif
    }
  }
  if (exit_code != nullptr) *exit_code = impl_->exit_code;
  return true;
}

DetachedProcess::DetachedProcess(std::unique_ptr<Impl> impl)
    : impl_(std::move(impl)) {}
DetachedProcess::DetachedProcess(DetachedProcess&&) noexcept = default;
DetachedProcess& DetachedProcess::operator=(DetachedProcess&&) noexcept = default;
DetachedProcess::~DetachedProcess() = default;

} // namespace holder::platform
