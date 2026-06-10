## Summary / 摘要

<!-- What changed, and why? -->
<!-- 改了什么，为什么改？ -->

## Scope / 范围

- [ ] Flight search / 航班搜索
- [ ] Pricing or verification / 价格查询或验价
- [ ] Booking or payment / 预订或支付
- [ ] Order lookup / 订单查询
- [ ] Cancellation, refund, or change / 取消、退票或改签
- [ ] Agent integration or MCP policy / Agent 集成或 MCP 策略
- [ ] Documentation or repository governance / 文档或仓库治理

## Testing / 测试

<!-- Describe manual checks or automated tests. If not tested, explain why. -->
<!-- 描述手动检查或自动测试。如未测试，请说明原因。 -->

## TravelKit Safety Checklist / TravelKit 安全检查

- [ ] No real API keys, access tokens, private keys, signatures, cookies, or session data are included.
- [ ] No real passenger names, birthdays, document numbers, phone numbers, emails, order data, ticket numbers, itinerary files, production logs, or screenshots with sensitive data are included.
- [ ] Hidden internal fields such as `solutionId`, `orderKey`, `externalOrderId`, confirmation flags, raw passenger IDs, segment IDs, `idempotencyKey`, and raw MCP JSON remain hidden from normal users.
- [ ] State-changing tools still require explicit user confirmation immediately before use.
- [ ] Passenger documents, birthdays, phone numbers, and emails are still collected only after price verification and user intent to continue booking.
- [ ] Missing tool-returned baggage, refund, change, ticketing, or policy details are reported as missing instead of invented.
- [ ] Normal consumer-facing output remains Simplified Chinese by default unless the user requests another language.

## 中文安全检查

- [ ] 未包含真实 API key、访问令牌、私钥、签名、cookie 或 session 数据。
- [ ] 未包含真实乘客姓名、生日、证件号、手机号、邮箱、订单信息、票号、行程单、生产日志或含敏感信息的截图。
- [ ] `solutionId`、`orderKey`、`externalOrderId`、确认标记、raw passenger IDs、segment IDs、`idempotencyKey` 和 raw MCP JSON 等内部字段仍不会暴露给普通用户。
- [ ] 所有状态变更工具在调用前仍要求用户立即、明确确认。
- [ ] 乘客证件、生日、电话和邮箱仍只在验价后且用户确认继续预订时收集。
- [ ] 工具未返回的行李、退改签、出票或政策详情会说明未返回，不会编造。
- [ ] 普通用户可见输出默认保持简体中文，除非用户要求其他语言。
