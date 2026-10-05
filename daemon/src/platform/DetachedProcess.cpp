#include "platform/DetachedProcess.h"

#include <cstdlib>
#include <string>
#include <system_error>
#include <utility>
#include <vector>

#ifdef _WIN32
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

#ifdef _WIN32

struct DetachedProcess::Impl {
  HANDLE process = nullptr;
  DWORD pid = 0;
  bool exited = false;
  int exit_code = 0;

  Impl() = default;
  Impl(const Impl&) = delete;
  Impl& operator=(const Impl&) = delete;
  ~Impl() {
    if (process != nullptr) CloseHandle(process);
  }
};

namespace {

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

std::wstring utf8_to_wide(const std::string& text) {
  if (text.empty()) return {};
  const int size = MultiByteToWideChar(CP_UTF8, 0, text.data(), static_cast<int>(text.size()), nullptr, 0);
  if (size <= 0) return {};
  std::wstring wide(static_cast<size_t>(size), L'\0');
  MultiByteToWideChar(CP_UTF8, 0, text.data(), static_cast<int>(text.size()), wide.data(), size);
  return wide;
}

// Quotes one argument following the rules CommandLineToArgvW and the C runtime use.
void append_argument(std::wstring& command, const std::wstring& arg) {
  if (!command.empty()) command.push_back(L' ');
  if (!arg.empty() && arg.find_first_of(L" \t\n\v\"") == std::wstring::npos) {
    command += arg;
    return;
  }
  command.push_back(L'"');
  for (auto it = arg.begin();; ++it) {
    size_t backslashes = 0;
    while (it != arg.end() && *it == L'\\') {
      ++it;
      ++backslashes;
    }
    if (it == arg.end()) {
      command.append(backslashes * 2, L'\\');
      break;
    }
    if (*it == L'"') {
      command.append(backslashes * 2 + 1, L'\\');
      command.push_back(L'"');
    } else {
      command.append(backslashes, L'\\');
      command.push_back(*it);
    }
  }
  command.push_back(L'"');
}

class HandleGuard {
 public:
  explicit HandleGuard(HANDLE handle = INVALID_HANDLE_VALUE) : handle_(handle) {}
  HandleGuard(HandleGuard&& other) noexcept : handle_(other.release()) {}
  HandleGuard& operator=(HandleGuard&& other) noexcept {
    if (this != &other) {
      reset();
      handle_ = other.release();
    }
    return *this;
  }
  HandleGuard(const HandleGuard&) = delete;
  HandleGuard& operator=(const HandleGuard&) = delete;
  ~HandleGuard() { reset(); }

  HANDLE get() const { return handle_; }
  bool valid() const { return handle_ != INVALID_HANDLE_VALUE && handle_ != nullptr; }
  HANDLE release() {
    const HANDLE handle = handle_;
    handle_ = INVALID_HANDLE_VALUE;
    return handle;
  }
  void reset() {
    if (valid()) CloseHandle(handle_);
    handle_ = INVALID_HANDLE_VALUE;
  }

 private:
  HANDLE handle_;
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

  std::error_code ec;
  if (!std::filesystem::is_regular_file(request.executable, ec)) {
    return fail("cannot start " + request.executable.string() + ": no such program");
  }

  SECURITY_ATTRIBUTES inheritable{};
  inheritable.nLength = sizeof(inheritable);
  inheritable.bInheritHandle = TRUE;

  HandleGuard null_handle(CreateFileW(
      L"NUL",
      GENERIC_READ | GENERIC_WRITE,
      FILE_SHARE_READ | FILE_SHARE_WRITE,
      &inheritable,
      OPEN_EXISTING,
      FILE_ATTRIBUTE_NORMAL,
      nullptr
  ));
  if (!null_handle.valid()) {
    return fail("cannot open NUL: " + windows_error_message(GetLastError()));
  }

  // Standard output and error go to the log file when there is one, otherwise to NUL.
  HandleGuard log_handle;
  if (!request.log_path.empty()) {
    std::filesystem::create_directories(request.log_path.parent_path(), ec);
    log_handle = HandleGuard(CreateFileW(
        request.log_path.c_str(),
        FILE_APPEND_DATA,
        FILE_SHARE_READ | FILE_SHARE_WRITE,
        &inheritable,
        OPEN_ALWAYS,
        FILE_ATTRIBUTE_NORMAL,
        nullptr
    ));
    if (!log_handle.valid()) {
      return fail(
          "cannot open log file " + request.log_path.string() + ": " +
          windows_error_message(GetLastError())
      );
    }
  }
  const HANDLE output_handle = log_handle.valid() ? log_handle.get() : null_handle.get();

