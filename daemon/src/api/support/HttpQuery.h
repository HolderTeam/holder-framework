#pragma once

#include <string>

namespace holder::api::support {

inline std::string query_param_value(const std::string& query_string, const std::string& key) {
  std::size_t start = 0;
  while (start < query_string.size()) {
    const auto end = query_string.find('&', start);
    const auto field = query_string.substr(start, end == std::string::npos ? end : end - start);
    const auto equals = field.find('=');
    if (equals != std::string::npos && field.substr(0, equals) == key) {
      return field.substr(equals + 1);
    }
    if (end == std::string::npos) break;
    start = end + 1;
  }
  return {};
}

inline std::string decoded_query_param_value(
    const std::string& query_string,
    const std::string& key
) {
  const auto raw = query_param_value(query_string, key);
  const auto hex = [](char value) -> int {
    if (value >= '0' && value <= '9') return value - '0';
    if (value >= 'a' && value <= 'f') return value - 'a' + 10;
    if (value >= 'A' && value <= 'F') return value - 'A' + 10;
    return -1;
  };
  std::string result;
  result.reserve(raw.size());
  for (std::size_t i = 0; i < raw.size(); ++i) {
    if (raw[i] == '%' && i + 2 < raw.size() && hex(raw[i + 1]) >= 0 && hex(raw[i + 2]) >= 0) {
      result.push_back(static_cast<char>(hex(raw[i + 1]) * 16 + hex(raw[i + 2])));
      i += 2;
    } else {
      result.push_back(raw[i] == '+' ? ' ' : raw[i]);
    }
  }
  return result;
}

} // namespace holder::api::support
