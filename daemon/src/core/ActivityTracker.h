#pragma once

#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstddef>
#include <cstdint>
#include <string_view>

namespace holder::core {

// Records whether the daemon is doing anything, so a daemon started with --idle-exit can
// stop itself once nothing needs it.
//
// Work holds a Scope for as long as it runs: executing or writing a request (which
// includes a streaming AI run), a sync pass, a model download, a resource import. A Scope
// releases itself on every path, including exceptions, so it cannot leak. touch() records
// a moment of activity, such as a connection arriving.
//
// The daemon is idle when no Scope is held, no event stream is open (the caller supplies
// that count), and nothing has happened for the quiet period. The quiet period also covers
// the brief gaps while a request moves between worker queues.
//
// A client that is leaving can say goodbye (POST /bye). That is a hint, not a command: it only
// shortens the quiet period to a short grace, and only for as long as nothing new happens. Work,
// open streams and activity still count, and a new connection or any other request cancels it.
class ActivityTracker {
 public:
  using Clock = std::chrono::steady_clock;

  class Scope {
   public:
    Scope() = default;
    Scope(Scope&& other) noexcept
        : tracker_(other.tracker_) {
      other.tracker_ = nullptr;
    }
    Scope& operator=(Scope&& other) noexcept {
      if (this != &other) {
        release();
        tracker_ = other.tracker_;
        other.tracker_ = nullptr;
      }
      return *this;
    }
    Scope(const Scope&) = delete;
    Scope& operator=(const Scope&) = delete;
    ~Scope() { release(); }

   private:
    friend class ActivityTracker;
    explicit Scope(ActivityTracker* tracker) noexcept
        : tracker_(tracker) {}
    void release() noexcept {
      if (tracker_ != nullptr) {
        tracker_->end();
        tracker_ = nullptr;
      }
    }
    ActivityTracker* tracker_ = nullptr;
  };

  static constexpr Clock::duration kDefaultGoodbyeGrace = std::chrono::seconds(3);

  explicit ActivityTracker(Clock::duration goodbye_grace = kDefaultGoodbyeGrace) noexcept
      : goodbye_grace_(goodbye_grace) {
    touch();
  }

  // Work starts now and lasts until the returned Scope is destroyed.
  [[nodiscard]] Scope begin() noexcept {
    active_.fetch_add(1, std::memory_order_acq_rel);
    touch();
    return Scope(this);
  }

  void touch() noexcept {
    last_activity_ticks_.store(Clock::now().time_since_epoch().count(), std::memory_order_release);
  }

  std::size_t active() const noexcept { return active_.load(std::memory_order_acquire); }

  // Time since work last started or finished, or since touch() was last called.
  Clock::duration quiet_for() const noexcept {
    const Clock::duration since_epoch(last_activity_ticks_.load(std::memory_order_acquire));
    return Clock::now().time_since_epoch() - since_epoch;
  }

  bool idle(Clock::duration quiet, std::size_t open_streams = 0) const noexcept {
    const auto required = goodbye_.load(std::memory_order_acquire) ? std::min(quiet, goodbye_grace_)
                                                                   : quiet;
    return active() == 0 && open_streams == 0 && quiet_for() >= required;
  }

  // A client says it is leaving. Counts as activity itself, so the grace starts from here.
  void say_goodbye() noexcept {
    goodbye_.store(true, std::memory_order_release);
    touch();
  }

  void cancel_goodbye() noexcept { goodbye_.store(false, std::memory_order_release); }

  bool goodbye_pending() const noexcept { return goodbye_.load(std::memory_order_acquire); }

  // Something new arrived, so whoever said goodbye was not the last client.
  void connection_arrived() noexcept {
    cancel_goodbye();
    touch();
  }

  // A request is about to run. Every request but the goodbye itself cancels a goodbye.
  void request_started(std::string_view path) noexcept {
    if (path != "/bye") cancel_goodbye();
  }

 private:
  void end() noexcept {
    active_.fetch_sub(1, std::memory_order_acq_rel);
    touch();
  }

  Clock::duration goodbye_grace_;
  std::atomic<bool> goodbye_{false};
  std::atomic<std::size_t> active_{0};
  std::atomic<Clock::rep> last_activity_ticks_{0};
};

// The tracker for this process. Callers anywhere in the daemon can record work without
// the tracker being passed through every layer.
inline ActivityTracker& activity() noexcept {
  static ActivityTracker tracker;
  return tracker;
}

} // namespace holder::core
