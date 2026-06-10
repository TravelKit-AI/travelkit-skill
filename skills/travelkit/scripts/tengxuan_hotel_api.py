#!/usr/bin/env python3
"""Local Tengxuan hotel OpenAPI helper for TravelKit skill testing."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import sys
import time
import uuid
import zipfile
from datetime import datetime
from decimal import Decimal
from xml.etree import ElementTree
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


SEARCH_LIST_PATH = "/txjd/hotel/hotelSearchList/json"
PRICE_DETAIL_PATH = "/txjd/hotel/hotelSearchDetail/json"
DEFAULT_CITY_XLSX = "/Users/ricardo/Documents/国内城市.xlsx"
ENV_BASE_URL = "TENGXUAN_HOTEL_BASE_URL"
ENV_AGENCY_CODE = "TENGXUAN_AGENCY_CODE"
ENV_SECURITY_CODE = "TENGXUAN_SECURITY_CODE"
ENV_CITY_XLSX = "TENGXUAN_CITY_XLSX"


class ConfigError(ValueError):
    pass


class ApiError(RuntimeError):
    def __init__(self, message: str, debug_request: dict[str, Any] | None = None):
        super().__init__(message)
        self.debug_request = debug_request


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call Tengxuan hotel list search and price detail APIs."
    )
    parser.add_argument(
        "--city-xlsx",
        default=os.getenv(ENV_CITY_XLSX, DEFAULT_CITY_XLSX),
        help="Path to domestic city xlsx for --city-name lookup.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="HTTP timeout in seconds.",
    )
    parser.add_argument(
        "--rq-identification",
        help="Override rqIdentification; defaults to agency_code plus a UUID.",
    )
    parser.add_argument(
        "--debug-request",
        action="store_true",
        help="Include redacted request details in command output.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    lookup = subparsers.add_parser("city-lookup", help="Look up city codes locally.")
    lookup.add_argument("--city-name", required=True, help="Chinese city name keyword.")

    search = subparsers.add_parser("search-list", help="Search hotel list.")
    add_city_args(search)
    search.add_argument("--check-in-date", required=True)
    search.add_argument("--check-out-date", required=True)
    search.add_argument("--page-index", type=int, default=1)
    search.add_argument("--page-size", type=int, default=10)
    search.add_argument("--sort-type")
    search.add_argument("--country")
    search.add_argument("--keyword")
    search.add_argument("--facilities")
    search.add_argument("--district-code")
    search.add_argument("--price-range-min", type=Decimal)
    search.add_argument("--price-range-max", type=Decimal)
    search.add_argument("--longitude")
    search.add_argument("--latitude")
    search.add_argument("--comment-score", type=float)
    search.add_argument("--business-zone-code")
    search.add_argument("--location-code")
    search.add_argument("--star-rate")
    search.add_argument("--radius", type=int)
    search.add_argument("--brand-code")
    search.add_argument("--sort-by-asc", choices=("true", "false"))
    search.add_argument("--payment-type")
    search.add_argument("--foreign-guest", type=int, choices=(1, 2))
    search.add_argument("--hotel-type", action="append", dest="hotel_types")

    detail = subparsers.add_parser("price-detail", help="Query hotel price detail.")
    add_city_args(detail)
    detail.add_argument("--origin-hotel-id", required=True)
    detail.add_argument("--check-in-date", required=True)
    detail.add_argument("--check-out-date", required=True)
    detail.add_argument("--payment-type", default="Prepay")
    detail.add_argument(
        "--foreign",
        choices=("true", "false"),
        help="Set hotelIdInfo.foreign explicitly; only international hotels require true.",
    )
    detail.add_argument(
        "--omit-foreign",
        action="store_true",
        help="Omit hotelIdInfo.foreign from the detail request.",
    )

    return parser.parse_args()


def add_city_args(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--city-code", help="Tengxuan city code, e.g. C110100.")
    group.add_argument("--city-name", help="City name to resolve from local xlsx.")


def validate_date(value: str, field_name: str) -> datetime:
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ConfigError(f"{field_name} must be YYYY-MM-DD.") from exc


def validate_stay(check_in: str, check_out: str) -> None:
    in_date = validate_date(check_in, "check-in-date")
    out_date = validate_date(check_out, "check-out-date")
    if out_date <= in_date:
        raise ConfigError("check-out-date must be later than check-in-date.")


def read_required_env() -> tuple[str, str, str]:
    missing = [
        name
        for name in (ENV_BASE_URL, ENV_AGENCY_CODE, ENV_SECURITY_CODE)
        if not os.getenv(name)
    ]
    if missing:
        raise ConfigError(
            "Missing required environment variable(s): " + ", ".join(missing)
        )
    return (
        os.environ[ENV_BASE_URL].rstrip("/"),
        os.environ[ENV_AGENCY_CODE],
        os.environ[ENV_SECURITY_CODE],
    )


def normalize_json_value(value: Any) -> Any:
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, dict):
        return {key: normalize_json_value(val) for key, val in value.items()}
    if isinstance(value, list):
        return [normalize_json_value(item) for item in value]
    return value


def compact_json(data: Any) -> str:
    return json.dumps(
        normalize_json_value(data),
        ensure_ascii=False,
        separators=(",", ":"),
    )


def make_payload(
    agency_code: str,
    rq_data: dict[str, Any],
    rq_identification: str | None = None,
) -> dict[str, Any]:
    return {
        "rsIsGzip": True,
        "rqIdentification": rq_identification or f"{agency_code}-{uuid.uuid4().hex}",
        "timeStamp": int(time.time() * 1000),
        "rqData": rq_data,
    }


def sign_body(body: str, security_code: str) -> str:
    return hashlib.md5((body + security_code).encode("utf-8")).hexdigest()


def redact_signature(signature: str) -> str:
    if len(signature) <= 12:
        return "<redacted>"
    return f"{signature[:6]}...{signature[-6:]}"


def call_api(
    path: str,
    rq_data: dict[str, Any],
    timeout: float,
    rq_identification: str | None = None,
    debug_request: bool = False,
) -> dict[str, Any]:
    base_url, agency_code, security_code = read_required_env()
    payload = make_payload(agency_code, rq_data, rq_identification)
    body = compact_json(payload)
    signature = sign_body(body, security_code)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "USERNAME": agency_code,
        "SIGN": signature,
    }
    redacted_debug = build_debug_request(path, payload, headers) if debug_request else None
    request = Request(
        base_url + path,
        data=body.encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read()
            if response.headers.get("Content-Encoding") == "gzip":
                raw = gzip.decompress(raw)
            text = raw.decode("utf-8")
    except HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise ApiError(f"HTTP {exc.code}: {error_body[:500]}", redacted_debug) from exc
    except URLError as exc:
        raise ApiError(f"Network error: {exc.reason}", redacted_debug) from exc

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ApiError(f"Response is not valid JSON: {text[:500]}", redacted_debug) from exc

    rs_code = str(data.get("rsCode", ""))
    if rs_code and rs_code != "0":
        message = data.get("rsMessage") or data.get("msg") or "API returned an error."
        raise ApiError(f"Tengxuan API error {rs_code}: {message}", redacted_debug)
    if redacted_debug:
        data["_debugRequest"] = redacted_debug
    return data


def build_debug_request(
    path: str,
    payload: dict[str, Any],
    headers: dict[str, str],
) -> dict[str, Any]:
    return {
        "path": path,
        "payload": payload,
        "headers": {
            "Content-Type": headers["Content-Type"],
            "Accept": headers["Accept"],
            "USERNAME": headers["USERNAME"],
            "SIGN": redact_signature(headers["SIGN"]),
        },
    }


def city_lookup(city_xlsx: str, city_name: str) -> list[dict[str, str]]:
    path = Path(city_xlsx).expanduser()
    if not path.exists():
        raise ConfigError(f"City xlsx not found: {path}")

    rows = read_first_sheet(path)
    if not rows:
        raise ConfigError("City xlsx is empty.")
    headers = [str(value).strip() if value is not None else "" for value in rows[0]]
    try:
        code_index = headers.index("编码")
        name_index = headers.index("名称")
    except ValueError as exc:
        raise ConfigError("City xlsx must contain 编码 and 名称 columns.") from exc

    keyword = city_name.strip()
    matches: list[dict[str, str]] = []
    for row in rows[1:]:
        code = row[code_index] if code_index < len(row) else None
        name = row[name_index] if name_index < len(row) else None
        if code is None or name is None:
            continue
        code_text = str(code).strip()
        name_text = str(name).strip()
        if keyword == name_text or keyword in name_text:
            matches.append({"cityCode": code_text, "cityName": name_text})
    return matches


def read_first_sheet(path: Path) -> list[list[str]]:
    with zipfile.ZipFile(path) as archive:
        shared_strings = read_shared_strings(archive)
        sheet_name = first_sheet_filename(archive)
        root = ElementTree.fromstring(archive.read(sheet_name))

    namespace = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    rows: list[list[str]] = []
    for row in root.findall(".//x:sheetData/x:row", namespace):
        values: list[str] = []
        for cell in row.findall("x:c", namespace):
            cell_ref = cell.attrib.get("r", "")
            column_index = column_number(cell_ref)
            while len(values) < column_index:
                values.append("")
            values.append(cell_value(cell, shared_strings, namespace))
        rows.append(values)
    return rows


def first_sheet_filename(archive: zipfile.ZipFile) -> str:
    names = archive.namelist()
    for candidate in ("xl/worksheets/sheet1.xml", "xl/worksheets/sheet.xml"):
        if candidate in names:
            return candidate
    matches = sorted(name for name in names if name.startswith("xl/worksheets/sheet"))
    if not matches:
        raise ConfigError("City xlsx has no worksheet XML.")
    return matches[0]


def read_shared_strings(archive: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = ElementTree.fromstring(archive.read("xl/sharedStrings.xml"))
    namespace = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    values: list[str] = []
    for item in root.findall("x:si", namespace):
        parts = [node.text or "" for node in item.findall(".//x:t", namespace)]
        values.append("".join(parts))
    return values


def column_number(cell_ref: str) -> int:
    letters = "".join(ch for ch in cell_ref if ch.isalpha())
    number = 0
    for char in letters:
        number = number * 26 + ord(char.upper()) - ord("A") + 1
    return max(number, 1)


def cell_value(
    cell: ElementTree.Element,
    shared_strings: list[str],
    namespace: dict[str, str],
) -> str:
    value_node = cell.find("x:v", namespace)
    if value_node is None or value_node.text is None:
        inline_node = cell.find(".//x:t", namespace)
        return inline_node.text if inline_node is not None and inline_node.text else ""
    raw_value = value_node.text
    if cell.attrib.get("t") == "s":
        try:
            return shared_strings[int(raw_value)]
        except (IndexError, ValueError):
            return raw_value
    return raw_value


def resolve_city_code(args: argparse.Namespace) -> str:
    if args.city_code:
        return args.city_code
    if not args.city_name:
        raise ConfigError("Either --city-code or --city-name is required.")
    matches = city_lookup(args.city_xlsx, args.city_name)
    exact = [item for item in matches if item["cityName"] == args.city_name]
    selected = exact or matches
    if not selected:
        raise ConfigError(f"No city code found for city name: {args.city_name}")
    if len(selected) > 1:
        preview = ", ".join(
            f"{item['cityName']}={item['cityCode']}" for item in selected[:10]
        )
        raise ConfigError(
            "City name is ambiguous; pass --city-code explicitly. Matches: " + preview
        )
    return selected[0]["cityCode"]


def add_if_present(target: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        target[key] = value


def build_search_data(args: argparse.Namespace) -> dict[str, Any]:
    validate_stay(args.check_in_date, args.check_out_date)
    if args.page_index < 1:
        raise ConfigError("page-index must be >= 1.")
    if args.page_size < 1 or args.page_size > 20:
        raise ConfigError("page-size must be between 1 and 20.")
    if args.radius is not None and (args.radius < 1 or args.radius > 20000):
        raise ConfigError("radius must be between 1 and 20000 meters.")

    data: dict[str, Any] = {
        "pageIndex": args.page_index,
        "pageSize": args.page_size,
        "cityCode": resolve_city_code(args),
        "checkInDate": args.check_in_date,
        "checkOutDate": args.check_out_date,
    }
    field_map = {
        "sortType": args.sort_type,
        "country": args.country,
        "keyword": args.keyword,
        "facilities": args.facilities,
        "districtCode": args.district_code,
        "priceRangeMin": args.price_range_min,
        "priceRangeMax": args.price_range_max,
        "longitude": args.longitude,
        "latitude": args.latitude,
        "commentScore": args.comment_score,
        "businessZoneCode": args.business_zone_code,
        "locationCode": args.location_code,
        "starRate": args.star_rate,
        "radius": args.radius,
        "brandCode": args.brand_code,
        "paymentType": args.payment_type,
        "foreignGuest": args.foreign_guest,
        "hotelTypes": args.hotel_types,
    }
    for key, value in field_map.items():
        add_if_present(data, key, value)
    if args.sort_by_asc is not None:
        data["sortByAsc"] = args.sort_by_asc == "true"
    return data


def build_detail_data(args: argparse.Namespace) -> dict[str, Any]:
    validate_stay(args.check_in_date, args.check_out_date)
    hotel_id_info: dict[str, Any] = {
        "originHotelId": args.origin_hotel_id,
    }
    if args.city_code or args.city_name:
        hotel_id_info["cityCode"] = resolve_city_code(args)
    if not args.omit_foreign and args.foreign is not None:
        hotel_id_info["foreign"] = args.foreign == "true"
    return {
        "checkInDate": args.check_in_date,
        "checkOutDate": args.check_out_date,
        "hotelIdInfo": hotel_id_info,
        "paymentType": args.payment_type,
    }


def emit(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, default=str))


def main() -> int:
    args = parse_args()
    try:
        if args.command == "city-lookup":
            emit({"ok": True, "matches": city_lookup(args.city_xlsx, args.city_name)})
            return 0
        if args.command == "search-list":
            data = call_api(
                SEARCH_LIST_PATH,
                build_search_data(args),
                args.timeout,
                args.rq_identification,
                args.debug_request,
            )
            emit({"ok": True, "response": data})
            return 0
        if args.command == "price-detail":
            data = call_api(
                PRICE_DETAIL_PATH,
                build_detail_data(args),
                args.timeout,
                args.rq_identification,
                args.debug_request,
            )
            emit({"ok": True, "response": data})
            return 0
    except ConfigError as exc:
        emit({"ok": False, "error": str(exc)})
        return 2
    except ApiError as exc:
        output: dict[str, Any] = {"ok": False, "error": str(exc)}
        if exc.debug_request:
            output["debugRequest"] = exc.debug_request
        emit(output)
        return 2
    return 2


if __name__ == "__main__":
    sys.exit(main())
