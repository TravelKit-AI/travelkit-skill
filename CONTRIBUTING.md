# Contributing / 参与贡献

Thanks for improving TravelKit Skill. This repository contains agent instructions for TravelKit flight workflows, so contributions are reviewed as user-facing behavior and safety policy, not only as text edits.

感谢你改进 TravelKit Skill。本仓库包含 TravelKit 航班工作流的 agent 指令，因此贡献审核不仅看文字，也会重点看用户可见行为和安全策略。

## How to Contribute / 如何贡献

1. Open or find an issue.
   先创建或找到一个 Issue。

2. Comment before starting if the change is non-trivial.
   如果改动不是很小，请先留言说明你准备处理，方便维护者确认方向。

3. Fork the repository and create a focused branch.
   Fork 仓库，并创建一个聚焦的小分支。

   ```bash
   git checkout -b fix/short-description
   ```

4. Make the smallest safe change that solves the issue.
   用尽量小且安全的改动解决问题。

5. Review the affected workflow manually.
   手动检查受影响的工作流。

6. Open a pull request and complete the PR checklist.
   创建 Pull Request，并完成 PR 模板中的检查清单。

7. Respond to maintainer review until the PR is ready to squash merge.
   根据维护者 review 修改，直到 PR 可以 squash merge。

## What to Work On / 可以做什么

- Bug fixes for incorrect, unsafe, or confusing TravelKit skill behavior.
- Documentation improvements for README, skill references, examples, and contribution docs.
- Workflow improvements for flight search, booking, payment, order lookup, cancellation, refund, change, or agent integration.
- Small issues labeled `good first issue`, `help wanted`, or `ready for PR`.

- 修复 TravelKit skill 中错误、不安全或令人困惑的行为。
- 改进 README、skill 参考、示例和贡献文档。
- 改进航班搜索、预订、支付、订单查询、取消、退票、改签或 agent 集成流程。
- 优先选择带有 `good first issue`、`help wanted` 或 `ready for PR` 标签的小任务。

## Before You Start / 开始前

- Read the affected `SKILL.md` and reference file from top to bottom.
- Use mock examples only.
- Do not add real user data, real orders, real credentials, production logs, or screenshots with sensitive data.
- Keep changes focused on the issue being solved.
- Ask in the issue if the intended behavior is unclear.

- 从头到尾阅读受影响的 `SKILL.md` 和 reference 文件。
- 仅使用模拟示例。
- 不要加入真实用户数据、真实订单、真实凭证、生产日志或含敏感信息的截图。
- 让改动聚焦在当前 Issue。
- 如果预期行为不清楚，请先在 Issue 中询问。

## Skill Boundaries / Skill 边界

- Flight shopping: search, comparison, recommendation, and visible option labels.
- Flight booking: price verification, passenger collection, order creation, and payment confirmation.
- Flight aftercare: order lookup, itinerary download, cancellation, refund, and change workflows.
- Agent integration: MCP connection, safety, privacy, hidden-field, confirmation, raw-JSON, and signing policy.

- 航班搜索：搜索、对比、推荐和用户可见选项编号。
- 航班预订：验价、乘客信息收集、创建订单和支付确认。
- 售后流程：订单查询、行程单下载、取消、退票和改签。
- Agent 集成：MCP 连接、安全、隐私、隐藏字段、确认、raw JSON 和签名策略。

Do not duplicate detailed workflow rules across unrelated files unless duplication is intentional and keeps agents safe when only one skill file is loaded.

除非是为了确保单独加载某个 skill 文件时仍然安全，否则不要在无关文件中重复详细工作流规则。

## Pull Request Checklist / PR 检查清单

Before opening a pull request, verify:

提交 PR 前请确认：

- No real credentials, private keys, signatures, personal data, order data, ticket numbers, itinerary files, production logs, or sensitive screenshots are included.
- Normal consumer-facing output remains Simplified Chinese by default unless the user requests another language.
- Internal fields such as `solutionId`, `orderKey`, `externalOrderId`, confirmation flags, raw passenger IDs, segment IDs, `idempotencyKey`, and raw MCP JSON remain hidden from normal users.
- State-changing tools still require explicit confirmation immediately before use.
- Passenger documents, birthdays, phone numbers, and emails are not collected during flight search.
- Missing tool-returned baggage, refund, change, ticketing, or policy details are described as not returned instead of invented.
- Examples use mock data only and do not imply that price verification locks prices, holds seats, or guarantees ticketing unless the tool explicitly says so.

- 未包含真实凭证、私钥、签名、个人信息、订单数据、票号、行程单、生产日志或敏感截图。
- 普通用户可见输出默认保持简体中文，除非用户要求其他语言。
- `solutionId`、`orderKey`、`externalOrderId`、确认标记、raw passenger IDs、segment IDs、`idempotencyKey` 和 raw MCP JSON 等内部字段仍不会暴露给普通用户。
- 状态变更工具在调用前仍要求用户立即、明确确认。
- 航班搜索阶段不会收集乘客证件、生日、手机号和邮箱。
- 工具未返回的行李、退改签、出票或政策详情会说明未返回，不会编造。
- 示例仅使用模拟数据，并且不会暗示验价会锁价、占座或保证出票，除非工具明确返回。

## Style / 风格

- Keep instructions direct, testable, and easy for agents to follow.
- Prefer concrete user-facing examples when a rule affects wording.
- Avoid raw JSON examples unless the change is specifically for technical integration policy.
- Keep file names, tool names, and MCP field names in English.
- Keep normal user-facing copy in Simplified Chinese.

- 指令应直接、可测试，并且便于 agent 遵循。
- 当规则影响措辞时，优先提供具体用户可见示例。
- 除非改动专门涉及技术集成策略，否则避免 raw JSON 示例。
- 文件名、工具名和 MCP 字段名保持英文。
- 普通用户可见文案保持简体中文。

## Testing Changes / 测试改动

There is no automated test suite yet. Review changes manually by checking:

当前还没有自动化测试。请通过手动检查验证：

- The relevant workflow from user intent to next action.
- Hidden-field handling.
- Confirmation wording before state-changing tools.
- Passenger data timing and required fields.
- Error handling for missing, failed, or incomplete tool results.
- Whether README, issue templates, and pull request templates guide contributors without asking for sensitive data.

- 从用户意图到下一步行动的相关工作流。
- 隐藏字段处理。
- 状态变更工具调用前的确认措辞。
- 乘客信息收集时机和必填字段。
- 工具返回缺失、失败或不完整时的错误处理。
- README、Issue 模板和 PR 模板是否能引导贡献者，同时避免收集敏感数据。

## Security / 安全

Security-sensitive reports should follow [SECURITY.md](SECURITY.md). Do not open public issues with exploit details, credentials, passenger data, order data, ticket numbers, or production logs.

安全敏感问题请遵循 [SECURITY.md](SECURITY.md)。不要在公开 Issue 中披露漏洞利用细节、凭证、乘客信息、订单数据、票号或生产日志。