  std::wstring command;
  append_argument(command, request.executable.wstring());
  for (const auto& arg : request.args) append_argument(command, utf8_to_wide(arg));
  std::vector<wchar_t> mutable_command(command.begin(), command.end());
  mutable_command.push_back(L'\0');

  STARTUPINFOW startup{};
  startup.cb = sizeof(startup);
  startup.dwFlags = STARTF_USESTDHANDLES;
  startup.hStdInput = null_handle.get();
  startup.hStdOutput = output_handle;
  startup.hStdError = output_handle;

  const std::wstring working_dir = request.working_dir.wstring();
  const wchar_t* cwd = working_dir.empty() ? nullptr : working_dir.c_str();
  const DWORD base_flags = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_UNICODE_ENVIRONMENT;

  auto create = [&](DWORD flags, PROCESS_INFORMATION* info) {
    return CreateProcessW(
        request.executable.c_str(),
        mutable_command.data(),
        nullptr,
        nullptr,
        TRUE,
        flags,
        nullptr,
        cwd,
        &startup,
        info
    );
  };

  // Try to leave any job we are in, so the child outlives it. If the job forbids
  // breakaway, CreateProcess fails with access denied; retry without it.
  PROCESS_INFORMATION info{};
  BOOL created = create(base_flags | CREATE_BREAKAWAY_FROM_JOB, &info);
  if (!created && GetLastError() == ERROR_ACCESS_DENIED) created = create(base_flags, &info);
  if (!created) {
    return fail(
        "cannot start " + request.executable.string() + ": " + windows_error_message(GetLastError())
    );
  }
  CloseHandle(info.hThread);

  auto impl = std::make_unique<Impl>();
  impl->process = info.hProcess;
  impl->pid = info.dwProcessId;
  return DetachedProcess(std::move(impl));
}

long long DetachedProcess::pid() const { return impl_ ? static_cast<long long>(impl_->pid) : 0; }

bool DetachedProcess::has_exited(int* exit_code) {
  if (!impl_) return true;
  if (!impl_->exited) {
    if (WaitForSingleObject(impl_->process, 0) == WAIT_TIMEOUT) return false;
    DWORD code = 0;
    impl_->exit_code = GetExitCodeProcess(impl_->process, &code) ? static_cast<int>(code) : -1;
    impl_->exited = true;
  }
  if (exit_code != nullptr) *exit_code = impl_->exit_code;
  return true;
}

std::filesystem::path find_executable_on_path(const std::string& name) {
  const std::wstring wide = utf8_to_wide(name);
  std::vector<wchar_t> buffer(MAX_PATH);
  for (;;) {
    const DWORD length =
        SearchPathW(nullptr, wide.c_str(), L".exe", static_cast<DWORD>(buffer.size()), buffer.data(), nullptr);
    if (length == 0) return {};
    if (length < buffer.size()) return std::filesystem::path(std::wstring(buffer.data(), length));
    buffer.resize(length + 1);
  }
}

std::filesystem::path current_executable_path() {
  std::vector<wchar_t> buffer(MAX_PATH);
  for (;;) {
    const DWORD length = GetModuleFileNameW(nullptr, buffer.data(), static_cast<DWORD>(buffer.size()));
    if (length == 0) return {};
    if (length < buffer.size()) return std::filesystem::path(std::wstring(buffer.data(), length));
    buffer.resize(buffer.size() * 2);
  }
}

#else // POSIX

struct DetachedProcess::Impl {
  pid_t pid = 0;
  bool exited = false;
  int exit_code = 0;
};

namespace {

// Standard descriptors must not be reused for our own files: dup2 onto the same number
// is a no-op and would leave close-on-exec set on a descriptor the child needs.
int move_above_stdio(int fd) {
  if (fd < 0 || fd > STDERR_FILENO) return fd;
  const int moved = ::fcntl(fd, F_DUPFD_CLOEXEC, STDERR_FILENO + 1);
  ::close(fd);
  return moved;
}

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
  const std::string working_dir = request.working_dir.string();

  // Everything the child needs is prepared before fork, so the child only has to make
  // async-signal-safe calls.
  std::vector<std::string> arg_strings;
  arg_strings.push_back(exe);
  arg_strings.insert(arg_strings.end(), request.args.begin(), request.args.end());
  std::vector<char*> argv;
  argv.reserve(arg_strings.size() + 1);
  for (auto& arg : arg_strings) argv.push_back(arg.data());
  argv.push_back(nullptr);

