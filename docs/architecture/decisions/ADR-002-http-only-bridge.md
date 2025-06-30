# ADR-002: HTTP-Only Bridge Implementation

## Status

Accepted

## Context

LM Studio provides an OpenAI-compatible HTTP API. MCP clients expect HTTP-based tool interfaces. The bridge needs to translate between these protocols efficiently.

## Decision

Implement HTTP-only bridge with:
- No WebSocket or streaming protocols initially
- Direct HTTP-to-HTTP translation
- Standard OpenAI API compatibility
- MCP tool interface compliance

## Consequences

### Positive
- Simple implementation
- Wide compatibility
- Easy testing and debugging
- Standard protocol support

### Negative
- No real-time streaming initially
- Higher latency for some use cases

### Neutral
- Can add streaming later if needed
