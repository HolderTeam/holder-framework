#include "core/ActivityTracker.h"

#include <catch2/catch_test_macros.hpp>

#include <chrono>
#include <stdexcept>
#include <thread>
#include <vector>

using holder::core::ActivityTracker;
using namespace std::chrono_literals;

TEST_CASE("the activity tracker counts work in progress", "[activity]") {
  ActivityTracker tracker;
  REQUIRE(tracker.active() == 0);
  {
    const auto first = tracker.begin();
    REQUIRE(tracker.active() == 1);
    {
      const auto second = tracker.begin();
      REQUIRE(tracker.active() == 2);
    }
    REQUIRE(tracker.active() == 1);
  }
  REQUIRE(tracker.active() == 0);
}

TEST_CASE("a moved scope releases exactly once", "[activity]") {
  ActivityTracker tracker;
  {
    auto original = tracker.begin();
    auto moved = std::move(original);
    REQUIRE(tracker.active() == 1);
    ActivityTracker::Scope assigned;
    assigned = std::move(moved);
    REQUIRE(tracker.active() == 1);
  }
  REQUIRE(tracker.active() == 0);
}

TEST_CASE("a scope is released when an exception unwinds past it", "[activity]") {
  ActivityTracker tracker;
  try {
    const auto scope = tracker.begin();
    REQUIRE(tracker.active() == 1);
    throw std::runtime_error("work failed");
  } catch (const std::runtime_error&) {
  }
  REQUIRE(tracker.active() == 0);
}

TEST_CASE("a scope can travel to another thread and be released there", "[activity]") {
  ActivityTracker tracker;
  std::thread worker([scope = tracker.begin(), &tracker]() {
    REQUIRE(tracker.active() == 1);
    std::this_thread::sleep_for(20ms);
  });
  worker.join();
  REQUIRE(tracker.active() == 0);
}

TEST_CASE("quiet time restarts when activity is recorded", "[activity]") {
  ActivityTracker tracker;
  std::this_thread::sleep_for(120ms);
  REQUIRE(tracker.quiet_for() >= 100ms);

  tracker.touch();
  REQUIRE(tracker.quiet_for() < 100ms);

  std::this_thread::sleep_for(120ms);
  REQUIRE(tracker.quiet_for() >= 100ms);
  { const auto scope = tracker.begin(); } // starting and finishing work both count as activity
  REQUIRE(tracker.quiet_for() < 100ms);
}

TEST_CASE(
    "the daemon is idle only with no work, no streams and a full quiet period",
    "[activity]"
) {
  ActivityTracker tracker;

  SECTION("a new tracker is not idle until the quiet period has passed") {
    REQUIRE_FALSE(tracker.idle(1h));
    std::this_thread::sleep_for(120ms);
    REQUIRE(tracker.idle(100ms));
  }

  SECTION("an open stream prevents idleness however long it has been quiet") {
    std::this_thread::sleep_for(120ms);
    REQUIRE(tracker.idle(100ms, 0));
    REQUIRE_FALSE(tracker.idle(100ms, 1));
  }

  SECTION("work in progress prevents idleness, and finishing it restarts the quiet period") {
    {
      const auto scope = tracker.begin();
      std::this_thread::sleep_for(120ms);
      REQUIRE_FALSE(tracker.idle(100ms));
    }
    REQUIRE_FALSE(tracker.idle(1h));
    std::this_thread::sleep_for(120ms);
    REQUIRE(tracker.idle(100ms));
  }
}

TEST_CASE("scopes taken on many threads always balance", "[activity]") {
  ActivityTracker tracker;
  std::vector<std::thread> threads;
  for (int i = 0; i < 8; ++i) {
    threads.emplace_back([&tracker]() {
      for (int n = 0; n < 2000; ++n) {
        const auto scope = tracker.begin();
        tracker.touch();
      }
    });
  }
  for (auto& thread : threads)
    thread.join();
  REQUIRE(tracker.active() == 0);
}

TEST_CASE("the process-wide tracker is a single instance", "[activity]") {
  REQUIRE(&holder::core::activity() == &holder::core::activity());
}

TEST_CASE(
    "a goodbye lets an otherwise idle daemon stop after a short grace",
    "[activity][goodbye]"
) {
  ActivityTracker tracker(50ms);
  const auto long_quiet = std::chrono::hours(1);
  REQUIRE_FALSE(tracker.goodbye_pending());

  tracker.say_goodbye();
  REQUIRE(tracker.goodbye_pending());
  REQUIRE_FALSE(tracker.idle(long_quiet));

  std::this_thread::sleep_for(120ms);
  REQUIRE(tracker.idle(long_quiet));
}

TEST_CASE("without a goodbye the full quiet period still applies", "[activity][goodbye]") {
  ActivityTracker tracker(10ms);
  std::this_thread::sleep_for(60ms);
  REQUIRE_FALSE(tracker.idle(std::chrono::hours(1)));
}

TEST_CASE(
    "a goodbye never shortens a quiet period that is already shorter",
    "[activity][goodbye]"
) {
  ActivityTracker tracker(std::chrono::hours(1));
  tracker.say_goodbye();
  std::this_thread::sleep_for(60ms);
  REQUIRE(tracker.idle(30ms));
}

TEST_CASE(
    "a goodbye does not override work, open streams or recent activity",
    "[activity][goodbye]"
) {
  ActivityTracker tracker(10ms);
  tracker.say_goodbye();
  std::this_thread::sleep_for(40ms);
  REQUIRE(tracker.idle(std::chrono::hours(1)));

  {
    const auto work = tracker.begin();
    REQUIRE_FALSE(tracker.idle(std::chrono::hours(1)));
  }
  REQUIRE_FALSE(tracker.idle(std::chrono::hours(1), 1));
  tracker.touch();
  tracker.say_goodbye();
  tracker.touch();
  REQUIRE_FALSE(tracker.idle(std::chrono::hours(1)));
}

TEST_CASE("cancelling a goodbye restores the full quiet period", "[activity][goodbye]") {
  ActivityTracker tracker(10ms);
  tracker.say_goodbye();
  tracker.cancel_goodbye();
  REQUIRE_FALSE(tracker.goodbye_pending());
  std::this_thread::sleep_for(60ms);
  REQUIRE_FALSE(tracker.idle(std::chrono::hours(1)));
}

TEST_CASE(
    "a new connection or request cancels a goodbye, the goodbye request itself does not",
    "[activity][goodbye]"
) {
  ActivityTracker tracker(10ms);
  tracker.say_goodbye();
  tracker.request_started("/bye");
  REQUIRE(tracker.goodbye_pending());

  tracker.request_started("/health");
  REQUIRE_FALSE(tracker.goodbye_pending());

  tracker.say_goodbye();
  tracker.connection_arrived();
  REQUIRE_FALSE(tracker.goodbye_pending());
}
