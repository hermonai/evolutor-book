# Chapter 45 author technical audit

Local author review only. Retains original Alice/Bob same-object, foreign
capability, malicious text, quota and redacted-audit scenarios. The original
nonce was neither authenticated nor checked for issuance; the replacement
requires exact registry object, session, action/resource, expiry, epoch and
current grant. A copied equal dataclass fails. This is trusted-process misuse
protection, never a cryptographic token or defense against malicious Python.
Integer time is trusted monotonic input; policy replacement revokes all old
capabilities. Calls are serialized, so production check/effect races remain open.

Structured cache encoding fixes delimiter aliasing, but does not make digest
collisions, cache poisoning or stored-envelope verification disappear. Cache
payload handling is a stated integration contract, not implemented by a key
function. Logical-value noninterference explicitly excludes global capacity,
timing and hardware observations. The shared-quota counterexample falsifies a
stronger availability claim. Vector quota checks all dimensions before mutation;
release requires exact issued reservation once. Object overwrite is distinct
from allocating a new object. Quotas are not fairness/deadline guarantees.

Only in-memory echo exists and the closed argument schema rejects extras.
Untrusted text never enters the authority predicate; that is not an attack
recognizer. Authorization precedes object fetch. Audit omits values/full resource
IDs and distinguishes decision from operation success; it is a mutable list,
not immutable tamper-proof storage. Secret scanners and namespace checks cannot
certify secure device erase or eliminate shared-device side channels.

Chapter32/33 pool lifetime, Chapter36 pages, Chapter37 lanes, Chapter40 memory
and Chapter41 effects require their actual final interfaces. They are not
silently substituted or imported while sibling batches change. No live system,
credential, outside tool, security account or finance repository was touched.
Three TikZ/TXT plates and source-bound tests/renders are local evidence only.
