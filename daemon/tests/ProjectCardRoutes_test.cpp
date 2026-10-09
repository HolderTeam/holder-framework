#include "api/routes/CardRoutes.h"
#include "api/routes/ProjectCardRoutes.h"
#include "api/support/HttpQuery.h"
#include "card/TagRepo.h"
#include "http_test_helpers.h"
#include <unordered_map>

namespace {
namespace http = boost::beast::http;
using Params = std::unordered_map<std::string, std::string>;
auto getter(Params params) {
  return [params](const std::string& name) {
    const auto it = params.find(name);
    return it == params.end() ? std::string{} : it->second;
  };
}
} // namespace

TEST_CASE(
    "Project card collection pages combine filters and preserve display behaviour",
    "[card-pages]"
) {
  const auto dir = holder::test::make_temp_dir();
  auto db = holder::test::open_db_with_schema(dir / "holder.db");
  holder::test::create_project(db, "p", (dir / "repo").string());
  holder::test::create_project(db, "other", (dir / "other").string());
  holder::index::FtsIndexer fts(db);
  holder::card::CardStore store(db, &fts);
  const std::string first = "00000000-0000-4000-8000-000000000001";
  const std::string second = "00000000-0000-4000-8000-000000000002";
  const std::string third = "00000000-0000-4000-8000-000000000003";
  const std::string deleted = "00000000-0000-4000-8000-000000000004";
  const std::string foreign = "00000000-0000-4000-8000-000000000005";
  holder::test::create_card_fixture(store, first, "p", "one", "one\n#work", 10);
  holder::test::create_card_fixture(store, second, "p", "two", "two\n#work", 20, first);
  holder::test::create_card_fixture(store, third, "p", "three", "three\n#work", 20, first);
  holder::test::create_card_fixture(store, deleted, "p", "deleted", "deleted\n#work", 40);
  holder::test::create_card_fixture(store, foreign, "other", "foreign", "foreign\n#work", 50);
  store.trash(deleted, 60);
  auto call = [&](Params params,
                  std::string path = "/projects/p/cards",
                  http::verb method = http::verb::get) {
    http::request<http::string_body> req{method, path, 11};
    http::response<http::string_body> res;
    REQUIRE(holder::api::routes::handle_project_card_routes(path, req, res, db, getter(params)));
    return std::make_pair(res.result(), nlohmann::json::parse(res.body()));
  };
  auto [status, payload] = call({{"limit", "2"}});
  REQUIRE(status == http::status::ok);
  REQUIRE(payload["data"]["items"].size() == 2);
  CHECK(payload["data"]["items"][0]["card_id"] == first);
  CHECK(payload["data"]["items"][1]["card_id"] == second);
  const auto cursor = payload["data"]["next_cursor"].get<std::string>();
  auto [next_status, next] = call({{"limit", "2"}, {"cursor", cursor}});
  REQUIRE(next_status == http::status::ok);
  REQUIRE(next["data"]["items"].size() == 1);
  CHECK(next["data"]["items"][0]["card_id"] == third);
  CHECK(next["data"]["next_cursor"].is_null());
  CHECK(call({{"limit", "3"}}).second["data"]["next_cursor"].is_null());
  CHECK(call({{"cursor", cursor}}, "/projects/other/cards").first == http::status::bad_request);
  for (const auto& change :
       Params{{"tag", "work"}, {"parent", "roots"}, {"order", "updated_desc"}}) {
    Params params{change, {"cursor", cursor}};
    CHECK(call(params).first == http::status::bad_request);
  }
  Params filtered{{"tag", "Work"}, {"parent", first}, {"order", "updated_desc"}, {"limit", "1"}};
  auto page = call(filtered).second["data"];
  REQUIRE(page["items"].size() == 1);
  CHECK(page["items"][0]["card_id"] == third);
  filtered["cursor"] = page["next_cursor"].get<std::string>();
  filtered["tag"] = "WORK";
  page = call(filtered).second["data"];
  REQUIRE(page["items"].size() == 1);
  CHECK(page["items"][0]["card_id"] == second);
  CHECK(page["next_cursor"].is_null());
  CHECK(call({{"tag", "work"}, {"parent", "roots"}}).second["data"]["items"].size() == 1);
  CHECK(call({}).second["data"]["items"].size() == 3);
  CHECK(call({{"tag", "work"}}).second["data"]["items"].size() == 3);
  CHECK(call({{"tag", "WORK"}}).second["data"] == call({{"tag", "work"}}).second["data"]);
  CHECK(call({{"tag", "missing"}}).second["data"]["items"].empty());
  for (const auto& limit : {"0", "5001", "bad", "2junk", "-1", "99999999999999999"})
    CHECK(call({{"limit", limit}}).first == http::status::bad_request);
  for (const auto& bad :
       Params{{"cursor", "bad"}, {"order", "bad"}, {"parent", "bad"}, {"tag", "#work"}})
    CHECK(call({bad}).first == http::status::bad_request);
  CHECK(call({}, "/projects/missing/cards").first == http::status::not_found);
  CHECK(call({}, "/projects/p/cards", http::verb::post).first == http::status::method_not_allowed);

  // The display endpoint retains its original hierarchy, recent mode and tag precedence.
  auto display = [&](Params params) {
    http::request<http::string_body> req{http::verb::get, "/cards", 11};
    http::response<http::string_body> res;
    params["project_id"] = "p";
    REQUIRE(
        holder::api::routes::handle_card_routes(
            "/cards",
            req,
            res,
            db,
            &store,
            &fts,
            [] {
              return "unused";
            },
            getter(params)
        )
    );
    return std::make_pair(res.result(), nlohmann::json::parse(res.body()));
  };
  CHECK(display({}).second["data"].size() == 1);
  CHECK(display({{"parent_card_id", first}}).second["data"].size() == 2);
  CHECK(display({{"tag", "work"}, {"parent_card_id", first}}).second["data"].size() == 3);
  CHECK(display({{"view", "recent"}, {"limit", "2junk"}}).second["data"].size() == 2);
  CHECK(display({{"view", "all"}}).first == http::status::bad_request);
  CHECK(display({{"after_card_id", third}}).second["data"].size() == 1);

  // Real trash leaves children live: flat pages must still expose them.
  store.trash(first, 70);
  page = call({{"limit", "1"}}).second["data"];
  REQUIRE(page["items"].size() == 1);
  CHECK(page["items"][0]["card_id"] == second);
  REQUIRE(page["next_cursor"].is_string());
  page = call({{"limit", "1"}, {"cursor", page["next_cursor"].get<std::string>()}}).second["data"];
  REQUIRE(page["items"].size() == 1);
  CHECK(page["items"][0]["card_id"] == third);
  CHECK(page["next_cursor"].is_null());
  CHECK(call({{"parent", "roots"}}).second["data"]["items"].empty());
  CHECK(call({{"parent", first}}).second["data"]["items"].size() == 2);
}

TEST_CASE("Project card routes decline unrelated paths", "[card-pages]") {
  holder::platform::Db db;
  for (const auto* path :
       {"/cards",
        "/projects/p",
        "/projects/cards",
        "/projects/p/tags",
        "/projects/p/cards/id",
        "/projects//cards"}) {
    http::request<http::string_body> req{http::verb::get, path, 11};
    http::response<http::string_body> res;
    CHECK_FALSE(holder::api::routes::handle_project_card_routes(path, req, res, db, getter({})));
  }
}

TEST_CASE("Project query values decode once and match complete parameter names", "[http-query]") {
  using holder::api::support::decoded_query_param_value;
  CHECK(
      decoded_query_param_value("name=Collection+integration", "name") == "Collection integration"
  );
  CHECK(decoded_query_param_value("name=caf%C3%A9%20%26%2B", "name") == "café &+");
  CHECK(decoded_query_param_value("name=%252B", "name") == "%2B");
  CHECK(decoded_query_param_value("other_name=wrong&name=right", "name") == "right");
}
