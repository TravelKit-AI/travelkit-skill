# Changelog

All notable changes to this project should be documented here.

This project follows a lightweight changelog format. Add entries under `Unreleased` before tagging a release.

## Unreleased

- Document v1 skill core capabilities and usage boundaries in the README.
- Add open source project documentation, license, security policy, contribution guide, and GitHub templates.
- Remove standalone known-issues documentation and keep issue tracking in GitHub.

## 1.0.6

- Republished the TravelKit release package from a clean skill bundle.
- Excluded unrelated hotel references and scripts from the ClawHub, GitHub, and SkillHub release artifacts.
- Kept the v1.0.5 API key guidance, credential routing, and platform-managed credential behavior unchanged.
- No MCP tool schemas or tool parameters were changed.

## 1.0.5

- Added install and first-use guidance directing users to https://www.travelkit.ai/ to apply for or complete API key configuration.
- Updated user-facing API key wording to say users should preferably not send API keys in chat.
- Kept platform-managed credential handling and local MCP configuration prevention unchanged.

## 1.0.4

- Renamed the credential/configuration reference from `mcp-connection.md` to `platform-credentials.md`.
- Updated API key troubleshooting to treat missing or invalid `TRAVELKIT_API_KEY` as a platform-managed credential issue.
- Directed users to https://www.travelkit.ai/ to apply for or complete TravelKit API key configuration.
- Prevented agents from inventing local MCP configuration snippets such as `mcpServers`, `npx`, stdio server setup, local MCP server installation, or local config JSON.
- Clarified that API keys must not be pasted into chat, prompts, frontend pages, skill files, examples, or logs.

## 1.0.3

- Added invoice application and invoice status lookup workflows.
- Added post-payment polling for payment and ticketing status checks.
- Added refund/change rule code interpretation.
- Improved flight search to default to 10 lowest-price display options and avoid raw response parsing.
- Improved low-inventory, passenger information, optional email, order list, and route display rules.
- Fixed user-visible output rules to omit restricted booking-record fields.
- Clarified unpaid order, post-payment, and order-lookup status wording.

## 1.0.1

- 优化了用户确认订单后，Agent 提示收集用户信息的稳定性。

## 1.0.0

- Add TravelKit flight shopping skill.
- Add TravelKit flight booking skill.
- Add TravelKit flight aftercare skill.
- Add TravelKit agent integration skill and local signing helper.
