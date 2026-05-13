---
name: travelkit
description: TravelKit flight booking and management skill. Use flight-search to search and compare flights, flight-verify to confirm real-time price, flight-create-order to collect passengers and create orders, flight-pay-order to pay, flight-order-lookup/cancel/refund/change/itinerary for aftercare, and mcp-connection/tool-categories/hidden-fields/confirmation-rules/output-rules for integration policy. This skill covers the complete flight booking lifecycle through TravelKit MCP tools. Use this skill even if TravelKit MCP prompts are not loaded.
---

# TravelKit Flight Skill

Complete flight booking and management solution powered by TravelKit MCP.

## Workflow Modules

This skill is organized into four specialized workflow modules, each further broken down into per-tool reference files:

- **Flight Shopping** - Search and compare flights
- **Flight Booking** - Price verification, passenger collection, order creation, and payment
- **Flight Aftercare** - Order lookup, cancellation, refund, change, and itinerary download
- **Agent Integration** - Technical integration, MCP configuration, and global safety rules

## Quick Reference

| Task | Reference |
|------|-----------|
| Search flights, compare options | [flight-search](references/flight-search.md) |
| Query price by flight number | [flight-pricing](references/flight-pricing.md) |
| Verify real-time price for selected option | [flight-verify](references/flight-verify.md) |
| Collect passengers and create order | [flight-create-order](references/flight-create-order.md) |
| Pay for an order | [flight-pay-order](references/flight-pay-order.md) |
| Look up order status | [flight-order-lookup](references/flight-order-lookup.md) |
| Cancel an order | [flight-cancel](references/flight-cancel.md) |
| Refund / 退票 | [flight-refund](references/flight-refund.md) |
| Change / 改签 | [flight-change](references/flight-change.md) |
| Download itinerary | [flight-itinerary](references/flight-itinerary.md) |
| MCP connection and authentication | [mcp-connection](references/mcp-connection.md) |
| Tool categories (read vs write) | [tool-categories](references/tool-categories.md) |
| Hidden internal fields | [hidden-fields](references/hidden-fields.md) |
| Write operation confirmation rules | [confirmation-rules](references/confirmation-rules.md) |
| User-facing output rules | [output-rules](references/output-rules.md) |

## MCP Endpoint

- **URL**: `https://mcp.travelkit.ai/mcp`
- **Auth**: Bearer token (`Authorization: Bearer {TRAVELKIT_API_KEY}`)
- **Details**: See [mcp-connection](references/mcp-connection.md) for complete setup

## Core Principles

1. **Search before booking** - Always use flight-shopping for initial searches
2. **Verify then book** - Price verification required before passenger collection
3. **Confirm before action** - Explicit confirmation required for all state-changing operations
4. **Chinese by default** - Simplified Chinese for normal consumers
5. **Hide internals** - Never expose solutionId, orderKey, raw JSON, or MCP fields to users

## Tool Categories

**Read tools** (can call when needed):
- flight_search, flight_pricing, flight_verify_solution
- flight_order_detail, flight_order_list, flight_download_itinerary
- flight_change_search, flight_refund_quote, flight_refund_money_search

**Write tools** (require explicit confirmation):
- flight_create_order, flight_pay_order, flight_cancel_order
- flight_refund_request, flight_refund_confirm, flight_change_request

## Module Selection Guide

### Flight Shopping
- 用户描述出行需求，搜索航班 → [flight-search](references/flight-search.md)
- 用户已知航班号，查询该航班票价 → [flight-pricing](references/flight-pricing.md)

### Flight Booking
- 用户选定 1/2 等数字选项，验证实时价格 → [flight-verify](references/flight-verify.md)
- 验价通过，收集乘客信息并创建订单 → [flight-create-order](references/flight-create-order.md)
- 订单已创建，用户要求支付 → [flight-pay-order](references/flight-pay-order.md)

### Flight Aftercare
- 查询订单状态、历史订单 → [flight-order-lookup](references/flight-order-lookup.md)
- 取消未支付订单 → [flight-cancel](references/flight-cancel.md)
- 退票申请 → [flight-refund](references/flight-refund.md)
- 改签申请 → [flight-change](references/flight-change.md)
- 下载行程单 → [flight-itinerary](references/flight-itinerary.md)

### Agent Integration
- MCP 连接配置与认证 → [mcp-connection](references/mcp-connection.md)
- 工具读写分类 → [tool-categories](references/tool-categories.md)
- 内部隐藏字段清单 → [hidden-fields](references/hidden-fields.md)
- 写入操作确认规则 → [confirmation-rules](references/confirmation-rules.md)
- 面向用户输出规则 → [output-rules](references/output-rules.md)

## Safety Checklist

Before any TravelKit MCP operation:
- [ ] Identify the correct ref file for the current task (see Module Selection Guide above)
- [ ] Use flight-search/pricing for search, flight-verify/create-order/pay-order for booking, flight-order-lookup/cancel/refund/change/itinerary for aftercare
- [ ] Distinguish read vs write tools
- [ ] Get explicit confirmation for state-changing operations
- [ ] Keep hidden fields internal
- [ ] Respond in Simplified Chinese for consumers
- [ ] Don't invent missing tool data
- [ ] Collect personal info only at appropriate workflow stage

## Directory Structure

```
skills/travelkit/
├── SKILL.md                          # This file - main entry point
├── references/
│   ├── flight-search.md              # flight_search — 搜索航班
│   ├── flight-pricing.md             # flight_pricing — 按航班号查价
│   ├── flight-verify.md              # flight_verify_solution — 验证实时价格
│   ├── flight-create-order.md        # flight_create_order — 乘客收集 + 创建订单
│   ├── flight-pay-order.md           # flight_pay_order — 支付订单
│   ├── flight-order-lookup.md        # flight_order_detail / list — 查询订单
│   ├── flight-cancel.md              # flight_cancel_order — 取消订单
│   ├── flight-refund.md              # flight_refund_* — 退票流程
│   ├── flight-change.md              # flight_change_* — 改签流程
│   ├── flight-itinerary.md           # flight_download_itinerary — 行程单下载
│   ├── mcp-connection.md             # MCP 连接配置与认证
│   ├── tool-categories.md            # 工具分类（读取 vs 写入）
│   ├── hidden-fields.md              # 不得暴露的内部字段清单
│   ├── confirmation-rules.md         # 写入操作确认规则
│   └── output-rules.md              # 面向用户的输出规则
```
