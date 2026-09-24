# Chapter 16: Expression complexity and resource semantics

Author-approved storyboard for the original standalone candidate. Independent review remains open.

## 01-ledger

Question: Why is activated parameter count not total cost?
Objects and arrow semantics: Explicit separate ledgers for parameters, arithmetic, routing decisions, bytes and trace events.
Change/invariant and caption claim: Owners deduplicate stored weights; calls still incur repeated work.
Scientific risk: Symbolic accounting is not measured latency.

## 02-routing

Question: When does sparse routing save less than expected?
Objects and arrow semantics: Dense/sparse token-expert incidence matrices and a padded capacity grid.
Change/invariant and caption claim: Padding and routing can add executed work beyond useful work.
Scientific risk: This is an accounting example, not a kernel performance claim.

## 03-liveness

Question: Why can two legal schedules have different memory peaks?
Objects and arrow semantics: Dependency diamond and buffer lifetime timelines for two schedules.
Change/invariant and caption claim: Last-use release changes peak live bytes while arithmetic stays constant.
Scientific risk: Inputs, outputs and allocate-before-free convention must be explicit.

## 04-potential

Question: How can rare expensive operations have bounded aggregate cost?
Objects and arrow semantics: Trace buffer capacity staircase with copying events and a nonnegative potential ledger.
Change/invariant and caption claim: Unused capacity changes potential; copying is counted on resize.
Scientific risk: Amortized cost is not worst-case latency.

## 05-roofline

Question: Which bottleneck can a cost estimate suggest?
Objects and arrow semantics: Arithmetic-intensity versus attainable-throughput upper envelope with bandwidth and compute limits.
Change/invariant and caption claim: The lower bound on time is the maximum of compute and transfer bounds.
Scientific risk: No hardware prediction without measured effective rates and actual traffic.
