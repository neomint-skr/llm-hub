# Architecture Decision Records (ADR) Index

This document provides an overview of all Architecture Decision Records for LLM Hub.

## ADR Overview

Architecture Decision Records (ADRs) capture important architectural decisions made during the development of LLM Hub. Each ADR documents the context, decision, and consequences of significant architectural choices.

## ADR Status Legend

- **Proposed** - Decision is under consideration
- **Accepted** - Decision has been approved and is being implemented
- **Implemented** - Decision has been fully implemented
- **Superseded** - Decision has been replaced by a newer ADR
- **Deprecated** - Decision is no longer relevant

## Current ADRs

| ADR# | Title | Status | Date | Supersedes |
|------|-------|--------|------|------------|
| [ADR-000](ADR-000-template.md) | ADR Template | Template | 2025-01-30 | - |
| [ADR-001](ADR-001-minimal-platform.md) | Minimal Platform Architecture | Implemented | 2025-01-30 | - |
| [ADR-002](ADR-002-http-only-bridge.md) | HTTP-Only Bridge Implementation | Implemented | 2025-01-30 | - |

## ADR Details

### ADR-000: ADR Template
**Status:** Template  
**Date:** 2025-01-30  
**Context:** Provides a standard template for creating new Architecture Decision Records.  
**Decision:** Use a consistent format for all ADRs including Context, Decision, Status, and Consequences sections.  
**Impact:** Ensures consistency and completeness in architectural documentation.

### ADR-001: Minimal Platform Architecture
**Status:** Implemented  
**Date:** 2025-01-30  
**Context:** Need for a lightweight, scalable platform architecture that follows dedardf principles.  
**Decision:** Implement a minimal platform with clear separation between platform core, units, and operations.  
**Impact:** Enables independent unit development, clear boundaries, and simplified deployment.

### ADR-002: HTTP-Only Bridge Implementation
**Status:** Implemented  
**Date:** 2025-01-30  
**Context:** Choice between WebSocket and HTTP for LM Studio bridge communication.  
**Decision:** Use HTTP-only communication for simplicity and reliability.  
**Impact:** Simplified implementation, better debugging, standard REST patterns.

## Creating New ADRs

### When to Create an ADR

Create a new ADR when making decisions about:
- System architecture and design patterns
- Technology choices and frameworks
- Integration approaches
- Security and authentication strategies
- Performance and scalability decisions
- Breaking changes to existing architecture

### ADR Creation Process

1. **Copy Template**
   ```bash
   cp docs/architecture/decisions/ADR-000-template.md \
      docs/architecture/decisions/ADR-XXX-your-decision.md
   ```

2. **Fill Out Sections**
   - Update the ADR number (next sequential number)
   - Provide clear title describing the decision
   - Fill in all required sections
   - Set initial status to "Proposed"

3. **Review Process**
   - Share with team for feedback
   - Discuss alternatives and implications
   - Update status to "Accepted" when approved
   - Update to "Implemented" when complete

4. **Update Index**
   - Add entry to this index file
   - Include links and summary information
   - Update any superseded ADRs

### ADR Numbering

- Use sequential numbering: ADR-001, ADR-002, etc.
- ADR-000 is reserved for the template
- Do not reuse numbers from deprecated ADRs
- Include leading zeros for numbers under 100

## ADR Relationships

### Dependencies
- ADR-002 depends on ADR-001 (platform architecture)
- Future bridge implementations should reference ADR-002

### Superseding
- No current superseding relationships
- When superseding, update both ADRs with cross-references

## Implementation Status

### Completed Implementations
- ✅ ADR-001: Minimal Platform Architecture
  - Platform structure implemented
  - Unit separation established
  - dedardf principles applied

- ✅ ADR-002: HTTP-Only Bridge Implementation
  - LM Studio bridge uses HTTP
  - REST API patterns implemented
  - No WebSocket dependencies

### Pending Implementations
- No pending implementations currently

## Future ADR Topics

Potential areas for future ADRs:
- Authentication and authorization strategy
- Monitoring and observability approach
- Multi-tenant support design
- Performance optimization strategies
- Security hardening decisions
- Scaling and load balancing approaches

## ADR Maintenance

### Regular Review
- Review ADRs quarterly for relevance
- Update implementation status
- Identify superseded decisions
- Archive deprecated ADRs

### Documentation Standards
- Keep ADRs concise but complete
- Include diagrams where helpful
- Reference related ADRs
- Maintain consistent formatting

### Version Control
- All ADRs are version controlled
- Changes require pull request review
- Maintain history of decision evolution
- Tag major architectural milestones

## References

- [ADR Template](ADR-000-template.md) - Standard format for new ADRs
- [Minimal Platform](ADR-001-minimal-platform.md) - Core architecture decisions
- [HTTP Bridge](ADR-002-http-only-bridge.md) - Communication protocol choices

## Contact

For questions about ADRs or to propose new architectural decisions:
- Create an issue in the project repository
- Reference relevant existing ADRs
- Follow the ADR template format
- Include implementation considerations
