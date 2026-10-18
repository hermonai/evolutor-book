# Approved author storyboard — Chapter 37

Incoming admission, mixed work, metrics, precision and quality/frontier questions are retained and combined in five specific plates.
1. Reservation: arena of eight page credits split into A=3, B=2 and three unreserved; allocated pages lie inside reservations.
2. Scheduling timeline: show actual computed trace for A(prompt5/output3), B(prompt1/output2), C(prompt3/output1), B=4 C=2. Prefill fills and decode rows have explicit token counts.
3. Prediction clock: final prefill consumes x2 and emits y0; next iteration consumes y0 and emits y1. TTFT and ITL use completion boundaries.
4. Quantization: normal values collide when one outlier sets INT8 scale; show numerical grid and saturation on a fixed calibration scale.
5. Margin: logits [1,.99] with epsilon .02 can reverse the winner; numerical and task gates plus load curves answer different questions.

Ticks are abstract scheduling boundaries, never milliseconds. Precision arrows distinguish stored representations from float64 arithmetic. No invented measured frontier is drawn.
