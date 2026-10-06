#include "api/support/PathDiscovery.h"

#include "http_test_helpers.h"

#include <catch2/catch_test_macros.hpp>

#include <filesystem>
#include <fstream>
#include <string>

namespace {

// Runs with the working directory changed, and puts it back afterwards.
class WorkingDirectory {
 public:
  explicit WorkingDirectory(const std::filesystem::path& directory)
      : previous_(std::filesystem::current_path()) {
    std::filesystem::current_path(directory);
  }
  WorkingDirectory(const WorkingDirectory&) = delete;
  WorkingDirectory& operator=(const WorkingDirectory&) = delete;
  ~WorkingDirectory() {
    std::error_code ignored;
    std::filesystem::current_path(previous_, ignored);
  }

 private:
  std::filesystem::path previous_;
};

void write_file(const std::filesystem::path& path, const std::string& text) {
  std::filesystem::create_directories(path.parent_path());
  std::ofstream(path) << text;
}

} // namespace

TEST_CASE(
    "PathDiscovery content_type_for_extension covers image/text and fallback mappings",
    "[path_discovery]"
) {
  using holder::api::support::content_type_for_extension;

  REQUIRE(content_type_for_extension(".svg") == "image/svg+xml");
  REQUIRE(content_type_for_extension(".png") == "image/png");
  REQUIRE(content_type_for_extension(".ico") == "image/x-icon");
  REQUIRE(content_type_for_extension(".txt") == "text/plain; charset=utf-8");
  REQUIRE(content_type_for_extension(".bin") == "application/octet-stream");
}

TEST_CASE("the contract is found in api/ beside daemon/ when run from a source tree", "[path_discovery]") {
  const auto root = holder::test::make_temp_dir();
  std::filesystem::create_directories(root / "daemon");
  write_file(root / "api" / "openapi.yaml", "openapi: 3.0.3\n");
  const holder::test::EnvGuard no_override("HOLDER_OPENAPI_PATH", std::nullopt);
  const WorkingDirectory in_daemon(root / "daemon");

  const auto found = holder::api::support::find_openapi_path();

  REQUIRE(found.has_value());
  REQUIRE(std::filesystem::equivalent(*found, root / "api" / "openapi.yaml"));
}

TEST_CASE("a contract in the working directory wins over the one in api/", "[path_discovery]") {
  const auto root = holder::test::make_temp_dir();
  write_file(root / "api" / "openapi.yaml", "from api\n");
  write_file(root / "daemon" / "openapi.yaml", "from the build directory\n");
  const holder::test::EnvGuard no_override("HOLDER_OPENAPI_PATH", std::nullopt);
  const WorkingDirectory in_daemon(root / "daemon");

  const auto found = holder::api::support::find_openapi_path();

  REQUIRE(found.has_value());
  REQUIRE(std::filesystem::equivalent(*found, root / "daemon" / "openapi.yaml"));
}

TEST_CASE("HOLDER_OPENAPI_PATH wins over everything", "[path_discovery]") {
  const auto root = holder::test::make_temp_dir();
  write_file(root / "api" / "openapi.yaml", "from api\n");
  write_file(root / "elsewhere.yaml", "from the override\n");
  const holder::test::EnvGuard override_path("HOLDER_OPENAPI_PATH", (root / "elsewhere.yaml").string());
  std::filesystem::create_directories(root / "daemon");
  const WorkingDirectory in_daemon(root / "daemon");

  const auto found = holder::api::support::find_openapi_path();

  REQUIRE(found.has_value());
  REQUIRE(std::filesystem::equivalent(*found, root / "elsewhere.yaml"));
}

