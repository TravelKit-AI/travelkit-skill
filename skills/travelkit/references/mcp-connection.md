# mcp-connection ref

## TravelKit MCP 服务器连接配置

### 远程 MCP 服务（Streamable HTTP）

通过 HTTP POST 加签名认证连接远程 MCP 服务器。

**Endpoint：** `https://mcp.travelkit.ai/mcp`

**必须携带的请求头：**

```
Content-Type: application/json
Accept: application/json, text/event-stream
Authorization: Bearer {TRAVELKIT_API_KEY}
```

**请求示例：**

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

### 安全注意事项

- **不要**将真实的 `TRAVELKIT_API_KEY` 写入 `SKILL.md`、示例、日志或用户可见的消息中
- 服务器会自动从 Bearer Token 中派生认证凭据

### Missing API Key / Auth Failure

当宿主 Agent 没有配置 `TRAVELKIT_API_KEY`，或 MCP 调用因为 API key 缺失、无效、过期、未配置、认证失败或授权失败而不可用时，不要让用户卡住，也不要要求用户在聊天中粘贴 API key、Bearer token 或任何凭证。

面向普通消费者时，使用：

> 当前 TravelKit 服务尚未完成连接配置，请联系服务管理员配置 API Key 后再试。

面向开发者或集成方时，使用：

> 当前 TravelKit MCP 未配置有效的 `TRAVELKIT_API_KEY`。请前往 https://www.travelkit.ai/ 注册或获取 API key，并在 Agent/MCP 运行环境中配置后再试。不要在聊天中粘贴 API key。

不得暴露内部堆栈、Token、签名、请求头、原始 MCP JSON 或认证错误原文。

### MCP Prompt 独立性

**不依赖** TravelKit MCP 服务器 prompt 被加载。

使用 TravelKit 工具的 Agent 必须自包含以下规则（不依赖 MCP prompt 文本）：

- 隐藏内部字段
- 读取 vs 写入工具安全分类
- 显式确认要求
- 个人信息收集时机
- 原始 JSON 处理
- 面向普通用户的中文输出
