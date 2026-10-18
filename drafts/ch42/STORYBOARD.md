# Chapter 42 figure decisions (before prose)

1. WAL crash-cut timeline with append/flush/page-write events and distinct durable log versus page LSN tracks. Cut after flush before page is recoverable by redo; cut before flush loses the assignment.
2. Buffer validity: native recurrence, Hermon KV and durable event have different recovery prerequisites. Show object-specific checks before eviction/reconstruction rather than generic boxes claiming interchangeability.
3. Physical-plan comparison: hard semantic and resource filters precede weighted cost ranking. Cheapest wrong-contract candidate is rejected. Numeric result is a stipulated cost model, not hardware measurement.
