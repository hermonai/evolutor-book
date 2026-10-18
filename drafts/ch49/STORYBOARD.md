# Chapter 49 figure storyboard

Author's design approval: 17 October 2026, before final prose/layout closure. This is a local author decision, not independent review. Incoming six concept leads were read and merged into the three mechanism plates below. Caption inference and boundaries are specified here and implemented in editable TikZ/TXT.

## 01-pressure

- Question: Which arrival owns an item when the queue is full?
- Objects/notation: Queue occupancy step trace, accepted A/B, rejected C and FIFO departures.
- Changing/unchanged semantics: Only accepted arrivals consume capacity; rejection preserves producer responsibility.
- Caption inference/scientific risk: Tick order is illustrative; item counts are not byte or measured latency bounds.
- Final review: inspect page at print size in color and grayscale; labels and line styles carry meaning without color.

## 02-recovery

- Question: What does an unresolved action permit after restart?
- Objects/notation: Absent/intent/completed state machine with labelled record and reconciliation transitions.
- Changing/unchanged semantics: Same-key pending lookup reconciles; completed lookup returns a copy of cached result.
- Caption inference/scientific risk: Local dispatch theorem is not external exactly-once execution or durable log implementation.
- Final review: inspect page at print size in color and grayscale; labels and line styles carry meaning without color.

## 03-code

- Question: Which source revision do patch tests certify?
- Objects/notation: Base A, patch P, test identity and concurrently changed base B.
- Changing/unchanged semantics: A-to-B mismatch forces reconciliation and retesting.
- Caption inference/scientific risk: Version diagram is not a repository transaction, sandbox or proof of patch correctness.
- Final review: inspect page at print size in color and grayscale; labels and line styles carry meaning without color.
