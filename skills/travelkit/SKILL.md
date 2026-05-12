---
name: travelkit
description: TravelKit flight booking and management skill. Use flight-shopping for search/comparison, flight-booking for price verification and order creation, flight-aftercare for order management, and agent-integration for technical configuration. This skill covers the complete flight booking lifecycle through TravelKit MCP tools. Use this skill even if TravelKit MCP prompts are not loaded.
---

# TravelKit Flight Skill

Complete flight booking and management solution powered by TravelKit MCP.

## Workflow Modules

This skill is organized into four specialized workflow modules:

- **[flight-shopping](references/flight-shopping.md)** - Search, compare, and recommend flights
- **[flight-booking](references/flight-booking.md)** - Price verification, passenger collection, order creation, and payment
- **[flight-aftercare](references/flight-aftercare.md)** - Order lookup, cancellation, refund, change, and itinerary download
- **[agent-integration](references/agent-integration.md)** - Technical integration, MCP configuration, and global safety rules

## Quick Reference

| Task | Use Module |
|------|-----------|
| Search flights, compare options | flight-shopping |
| Book a flight, create order | flight-booking |
| Check order status, cancel, refund | flight-aftercare |
| Configure MCP, authentication | agent-integration |

## MCP Endpoint

- **URL**: `https://mcp.travelkit.ai/mcp`
- **Auth**: Signature-based (code + timestamp + signature)
- **Details**: See [agent-integration](references/agent-integration.md) for complete setup

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

### When to use flight-shopping
- User asks to search flights
- User wants to compare options
- User needs recommendations
- Initial flight discovery phase

### When to use flight-booking
- User selected a flight option (F1, F2, etc.)
- Price verification needed
- Passenger information collection
- Order creation and payment

### When to use flight-aftercare
- User wants to check order status
- Cancellation request
- Refund or change request
- Itinerary download

### When to use agent-integration
- Setting up MCP connection
- Configuring authentication
- Building custom agent
- Technical integration work

## Safety Checklist

Before any TravelKit MCP operation:
- [ ] Identify the correct workflow module
- [ ] Use flight-shopping for search, flight-booking for booking, flight-aftercare for management
- [ ] Distinguish read vs write tools
- [ ] Get explicit confirmation for state-changing operations
- [ ] Keep hidden fields internal
- [ ] Respond in Simplified Chinese for consumers
- [ ] Don't invent missing tool data
- [ ] Collect personal info only at appropriate workflow stage

## Directory Structure

```
skills/travelkit/
├── SKILL.md                      # This file - main entry point
├── references/
│   ├── flight-shopping.md        # Search and comparison workflow
│   ├── flight-booking.md         # Booking and payment workflow
│   ├── flight-aftercare.md       # Order management workflow
│   └── agent-integration.md      # Technical integration guide
```
