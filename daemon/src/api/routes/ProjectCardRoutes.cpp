#include "api/routes/ProjectCardRoutes.h"
#include "api/support/HttpResponses.h"
#include "card/CardRepo.h"
#include "card/TagExtractor.h"
#include "identity/Uuid.h"
#include "project/ProjectRepo.h"

#include <charconv>
#include <limits>
#include <nlohmann/json.hpp>
#include <stdexcept>
#include <string_view>

namespace holder::api::routes {
namespace {
namespace http = boost::beast::http;

std::string encode_cursor(const nlohmann::json& value) {
  constexpr char hex[] = "0123456789abcdef";
  std::string result;
  for (const char character : value.dump()) {
    const auto byte = static_cast<unsigned char>(character);
    result += hex[byte >> 4];
    result += hex[byte & 15];
  }
  return result;
}

nlohmann::json decode_cursor(const std::string& value) {
  if (value.empty() || value.size() > 8192 || value.size() % 2)
    throw std::invalid_argument("Invalid cursor.");
  const auto digit = [](char c) -> int {
    if (c >= '0' && c <= '9') return c - '0';
    if (c >= 'a' && c <= 'f') return c - 'a' + 10;
    throw std::invalid_argument("Invalid cursor.");
  };
  std::string decoded;
  for (std::size_t i = 0; i < value.size(); i += 2)
    decoded += static_cast<char>((digit(value[i]) << 4) | digit(value[i + 1]));
  return nlohmann::json::parse(decoded);
}

bool boolean_param(const std::string& raw) {
  if (raw.empty() || raw == "false") return false;
  if (raw == "true") return true;
  throw std::invalid_argument("include_deleted must be true or false.");
}
} // namespace

bool handle_project_card_routes(
    const std::string& path,
    const http::request<http::string_body>& req,
    http::response<http::string_body>& res,
    holder::platform::Db& db,
    const std::function<std::string(const std::string&)>& param_get
) {
  constexpr std::string_view prefix = "/projects/";
  constexpr std::string_view suffix = "/cards";
  if (!path.starts_with(prefix) || !path.ends_with(suffix) ||
      path.size() <= prefix.size() + suffix.size())
    return false;
  const auto project_id = path.substr(prefix.size(), path.size() - prefix.size() - suffix.size());
  if (project_id.empty() || project_id.find('/') != std::string::npos) return false;
  if (req.method() != http::verb::get) {
    res =
        support::error_response(http::status::method_not_allowed, "method_not_allowed", "Use GET.");
    return true;
  }
  try {
    holder::card::CardPageQuery query;
    int limit = 200;
    const auto limit_raw = param_get("limit");
    if (!limit_raw.empty()) {
      const auto [end, error] =
          std::from_chars(limit_raw.data(), limit_raw.data() + limit_raw.size(), limit);
      if (error != std::errc{} || end != limit_raw.data() + limit_raw.size() || limit < 1 ||
          limit > 5000)
        throw std::invalid_argument("limit must be an integer from 1 to 5000.");
    }
    const auto tag = param_get("tag");
    if (!tag.empty()) {
      if (!holder::core::is_valid_tag(tag) || tag != holder::core::normalize_tag(tag))
        throw std::invalid_argument("tag must be normalized without a leading #.");
      query.tag = tag;
    }
    const auto parent = param_get("parent");
    if (!parent.empty()) {
      if (parent != "roots" && !holder::identity::is_valid_uuid(parent))
        throw std::invalid_argument("parent must be roots or a card UUID.");
      query.parent_card_id = parent == "roots" ? "" : parent;
    }
    query.include_deleted = boolean_param(param_get("include_deleted"));
    const auto order_raw = param_get("order");
    const auto order = order_raw.empty() ? "card_id_asc" : order_raw;
    if (order == "updated_desc")
      query.order = holder::card::CardPageOrder::UpdatedDesc;
    else if (order != "card_id_asc")
      throw std::invalid_argument("Invalid order.");
    const nlohmann::json scope = {
        {"project_id", project_id},
        {"tag", tag},
        {"parent", parent},
        {"include_deleted", query.include_deleted},
        {"order", order}
    };
    const auto cursor = param_get("cursor");
    if (!cursor.empty()) {
      const auto decoded = decode_cursor(cursor);
      if (decoded.at("version") != 1 || decoded.at("query") != scope)
        throw std::invalid_argument("Cursor belongs to a different query.");
      const auto id = decoded.at("card_id").get<std::string>();
      const auto& timestamp = decoded.at("updated_at");
      if (id.empty() || !timestamp.is_number_integer() ||
          (timestamp.is_number_unsigned() &&
           timestamp.get<unsigned long long>() >
               static_cast<unsigned long long>(std::numeric_limits<long long>::max())))
        throw std::invalid_argument("Invalid cursor.");
      query.cursor = holder::card::CardPageCursor{id, timestamp.get<long long>()};
    }
    holder::project::ProjectRepo projects(db);
    if (!projects.get(project_id).has_value()) {
      res = support::error_response(http::status::not_found, "not_found", "Project not found.");
      return true;
    }
    holder::card::CardRepo cards(db);
    auto rows = cards.list_collection_page(project_id, query, limit + 1);
    nlohmann::json next_cursor = nullptr;
    if (rows.size() > static_cast<std::size_t>(limit)) {
      rows.resize(static_cast<std::size_t>(limit));
      next_cursor = encode_cursor(
          {{"version", 1},
           {"query", scope},
           {"card_id", rows.back().card_id},
           {"updated_at", rows.back().updated_at}}
      );
    }
    auto items = nlohmann::json::array();
    for (const auto& card : rows) {
      items.push_back(
          {{"card_id", card.card_id},
           {"project_id", card.project_id},
           {"title", card.title},
           {"rel_path", card.rel_path},
           {"sort_key", card.sort_key},
           {"created_at", card.created_at},
           {"updated_at", card.updated_at},
           {"parent_card_id",
            card.parent_card_id.has_value() ? nlohmann::json(*card.parent_card_id)
                                            : nlohmann::json(nullptr)},
           {"deleted_at",
            card.deleted_at.has_value() ? nlohmann::json(*card.deleted_at) : nlohmann::json(nullptr)
           }}
      );
    }
    res = support::json_response(
        http::status::ok,
        {{"ok", true},
         {"data", {{"items", std::move(items)}, {"next_cursor", std::move(next_cursor)}}}}
    );
  } catch (const std::invalid_argument& ex) {
    res = support::error_response(http::status::bad_request, "bad_request", ex.what());
  } catch (const nlohmann::json::exception&) {
    res = support::error_response(http::status::bad_request, "bad_request", "Invalid cursor.");
  } catch (const std::exception& ex) {
    res = support::error_response(http::status::internal_server_error, "error", ex.what());
  }
  return true;
}
} // namespace holder::api::routes
