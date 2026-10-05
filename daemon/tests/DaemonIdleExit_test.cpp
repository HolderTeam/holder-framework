#include "ProcessTestSupport.h"

#include "platform/DetachedProcess.h"

#include <catch2/catch_test_macros.hpp>

#include <chrono>
#include <optional>
#include <string>
#include <vector>

#ifndef _WIN32

#include <boost/asio.hpp>
#include <boost/beast/core.hpp>
#include <boost/beast/http.hpp>

namespace {

using holder::test::DaemonInfo;
using holder::test::IsolatedHome;
using namespace std::chrono_literals;

// Starts the real holderd with the given extra arguments, in the home's environment.
std::optional<holder::platform::DetachedProcess> start_daemon(
    const IsolatedHome& home,
    const std::vector<std::string>& extra
) {
  holder::platform::DetachedProcessRequest request;
  request.executable = HOLDER_BIN_PATH;
  request.args = {"--port", "0"};
  request.args.insert(request.args.end(), extra.begin(), extra.end());
  request.working_dir = IsolatedHome::source_root();
  request.log_path = home.root() / "holderd.log";
  std::string error;
  auto process = holder::platform::DetachedProcess::start(request, &error);
  INFO("starting holderd: " << error);
  return process;
}

bool exited(holder::platform::DetachedProcess& process, int* code = nullptr) {
  return process.has_exited(code);
}

// A GET /events stream held open until it is closed or destroyed.
class OpenEventStream {
 public:
  explicit OpenEventStream(const DaemonInfo& info)
      : stream_(ioc_) {
    namespace http = boost::beast::http;
    boost::asio::ip::tcp::resolver resolver(ioc_);
    stream_.expires_after(std::chrono::seconds(5));
    stream_.connect(resolver.resolve(info.bind, std::to_string(info.port)));
    http::request<http::empty_body> request{http::verb::get, "/events", 11};
    request.set(http::field::host, info.bind);
    request.set(http::field::authorization, "Bearer " + info.token);
    request.set(http::field::accept, "text/event-stream");
    http::write(stream_, request);
    boost::beast::flat_buffer buffer;
    http::response_parser<http::empty_body> parser;
    http::read_header(stream_, buffer, parser);  // headers only; the body never ends
    status_ = parser.get().result();
    stream_.expires_never();
  }

  boost::beast::http::status status() const { return status_; }

  void close() {
    boost::system::error_code ignored;
    stream_.socket().shutdown(boost::asio::ip::tcp::socket::shutdown_both, ignored);
    stream_.socket().close(ignored);
  }

 private:
  boost::asio::io_context ioc_;
  boost::beast::tcp_stream stream_;
  boost::beast::http::status status_{};
};

} // namespace

TEST_CASE("holderd --idle-exit stops a daemon that nobody uses", "[idle][process]") {
  IsolatedHome home;
  auto daemon = start_daemon(home, {"--idle-exit", "2"});
  REQUIRE(daemon.has_value());
  REQUIRE(home.wait_for_daemon_info(60s).has_value());

  int code = -1;
  REQUIRE(holder::test::wait_until(30s, [&]() { return exited(*daemon, &code); }));
  REQUIRE(code == 0);
  REQUIRE(holder::test::read_file(home.root() / "holderd.log").find("idle for 2 seconds") != std::string::npos);
}

TEST_CASE("holderd without --idle-exit keeps running while unused", "[idle][process]") {
  IsolatedHome home;
  auto daemon = start_daemon(home, {});
  REQUIRE(daemon.has_value());
  REQUIRE(home.wait_for_daemon_info(60s).has_value());

  std::this_thread::sleep_for(3s);
  REQUIRE_FALSE(exited(*daemon));
  home.track(daemon->pid());
}

TEST_CASE("requests keep a daemon with --idle-exit alive", "[idle][process]") {
  IsolatedHome home;
  auto daemon = start_daemon(home, {"--idle-exit", "2"});
  REQUIRE(daemon.has_value());
  const auto info = home.wait_for_daemon_info(60s);
  REQUIRE(info.has_value());

  // Well past the idle limit, a request every half second keeps it up.
  const auto until = std::chrono::steady_clock::now() + 5s;
  while (std::chrono::steady_clock::now() < until) {
    const auto reply = holder::test::http_request_raw(
        info->bind, info->port, info->token, boost::beast::http::verb::get, "/health"
    );
    REQUIRE(reply.status == boost::beast::http::status::ok);
    REQUIRE_FALSE(exited(*daemon));
    std::this_thread::sleep_for(500ms);
  }

  // Once the requests stop, it goes.
  REQUIRE(holder::test::wait_until(30s, [&]() { return exited(*daemon); }));
}

TEST_CASE("an open event stream keeps the daemon alive and a closing one restarts the quiet period",
          "[idle][process]") {
  IsolatedHome home;
  auto daemon = start_daemon(home, {"--idle-exit", "2"});
  REQUIRE(daemon.has_value());
  const auto info = home.wait_for_daemon_info(60s);
  REQUIRE(info.has_value());

  OpenEventStream stream(*info);
  REQUIRE(stream.status() == boost::beast::http::status::ok);

  // Subscribed for more than twice the idle limit with no other activity.
  for (int i = 0; i < 9; ++i) {
    std::this_thread::sleep_for(500ms);
    REQUIRE_FALSE(exited(*daemon));
  }

  // A client that drops its stream and comes back gets a full quiet period to do so.
  stream.close();
  std::this_thread::sleep_for(700ms);
  REQUIRE_FALSE(exited(*daemon));

  // Nobody returns, so it stops.
  REQUIRE(holder::test::wait_until(30s, [&]() { return exited(*daemon); }));
}

TEST_CASE("SIGTERM still stops a daemon started with --idle-exit at once", "[idle][process]") {
  IsolatedHome home;
  auto daemon = start_daemon(home, {"--idle-exit", "3600"});
  REQUIRE(daemon.has_value());
  REQUIRE(home.wait_for_daemon_info(60s).has_value());

  ::kill(static_cast<pid_t>(daemon->pid()), SIGTERM);
  int code = -1;
  REQUIRE(holder::test::wait_until(15s, [&]() { return exited(*daemon, &code); }));
  REQUIRE(code == 0);
}

TEST_CASE("holderd rejects invalid --idle-exit values", "[idle][process]") {
  IsolatedHome home;
  for (const char* bad : {"0", "-3", "abc", "86401", "99999999"}) {
    INFO("value: " << bad);
    const std::string command = "\"" + std::string(HOLDER_BIN_PATH) + "\" --port 0 --idle-exit " + bad +
                                " > /dev/null 2>&1";
    REQUIRE(holder::test::run_system_command(command) == 2);
  }
}

#endif
