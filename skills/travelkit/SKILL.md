---
name: travelkit
description: TravelKit flight booking and management skill. Use for flight search, pricing, real-time price verification, order creation, payment, cancellation, refund, change, itinerary download, and TravelKit MCP integration policy. Always use this skill for TravelKit flight lifecycle tasks.
---

# TravelKit Flight Skill

Use the smallest relevant reference file for the user's current task. Keep consumer replies in Simplified Chinese unless the user requests another language.

## Fast Routing

| User intent | Read | Tool(s) |
|---|---|---|
| Search or compare flights | [flight-search](references/flight-search.md) | `flight_search` |
| Price a known flight number | [flight-pricing](references/flight-pricing.md) | `flight_pricing` |
| User selects a search option | [flight-verify](references/flight-verify.md) | `flight_verify_solution` |
| Create an order after verified price | [flight-create-order](references/flight-create-order.md) | `flight_create_order` |
| Pay an order | [flight-pay-order](references/flight-pay-order.md) | `flight_pay_order` |
| Look up orders | [flight-order-lookup](references/flight-order-lookup.md) | `flight_order_detail`, `flight_order_detail_by_external_id`, `flight_order_list` |
| Cancel an order | [flight-cancel](references/flight-cancel.md) | `flight_cancel_order` |
| Refund | [flight-refund](references/flight-refund.md) | `flight_refund_quote`, `flight_refund_money_search`, `flight_refund_request`, `flight_refund_confirm` |
| Change flight | [flight-change](references/flight-change.md) | `flight_change_search`, `flight_change_request` |
| Download itinerary | [flight-itinerary](references/flight-itinerary.md) | `flight_download_itinerary` |
| Integration/config questions | [mcp-connection](references/mcp-connection.md) | N/A |

## Core Rules

- Search before booking; verify real-time price before collecting passenger information or creating an order.
- Never expose internal fields such as `solutionId`, `orderKey`, confirmation flags, raw MCP JSON, API keys, `passengerIds`, `segmentIds`, or idempotency keys to normal users.
- Never invent missing tool data. If baggage, refund/change policy, ticketing, or deadline data is absent, say it was not returned.
- Search/pricing/verify/order lookup/itinerary/change-search/refund quote are read operations and can be called as needed.
- Create order, pay, cancel, refund request/confirm, and change request are write operations; get explicit user confirmation for the exact action first.
- Search stage collects only route, dates, passenger counts, cabin, and preferences. Collect ID/passport/phone/email only after price verification succeeds and the user confirms they want to proceed.

## Search Quick Path

- Convert relative dates to `YYYY-MM-DD` using the current date/timezone.
- Defaults: 1 adult, economy, no airline restriction, no baggage guarantee unless requested.
- If the user specifies an airport (for example PEK/北京首都), treat it as a hard airport-level constraint. Pass the airport code to `flight_search` when possible, then filter returned `displayOptions` by actual route before showing results.
- If the user specifies include/exclude airlines, pass `includeAirlines` or `excludeAirlines` when possible, then filter by IATA airline code before showing results.
- For multiple outbound/return date choices where the user wants the cheapest feasible combination, search the candidate one-way dates in parallel and combine locally. Use multi-journey round-trip search only when the user explicitly needs one round-trip fare/order or the supplier requires it.
- Show only user-facing flight facts: flight number, route/terminals, times, stops, cabin, and price. Keep option labels mapped to internal IDs privately for later verification.

## Write Confirmation

Before any write tool, summarize the business action in normal language and wait for explicit confirmation. After confirmation, set required internal confirmation fields in the tool call without asking users about production or technical flags. Read [confirmation-rules](references/confirmation-rules.md) for operation-specific details.

## Shared References

- Tool category details: [tool-categories](references/tool-categories.md)
- Hidden fields: [hidden-fields](references/hidden-fields.md)
- Output rules: [output-rules](references/output-rules.md)
