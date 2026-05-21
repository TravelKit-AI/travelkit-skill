# mcp-connection ref

## TravelKit 平台凭证配置

TravelKit API credentials are platform-managed. `TRAVELKIT_API_KEY` must be configured by the agent platform, host application, or server-side runtime, then injected automatically when TravelKit tools are called.

Do not treat missing credentials as a local MCP setup task.

## Install / First Use Notice

When the user says the TravelKit Skill is installed, asks how to start using it, asks how to configure an API key, or appears to be using TravelKit for the first time, explain the credential requirement without generating local MCP configuration:

> TravelKit Skill 已安装。使用前请前往 https://www.travelkit.ai/ 申请或完成 API Key 配置，并由智能体平台在后台安全注入 `TRAVELKIT_API_KEY`。最好不要在聊天中发送 API Key。

## Missing API Key / Auth Failure

When `TRAVELKIT_API_KEY` is missing, invalid, expired, not configured, or authentication/authorization fails:

- Do not generate `mcpServers` JSON.
- Do not mention `npx`, local MCP server installation, stdio server setup, or local config files.
- Do not ask users to paste API keys, Bearer tokens, or secrets in chat.
- Do not expose stack traces, request headers, signatures, raw MCP JSON, or raw auth errors.
- Do not ask users to resend passenger, order, or payment information.

Consumer-facing reply:

> 当前 TravelKit 服务凭证未配置或已失效，请前往 https://www.travelkit.ai/ 申请或完成配置后再试。最好不要在聊天中发送 API Key。

Developer/admin-facing reply:

> 请前往 https://www.travelkit.ai/ 申请 TravelKit API Key，并在智能体平台的服务端密钥或环境变量管理中配置 `TRAVELKIT_API_KEY`，由平台在调用 TravelKit 工具时自动注入。不要把密钥写入 skill 文档、提示词、聊天内容、前端页面或本地 MCP 配置示例；最好不要在聊天中发送 API Key。

## Internal Reference Only

Platform implementers may connect to the remote TravelKit endpoint with a Bearer token:

- Endpoint: `https://mcp.travelkit.ai/mcp`
- Header: `Authorization: Bearer {TRAVELKIT_API_KEY}`

This is an internal platform integration reference. Do not turn it into user-facing local MCP configuration instructions.