  int log_fd = -1;
  if (!request.log_path.empty()) {
    std::error_code ec;
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
  const int null_fd = move_above_stdio(::open("/dev/null", O_RDWR | O_CLOEXEC));
  if (null_fd < 0) {
    const std::string reason = std::strerror(errno);
    if (log_fd >= 0) ::close(log_fd);
    return fail("cannot open /dev/null: " + reason);
  }

  // The child reports a failed chdir or exec through this pipe. It closes on a
  // successful exec, so a read that returns nothing means the program started.
  int status_pipe[2] = {-1, -1};
  if (::pipe(status_pipe) != 0) {
    const std::string reason = std::strerror(errno);
    if (log_fd >= 0) ::close(log_fd);
    ::close(null_fd);
    return fail("cannot create a pipe: " + reason);
  }
  ::fcntl(status_pipe[0], F_SETFD, FD_CLOEXEC);
  ::fcntl(status_pipe[1], F_SETFD, FD_CLOEXEC);

  const pid_t pid = ::fork();
  if (pid < 0) {
    const std::string reason = std::strerror(errno);
    if (log_fd >= 0) ::close(log_fd);
    ::close(null_fd);
    ::close(status_pipe[0]);
    ::close(status_pipe[1]);
    return fail("cannot fork: " + reason);
  }

  if (pid == 0) {
    // Child: async-signal-safe calls only.
    ::setsid();
    int child_errno = 0;
    if (!working_dir.empty() && ::chdir(working_dir.c_str()) != 0) {
      child_errno = errno;
    } else {
      const int output_fd = log_fd >= 0 ? log_fd : null_fd;
      ::dup2(null_fd, STDIN_FILENO);
      ::dup2(output_fd, STDOUT_FILENO);
      ::dup2(output_fd, STDERR_FILENO);
      ::execv(exe.c_str(), argv.data());
      child_errno = errno;
    }
    const ssize_t written = ::write(status_pipe[1], &child_errno, sizeof(child_errno));
    (void)written;
    ::_exit(127);
  }

  ::close(status_pipe[1]);
  if (log_fd >= 0) ::close(log_fd);
  ::close(null_fd);

  int child_errno = 0;
  ssize_t count = 0;
  do {
    count = ::read(status_pipe[0], &child_errno, sizeof(child_errno));
  } while (count < 0 && errno == EINTR);
  ::close(status_pipe[0]);

  if (count == static_cast<ssize_t>(sizeof(child_errno))) {
    int ignored = 0;
    while (::waitpid(pid, &ignored, 0) < 0 && errno == EINTR) {
    }
    return fail("cannot start " + exe + ": " + std::strerror(child_errno));
  }

  auto impl = std::make_unique<Impl>();
  impl->pid = pid;
  return DetachedProcess(std::move(impl));
}

long long DetachedProcess::pid() const { return impl_ ? static_cast<long long>(impl_->pid) : 0; }

bool DetachedProcess::has_exited(int* exit_code) {
  if (!impl_) return true;
  if (!impl_->exited) {
    int status = 0;
    pid_t result = 0;
    do {
      result = ::waitpid(impl_->pid, &status, WNOHANG);
    } while (result < 0 && errno == EINTR);
    if (result == 0) return false;
    impl_->exited = true;
    if (result < 0) {
      impl_->exit_code = -1;
    } else if (WIFEXITED(status)) {
      impl_->exit_code = WEXITSTATUS(status);
    } else if (WIFSIGNALED(status)) {
      impl_->exit_code = 128 + WTERMSIG(status);
    } else {
      impl_->exit_code = -1;
    }
  }
  if (exit_code != nullptr) *exit_code = impl_->exit_code;
  return true;
}

std::filesystem::path find_executable_on_path(const std::string& name) {
  if (name.empty()) return {};
  if (name.find('/') != std::string::npos) {
    return ::access(name.c_str(), X_OK) == 0 ? std::filesystem::path(name) : std::filesystem::path();
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
      if (std::filesystem::is_regular_file(candidate, ec) && ::access(candidate.c_str(), X_OK) == 0) {
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

DetachedProcess::DetachedProcess(std::unique_ptr<Impl> impl) : impl_(std::move(impl)) {}
DetachedProcess::DetachedProcess(DetachedProcess&&) noexcept = default;
DetachedProcess& DetachedProcess::operator=(DetachedProcess&&) noexcept = default;
DetachedProcess::~DetachedProcess() = default;

} // namespace holder::platform
