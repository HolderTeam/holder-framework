#pragma once

#include "card/CardStore.h"
#include "platform/Db.h"
#include <boost/beast/http.hpp>
#include <functional>
#include <string>

namespace holder::api::routes {
bool handle_project_card_routes(
    const std::string& path,
    const boost::beast::http::request<boost::beast::http::string_body>& req,
    boost::beast::http::response<boost::beast::http::string_body>& res,
    holder::platform::Db& db,
    const std::function<std::string(const std::string&)>& param_get,
    // Reads card bodies for include_content pages; metadata pages need only the database.
    holder::card::CardStore* card_store = nullptr
);
} // namespace holder::api::routes
