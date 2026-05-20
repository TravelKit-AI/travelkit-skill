# Changelog

All notable changes to this project should be documented here.

This project follows a lightweight changelog format. Add entries under `Unreleased` before tagging a release.

## Unreleased

- Document v1 skill core capabilities and usage boundaries in the README.
- Add open source project documentation, license, security policy, contribution guide, and GitHub templates.
- Remove standalone known-issues documentation and keep issue tracking in GitHub.

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
