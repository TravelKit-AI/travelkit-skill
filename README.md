# TravelKit-AI

[![Repository checks](https://github.com/TravelKit-AI/travelkit-skill/actions/workflows/repository-checks.yml/badge.svg)](https://github.com/TravelKit-AI/travelkit-skill/actions/workflows/repository-checks.yml)

TravelKit-AI is a set of reusable agent instructions for agents that work with TravelKit flight MCP tools. The skills define consumer-facing flight shopping, booking, payment safety, order aftercare, and shared integration policy.

The project is prompt and policy content, not a standalone flight API client. It assumes a TravelKit MCP server is connected by the host agent or application.

## What Is Included

One skill (`travelkit`) with 15 per-tool reference files organized into four workflow groups:

| Group | Reference Files |
|---|---|
| **Flight Shopping** | `flight-search`, `flight-pricing` |
| **Flight Booking** | `flight-verify`, `flight-create-order`, `flight-pay-order` |
| **Flight Aftercare** | `flight-order-lookup`, `flight-cancel`, `flight-refund`, `flight-change`, `flight-itinerary` |
| **Agent Integration** | `mcp-connection`, `tool-categories`, `hidden-fields`, `confirmation-rules`, `output-rules` |

## Core Capabilities

The first version of the `travelkit` skill covers the full consumer flight lifecycle through TravelKit MCP tools:

| Capability | What It Supports |
|---|---|
| **Flight Shopping** | Search and compare available flights, price a known flight number, apply airport/airline/time/stop preferences, and present user-facing options. |
| **Flight Booking** | Verify real-time price for a selected option, collect required passenger details at the correct stage, and create an order after explicit confirmation. |
| **Payment Safety** | Present supported payment choices, require explicit payment confirmation, and verify order state after payment attempts. |
| **Order Aftercare** | Look up order details or lists, cancel eligible orders, quote/request refunds, search/submit changes, and download itineraries. |
| **Agent Integration** | Document MCP connection requirements, read/write tool categories, hidden fields, confirmation rules, and consumer-facing output rules. |

## Contributing / 参与贡献

TravelKit-AI is managed as an open source GitHub project. Community members can report issues, propose improvements, discuss ideas, and submit pull requests.

TravelKit-AI 按开源 GitHub 项目方式管理。社区用户可以反馈问题、提出改进建议、参与讨论并提交 Pull Request。

- **Report a bug / 报告错误**: Open a bug issue with mock data only. Do not include real passenger data, order data, ticket numbers, credentials, logs, or raw MCP responses.
- **Request a feature / 提出功能建议**: Open a feature issue and describe the user workflow, affected TravelKit area, and expected behavior.
- **Improve docs / 改进文档**: Open a documentation issue or pull request for README, skill references, examples, or contribution docs.
- **Ask questions / 提问讨论**: Use GitHub Discussions for open-ended questions, ideas, and community help.
- **Submit a pull request / 提交 PR**: Read [CONTRIBUTING.md](CONTRIBUTING.md), fork the repository, create a focused branch, and complete the pull request checklist.
- **Report security issues / 报告安全问题**: Follow [SECURITY.md](SECURITY.md). Do not disclose vulnerabilities, credentials, personal data, or production order data in public issues.

## Usage Boundaries

Use the skill for TravelKit flight workflows only. It is not a standalone API client and does not replace the TravelKit MCP server or its live availability, pricing, ticketing, and policy responses.

| Area | Use When | Do Not Use When |
|---|---|---|
| **Search / compare** | The user gives a route, date, passenger count, cabin, or preferences and wants flight options. | The user already provided a complete flight number, airports, date, and cabin; use pricing instead. |
| **Known-flight pricing** | The user asks for the price of a specific flight number with enough route/date/cabin detail. | The user is still exploring routes, dates, airlines, or airports. |
| **Price verification** | The user selects a numbered search/pricing option and wants to continue. | The user has not selected a concrete option. |
| **Order creation** | Price verification has passed, required passenger/contact details are collected, and the user explicitly confirms order creation. | During search, before real-time price verification, or without explicit confirmation. |
| **Payment** | An order exists and the user explicitly confirms a payment method and amount. | The user only says they may book, or payment details are ambiguous. |
| **Cancellation** | The user wants to cancel an unpaid or cancelable order and explicitly confirms the target order. | The order is ticketed and needs refund handling instead. |
| **Refund** | The user wants to refund ticketed segments and the agent can quote/confirm refund details first. | The user has not selected passengers/segments or has not confirmed the refund request. |
| **Change** | The user wants to change ticketed flights, reviews available change options, and confirms the selected option. | No valid change option has been returned or selected. |
| **Itinerary** | The user asks for an itinerary document for an existing order. | The user is asking for booking confirmation or ticket issuance status; use order lookup first. |
| **Integration config** | Developers need MCP endpoint, auth/header requirements, hidden-field policy, or confirmation behavior. | The request requires credentials, live passenger data, or exposing internal MCP fields to normal users. |

## Requirements

- An agent runtime that can load reusable instructions, skills, prompts, or policy files.
- A TravelKit MCP server exposing the flight tools referenced by the skill files.

The skills intentionally do not include API credentials, private endpoints, or live passenger data.

## Installation

Install from the source directory or from the release package according to your agent framework's instruction-loading mechanism.

### From Source / 从源码目录安装

Copy, symlink, or import the skill directory:

```bash
mkdir -p /path/to/your-agent/skills
cp -R skills/travelkit /path/to/your-agent/skills/
```

### From Release Zip / 从发布压缩包安装

Download `travelkit.zip` from the latest GitHub Release, then extract it into your agent's skills directory:

```bash
mkdir -p /path/to/your-agent/skills
unzip travelkit.zip -d /path/to/your-agent/skills/
```

The committed package `skills/travelkit.zip` is a release artifact and must stay in sync with `skills/travelkit/`. Maintainers should rebuild it with `scripts/package-skill.sh` before tagging a release.

If your framework does not support directory-based skills, import the relevant `SKILL.md` files as system instructions or workflow policy for your agent.

## MCP Connection

- **Endpoint**: `https://mcp.travelkit.ai/mcp` (Streamable HTTP)
- **Auth**: Bearer token via `Authorization: Bearer {TRAVELKIT_API_KEY}`
- **Required headers**: `Content-Type: application/json`, `Accept: application/json, text/event-stream`

```bash
curl -X POST https://mcp.travelkit.ai/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer ${TRAVELKIT_API_KEY}" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "id": 1,
    "params": {
      "name": "flight_search",
      "arguments": {
        "cabinClass": "economy",
        "journeys": [{"origin": "BJS", "destination": "BKK", "departureDate": "2026-06-01"}],
        "adult": 1,
        "child": 0,
        "infant": 0
      }
    }
  }'
```

Do **not** write `TRAVELKIT_API_KEY` into `SKILL.md`, logs, or user-visible messages.

## Skill And MCP Responsibilities

Use the skill as the workflow and policy layer, and use MCP tools as low-level execution primitives.

- Skill owns user-intent routing, workflow order, confirmations, safety checks, passenger-data timing, output format, and error handling.
- MCP tools own live execution only: search, price verification, order creation, payment, order lookup, cancellation, refund, change, and itinerary download.
- MCP tool descriptions should not compete with the skill as business entry points. Prefer capability wording such as "Low-level tool used by the TravelKit flight workflow..." instead of "Use this tool when the user wants to book a flight."
- If the agent platform supports staged exposure, expose TravelKit MCP tools after this skill is selected. If all tools are always visible, the agent must still follow `SKILL.md` Tool Routing before any MCP call.

## Version Update Notices

Skill update checks should be handled by SkillHub or the host agent platform, not by the skill itself. A recommended integration is to check once per user or workspace on the first TravelKit Skill use each day, then inject version facts into the agent context:

- `skillVersionStatus`: `outdated`, `latest`, or `unknown`
- `installedVersion`: currently installed TravelKit Skill version
- `latestVersion`: latest TravelKit Skill version known to SkillHub or the host platform
- `updateUrl`: optional SkillHub, host-platform, or release-page URL

When the injected status is `outdated`, the skill may show a short non-blocking update notice. When the status is `latest`, it stays silent. When the status is `unknown`, the skill must not claim the installed version is outdated; it only suggests checking SkillHub or the release page in installation, configuration, API key, missing-tool, unexpected-behavior, version, or update conversations.

The skill does not store user state, run timers, or independently query latest versions. Daily check frequency, persistence such as `lastSkillVersionCheckAt`, and update-source selection belong to the host platform.

## Usage

Load `skills/travelkit/SKILL.md` as the main entry point. The agent follows the Module Selection Guide to load the relevant per-tool ref file for each task:

| Task | Reference |
|------|-----------|
| Search / compare flights | `references/flight-search.md` |
| Query price by flight number | `references/flight-pricing.md` |
| Verify real-time price for a selected option | `references/flight-verify.md` |
| Collect passengers and create order | `references/flight-create-order.md` |
| Pay for an order | `references/flight-pay-order.md` |
| Look up order status | `references/flight-order-lookup.md` |
| Cancel an order | `references/flight-cancel.md` |
| Refund / 退票 | `references/flight-refund.md` |
| Change / 改签 | `references/flight-change.md` |
| Download itinerary | `references/flight-itinerary.md` |
| MCP connection and auth | `references/mcp-connection.md` |
| Tool categories (read vs write) | `references/tool-categories.md` |
| Hidden internal fields | `references/hidden-fields.md` |
| Write-operation confirmation rules | `references/confirmation-rules.md` |
| User-facing output rules | `references/output-rules.md` |

## Tool Categories

**Read tools** — call as needed, no extra confirmation required:

`flight_search`, `flight_pricing`, `flight_verify_solution`, `flight_order_detail`, `flight_order_detail_by_external_id`, `flight_order_list`, `flight_download_itinerary`, `flight_change_search`, `flight_refund_quote`, `flight_refund_money_search`, `flight_get_airline_alliances`, `flight_get_airline_alliance_by_airline`, `flight_get_balance`

**Write tools** — require explicit user confirmation before every call:

`flight_create_order`, `flight_pay_order`, `flight_cancel_order`, `flight_refund_request`, `flight_refund_confirm`, `flight_change_request`

## Booking Workflow

```
flight_search / flight_pricing
        ↓  user selects option
flight_verify_solution          ← verify real-time price
        ↓  price confirmed
flight_create_order             ← collect passengers → create order (no auto-pay)
        ↓  user confirms payment
flight_pay_order                ← pay order
        ↓
flight_order_detail             ← verify final ticket status
```

**Aftercare**: `flight_order_detail` / `flight_order_list` → `flight_cancel_order` / `flight_refund_*` / `flight_change_*` / `flight_download_itinerary`

## Safety Principles

- **Hide internals** — never expose `solutionId`, `orderKey`, `externalOrderId`, confirmation flags, raw `passengerIds`/`segmentIds`, `idempotencyKey`, API keys, or raw MCP JSON to normal users.
- **Confirm before every write** — restate key details and get explicit confirmation before calling any write tool. Generic intent ("帮我订", "退了吧") is not sufficient.
- **Collect personal info at the right stage** — collect passport / ID card / birthday / phone / email only after price verification passes and the user confirms they want to proceed with booking.
- **Route through the skill first** — TravelKit MCP tools are execution primitives, not standalone business workflows. Choose the skill workflow before calling any tool.
- **Never invent missing data** — if baggage, refund, change, ticketing, or policy details are not returned by tools, say they were not returned.
- **Simplified Chinese by default** — respond in Simplified Chinese for normal consumers unless the user requests another language.
- **Self-contained rules** — the agent must enforce all rules above independently of whether TravelKit MCP server prompts are loaded.

## Repository Layout

```text
skills/
  travelkit/
    SKILL.md                          # main entry point
    references/
      flight-search.md              # flight_search — search flights
      flight-pricing.md             # flight_pricing — query price by flight number
      flight-verify.md              # flight_verify_solution — verify real-time price
      flight-create-order.md        # flight_create_order — collect passengers + create order
      flight-pay-order.md           # flight_pay_order — pay order
      flight-order-lookup.md        # flight_order_detail / list — look up orders
      flight-cancel.md              # flight_cancel_order — cancel order
      flight-refund.md              # flight_refund_* — refund flow
      flight-change.md              # flight_change_* — change flow
      flight-itinerary.md           # flight_download_itinerary — download itinerary
      mcp-connection.md             # MCP connection and auth
      tool-categories.md            # read vs write tool classification
      hidden-fields.md              # internal fields that must never be exposed
      confirmation-rules.md         # per-operation confirmation requirements
      output-rules.md               # user-facing output rules
```

## Community / 社区

See [CONTRIBUTING.md](CONTRIBUTING.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), and [SECURITY.md](SECURITY.md) before opening issues, discussions, or pull requests.

创建 Issue、Discussion 或 Pull Request 前，请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)、[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) 和 [SECURITY.md](SECURITY.md)。

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
