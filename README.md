# TravelKit-AI

TravelKit-AI is a set of reusable agent instructions for agents that work with TravelKit flight MCP tools. The skills define consumer-facing flight shopping, booking, payment safety, order aftercare, and shared integration policy.

The project is prompt and policy content, not a standalone flight API client. It assumes a TravelKit MCP server is connected by the host agent or application.

## What Is Included

| Skill | Purpose |
|---|---|
| `travelkit-flight-shopping` | Search, compare, recommend, and label flight options as `F1`-`F5`. |
| `travelkit-flight-booking` | Verify selected prices, collect passenger details, create orders, and handle payment confirmation. |
| `travelkit-flight-aftercare` | Check orders, download itineraries, cancel unpaid orders, request refunds, and change flights. |
| `travelkit-agent-integration` | Shared TravelKit MCP safety, privacy, confirmation, hidden-field, and signing rules. |

## Requirements

- An agent runtime that can load reusable instructions, skills, prompts, or policy files.
- A TravelKit MCP server exposing the flight tools referenced by the skill files.
- For local signed TravelKit requests, `shasum` and a POSIX-compatible shell.

The skills intentionally do not include API credentials, private endpoints, or live passenger data.

## Installation

Copy, symlink, or import the skill directories according to your agent framework's instruction-loading mechanism.

```bash
mkdir -p /path/to/your-agent/skills
cp -R skills/travelkit-* /path/to/your-agent/skills/
```

If your framework does not support directory-based skills, import the relevant `SKILL.md` files as system instructions or workflow policy for your agent.

## Usage

After installation, load or invoke the relevant skill from an agent task:

- Use `travelkit-flight-shopping` when the user wants to search, compare, filter, or choose flights.
- Use `travelkit-flight-booking` after the user selects an option and wants to verify price, continue booking, create an order, or pay.
- Use `travelkit-flight-aftercare` for order status, cancellation, itinerary, refund, or change workflows.
- Use `travelkit-agent-integration` for technical integration policy and global TravelKit MCP safety rules.

The workflow skills are designed to keep internal MCP fields hidden from normal users and to require explicit confirmation before every state-changing operation.

## Local Signing Helper

`skills/travelkit-agent-integration/scripts/local_sign.sh` generates a timestamp and SHA1 signature for local testing.

```bash
TRAVELKIT_API_KEY="<your-api-key>" \
  skills/travelkit-agent-integration/scripts/local_sign.sh
```

The script derives `CODE` from the first 6 characters of `TRAVELKIT_API_KEY` and `API_KEY` from the remainder.

Do not commit real `TRAVELKIT_API_KEY` values, signatures, access tokens, order payloads, passenger documents, or logs containing personal information.

## Safety Principles

- Never expose internal fields such as `solutionId`, `orderKey`, confirmation flags, raw passenger IDs, segment IDs, or raw MCP JSON to normal users.
- Never create an order, pay, cancel, refund, confirm a refund, or submit a change request without explicit user confirmation.
- Collect passport, ID card, birthday, phone, and email only at the correct booking stage.
- If baggage, refund, change, ticketing, or policy details are not returned by tools, say they were not returned instead of inventing them.
- Keep normal consumer responses in Simplified Chinese unless the user asks for another language.

## Repository Layout

```text
skills/
  travelkit-agent-integration/
    SKILL.md
    scripts/local_sign.sh
  travelkit-flight-aftercare/
    SKILL.md
  travelkit-flight-booking/
    SKILL.md
  travelkit-flight-shopping/
    SKILL.md
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Security-sensitive reports should follow [SECURITY.md](SECURITY.md).

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
