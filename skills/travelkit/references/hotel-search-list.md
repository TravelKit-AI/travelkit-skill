# hotel-search-list ref

Use `scripts/tengxuan_hotel_api.py search-list` for local testing of Tengxuan hotel list search.

## Inputs

Required:

- `checkInDate` and `checkOutDate` in `YYYY-MM-DD`; check-out must be later than check-in.
- One of:
  - `cityCode`, e.g. `C110100`
  - `cityName`, resolved locally from `国内城市.xlsx`

Optional filters supported by the script include keyword, page index/size, sort type, price range, district, business zone, location, star rate, brand, payment type, foreign guest, hotel type, and coordinate/radius.

## Local Data

For `--city-name`, the script reads the workbook path from `--city-xlsx`, then `TENGXUAN_CITY_XLSX`, then `/Users/ricardo/Documents/国内城市.xlsx`. The workbook must contain `编码` and `名称` columns.

If multiple city names match, ask the user to choose a specific `cityCode`; do not guess.

## Credentials

The script reads credentials from environment variables:

- `TENGXUAN_HOTEL_BASE_URL`
- `TENGXUAN_AGENCY_CODE`
- `TENGXUAN_SECURITY_CODE`

Never print, store, or ask the user to paste the security code in normal chat.

## Example

```bash
skills/travelkit/scripts/tengxuan_hotel_api.py search-list \
  --city-name 北京 \
  --check-in-date 2026-06-01 \
  --check-out-date 2026-06-02 \
  --keyword 丽思 \
  --page-size 5
```

## Display

Summarize successful results as a compact hotel list with hotel name, city/district, address, star/score, lowest price, and hotel id. Do not expose request signatures, raw headers, security code, or full raw JSON unless the user explicitly asks for debugging output.
