# TravelKit-AI

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

## Requirements

- An agent runtime that can load reusable instructions, skills, prompts, or policy files.
- A TravelKit MCP server exposing the flight tools referenced by the skill files.
- For local signed TravelKit requests, `shasum` and a POSIX-compatible shell.

The skills intentionally do not include API credentials, private endpoints, or live passenger data.

## Installation

Copy, symlink, or import the skill directories according to your agent framework's instruction-loading mechanism.

```bash
mkdir -p /path/to/your-agent/skills
cp -R skills/travelkit /path/to/your-agent/skills/
```

If your framework does not support directory-based skills, import the relevant `SKILL.md` files as system instructions or workflow policy for your agent.

## Usage

Load `skills/travelkit/SKILL.md` as the main entry point. The agent will follow the Module Selection Guide to load the relevant per-tool ref file for each task:

- Search / compare flights → `references/flight-search.md`
- Verify real-time price → `references/flight-verify.md`
- Collect passengers, create order → `references/flight-create-order.md`
- Pay → `references/flight-pay-order.md`
- Order lookup / cancel / refund / change / itinerary → respective `references/flight-*.md`
- MCP setup and global safety policy → `references/mcp-connection.md`, `tool-categories.md`, `hidden-fields.md`, `confirmation-rules.md`, `output-rules.md`

All ref files keep internal MCP fields hidden and require explicit confirmation before every state-changing operation.

Set `TRAVELKIT_API_KEY` as the Bearer Token in the `Authorization` header.

## Safety Principles

- Never expose internal fields such as `solutionId`, `orderKey`, confirmation flags, raw passenger IDs, segment IDs, or raw MCP JSON to normal users.
- Never create an order, pay, cancel, refund, confirm a refund, or submit a change request without explicit user confirmation.
- Collect passport, ID card, birthday, phone, and email only at the correct booking stage.
- If baggage, refund, change, ticketing, or policy details are not returned by tools, say they were not returned instead of inventing them.
- Keep normal consumer responses in Simplified Chinese unless the user asks for another language.

## Repository Layout

```text
skills/
  travelkit/
    SKILL.md
    references/
      flight-search.md
      flight-pricing.md
      flight-verify.md
      flight-create-order.md
      flight-pay-order.md
      flight-order-lookup.md
      flight-cancel.md
      flight-refund.md
      flight-change.md
      flight-itinerary.md
      mcp-connection.md
      tool-categories.md
      hidden-fields.md
      confirmation-rules.md
      output-rules.md
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Security-sensitive reports should follow [SECURITY.md](SECURITY.md).

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
