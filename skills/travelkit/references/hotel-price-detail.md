# hotel-price-detail ref

Use `scripts/tengxuan_hotel_api.py price-detail` for local testing of Tengxuan hotel price detail.

## Inputs

Required:

- `originHotelId`, usually from hotel list search results.
- `checkInDate` and `checkOutDate` in `YYYY-MM-DD`; check-out must be later than check-in.
- `paymentType`; the script defaults to `Prepay`.

Optional:

- `cityCode` or `cityName` for `hotelIdInfo.cityCode`.
- `--foreign` for international hotel detail requests.

## Credentials

The script reads credentials from environment variables:

- `TENGXUAN_HOTEL_BASE_URL`
- `TENGXUAN_AGENCY_CODE`
- `TENGXUAN_SECURITY_CODE`

Never print, store, or ask the user to paste the security code in normal chat.

## Example

```bash
skills/travelkit/scripts/tengxuan_hotel_api.py price-detail \
  --origin-hotel-id H5743355404436509450 \
  --city-name 北京 \
  --check-in-date 2026-06-01 \
  --check-out-date 2026-06-02 \
  --payment-type Prepay
```

## Display

Summarize successful results with hotel name/address, room name, bed/window/floor, rate plan, price, nightly prices, breakfast count, stock, payment type, instant confirmation, cancellation rule, and `shoppingCode` when returned.

Do not expose request signatures, raw headers, security code, or full raw JSON unless the user explicitly asks for debugging output.
