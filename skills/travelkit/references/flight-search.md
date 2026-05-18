# flight-search ref

Use `flight_search` when the user describes a route/date preference and needs available flight options. If the user provides a complete flight number + airports + date + cabin, use `flight_pricing` instead.

## Search Inputs

Collect only:

- origin/destination city or airport
- departure date, and return date if any
- for multi-city / 多段行程 requests, collect each leg's origin, destination, and departure date; `flight_search` supports up to 5 `journeys[]`
- adult/child/infant counts; default to 1 adult
- cabin class; default to economy
- preferences: nonstop, baggage, airline include/exclude, price cap, departure/arrival time window, max duration

Do not collect passenger ID/passport, phone, email, birthday, or name during search. Convert relative dates to `YYYY-MM-DD` using the current date/timezone. If route or date is missing, ask briefly.

## Tool Use

- Pass airport-level constraints directly in `journeys[].origin` / `journeys[].destination` when the user specifies an airport such as PEK, PKX, PVG, or SHA.
- Pass airline constraints with `includeAirlines` or `excludeAirlines` when the user clearly specifies airlines.
- Use `maxSegments: 1` for "直飞/不要转机"; otherwise omit unless the user sets a stop limit.
- For continuous multi-city / 多段行程 requests, use one `flight_search` call with one `journeys[]` entry per leg, up to 5 legs. For example, "北京到上海再到广州" becomes `BJS -> SHA` and `SHA -> CAN` as two journeys with their own departure dates.
- For multiple outbound/return date choices and "cheapest combination" style requests, search each candidate one-way date in parallel and combine locally by total price after filtering. Use multi-journey round-trip search only when the user explicitly wants a single round-trip fare/order or supplier round-trip pricing is required.

## Mandatory Post-Filtering

Filter `data.displayOptions` before showing anything:

- Airport constraints are hard constraints. Match by actual route IATA code, not by city code alone. If the user specified PEK, exclude PKX and any option whose route cannot confirm PEK.
- For outbound airport constraints, match the first route departure. For arrival airport constraints, match the last route arrival. Apply this per journey for round-trip or multi-city.
- Airline constraints match IATA airline code in every displayed flight. Exclude unclear code-share options if they cannot be confirmed.
- If filtering leaves no options, do not show same-city alternatives automatically. Ask whether to relax the airport or airline constraint.
- Never expose filtered-out internal IDs, `solutionId`, raw JSON, or MCP fields.

## Ranking And Recommendation

- Default display: 5 options after filtering when at least 5 are available. If fewer than 5 remain, show all available options and say only these matched the constraints.
- For the user's requested objective, rank first by hard constraints, then price, then time-window comfort, then duration/stops.
- Mark one recommendation below the table and briefly state why, such as cheapest, fastest, least hassle, or better timing.
- If a cheaper option violates a soft preference (for example too early/late), mention it separately only when useful.

## Display Format

Use Markdown table for normal chat channels:

```markdown
| 选项 | 航班 | 行程 | 时间 | 舱位 | 价格 |
|---|---|---|---|---|---:|
| 1 | CA1714 | 北京首都 PEK T3 → 杭州 HGH T4 | 12:30-14:40｜直飞约2小时10分 | 经济舱 | ¥790 |
```

Rules:

- Exactly 6 columns: `选项 | 航班 | 行程 | 时间 | 舱位 | 价格`.
- Option labels are plain numbers only; keep recommendation text outside the table.
- The `航班` column shows only complete flight numbers such as `CA1714`, without Chinese or English airline names.
- For multi-segment flights, list every returned complete flight number and every segment in the same row, and include total duration/stops. If segment or flight number data is absent, say the tool did not return it; do not say there is no segment.
- The `行程` column for multi-segment flights keeps the route chain, for example `北京首都 PEK T3 → 香港 HKG → 曼谷 BKK`.
- The `时间` column for direct flights keeps the compact range plus duration, for example `18:55-23:00｜直飞约5小时05分`.
- The `时间` column for multi-segment / 中转 flights must show each segment's departure and arrival time, not only the first departure and final arrival. Use this format: `PEK→HKG 07:25-10:55；HKG→BKK 14:30-16:30｜中转1次约10小时05分`.
- For cross-date segments, show the date on the segment time itself, for example `PEK→HKG 07:25-10:55；HKG→BKK 5/20 22:15-5/21 00:10｜中转1次约17小时45分`.
- If a segment's departure or arrival time is not returned, do not invent it; show that segment as `{origin}→{destination} 时间未返回` and still show all other returned segment times.
- Show cross-date arrivals with the arrival date, for example `23:50-6/17 09:40`.
- Do not add baggage as a table column. Mention baggage only if the user asks or the verified result returns it.
- If only IATA codes are returned, expand common airports when known; otherwise keep the code and do not invent names.

## Required Search Footer

End search results with this meaning, concise wording allowed:

> 你回复 1、2 等选项号，我先帮你确认实时价格。确认后如果继续预订，我再收集乘机人信息。你也可以继续补充筛选需求，比如航程偏好、航司、机场、时间段、价格上限或行李要求。

If more filtered options exist beyond those shown, add: `如需我也可以继续展示更多航班。`

## Handoff

When no result is returned for multi-city or multi-segment searches, retry only if there is a clear narrower interpretation (for example split by journey date). Otherwise explain no matching result was returned and ask whether to relax date, airport, airline, cabin, or nonstop constraints.

When the user selects an option, use the private option-to-`solutionId` mapping with `flight_verify_solution`. Say you will confirm the real-time price first; do not call it "下单" or "付款" at this stage.
