# Known Issues

This document tracks known v1 cross-agent behavior gaps and result-handling issues for the `travelkit` skill. These items are used to guide future skill and evaluation improvements; they do not necessarily indicate TravelKit MCP tool defects.

## KI-001: Search Result Count Is Not Fixed At Five

- **Frequency:** Common known issue / 常规已知问题
- **Area:** Flight shopping result display
- **Symptom:** Different agents may show more than five flight options, or fewer than five when enough filtered options are available.
- **Impact:** Users see inconsistent comparison sets across agents for the same request.
- **Expected Behavior:** Flight search should display exactly five options when at least five valid filtered options exist, and fewer only when fewer valid options are returned after filtering.
- **Current Mitigation / Next Step:** Keep the display-count rule explicit in search instructions and add evaluation cases for enough-results and fewer-than-five-results scenarios.

## KI-002: Passenger Information Prompt Is Inconsistent After Flight Selection

- **Frequency:** Common known issue / 常规已知问题
- **Area:** Booking handoff after price verification
- **Symptom:** After the user selects a flight and wants to proceed, agents ask for passenger information with inconsistent wording or field order.
- **Impact:** The booking flow feels inconsistent and may cause users to omit required fields.
- **Expected Behavior:** After real-time price verification passes and the user confirms booking intent, agents should use a stable passenger-information collection prompt and field set.
- **Current Mitigation / Next Step:** Define a fixed prompt template for passenger/contact collection and add regression checks for the post-verification handoff.

## KI-003: Order Information Output Is Inconsistent

- **Frequency:** Common known issue / 常规已知问题
- **Area:** Order lookup and order status display
- **Symptom:** Agents return different sets of order details for the same order lookup flow.
- **Impact:** Users may not consistently see the most important order status, payment, ticketing, route, passenger, or next-step information.
- **Expected Behavior:** Order lookup should summarize a stable minimum set of user-facing order fields when those fields are returned by tools.
- **Current Mitigation / Next Step:** Define a minimum order-summary schema for user-facing responses and evaluate detail/list lookup flows separately.

## KI-004: Refund And Change Policy Interpretation Can Be Wrong

- **Frequency:** Rare edge case / 少见异常
- **Area:** Refund and change policy display
- **Symptom:** Some agents report that a flight is non-refundable after departure even when the actual policy allows a refund after departure.
- **Impact:** Users may receive incorrect aftercare guidance.
- **Expected Behavior:** Agents should faithfully summarize tool-returned refund/change policy and avoid inferring "non-refundable" when the returned policy supports refund handling.
- **Current Mitigation / Next Step:** Tighten policy interpretation instructions and add examples that include post-departure refundable cases.

## KI-005: Flight Segment Or Leg Information May Be Missing

- **Frequency:** Rare edge case / 少见异常
- **Area:** Flight shopping and itinerary display
- **Symptom:** Some flights include multiple legs or segment details, but an agent returns them as if no leg information exists.
- **Impact:** Users may miss important routing or operating details.
- **Expected Behavior:** Agents should preserve and display returned flight leg/segment information when available.
- **Current Mitigation / Next Step:** Add display requirements and tests for flights with extra leg or segment metadata.

## KI-006: Airline Name And Airline Code Can Be Mismatched

- **Frequency:** Rare edge case / 少见异常
- **Area:** Airline display and code mapping
- **Symptom:** Some agents display an airline name that does not match the returned airline code or flight number.
- **Impact:** Users may see misleading airline information.
- **Expected Behavior:** Airline names should match IATA airline codes and flight numbers. If the mapping is uncertain, agents should show the code rather than invent a name.
- **Current Mitigation / Next Step:** Centralize common airline mappings and add validation checks for name/code consistency.

## KI-007: Multi-Segment Trip Searches May Return No Results

- **Frequency:** Rare edge case / 少见异常
- **Area:** Multi-city and multi-segment flight shopping
- **Symptom:** Some multi-segment trip searches return no results or unstable results across agents.
- **Impact:** Users may be told no itinerary is available even when a different search strategy might produce options.
- **Expected Behavior:** Agents should handle empty multi-segment search results gracefully and, when appropriate, suggest a narrower or decomposed search strategy.
- **Current Mitigation / Next Step:** Document fallback search strategies for multi-segment trips and add evaluation cases for empty results.

## KI-008: Agents May Output Python Files Or Code Artifacts Unexpectedly

- **Frequency:** Rare edge case / 少见异常
- **Area:** Response formatting and tool discipline
- **Symptom:** Some agents unexpectedly produce a Python file or code artifact during a normal flight workflow.
- **Impact:** Users receive irrelevant output instead of flight-shopping or order-care guidance.
- **Expected Behavior:** Flight workflows should produce consumer-facing travel responses, not code files, unless the user explicitly asks for code or integration artifacts.
- **Current Mitigation / Next Step:** Strengthen output-mode guidance and add tests that reject unrelated code artifacts in consumer flows.

## KI-009: First Search Response May Omit Prices

- **Frequency:** Rare edge case / 少见异常
- **Area:** Flight shopping result display
- **Symptom:** Some agents do not return prices on the first search response and instead ask follow-up questions even when tool results include prices.
- **Impact:** Users have to ask again or answer unnecessary questions before seeing useful options.
- **Expected Behavior:** If valid search results include prices, agents should show prices in the first result list.
- **Current Mitigation / Next Step:** Keep price as a required display field when returned and add tests for first-response search output.
