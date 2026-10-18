# Chapter 43 figure decisions (before prose)

1. Immutable lineage DAG branches from a served baseline into rejected unsafe and served good candidates. Dashed serving-pointer transitions and solid parent edges have different meanings.
2. Lifecycle state machine with guard labels offline gates, bounded canary, CAS revision and authority. Rejected has no path to active; rollback targets only historically served retired objects.
3. Model-state compatibility timeline: old requests pin old artifact, new serving pointer admits new requests, incompatible switch requires drain/reset. Rollback changes future serving identity and cannot reverse past tool effects.
