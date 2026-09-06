# Canonical planning data

curriculum.json is the editable chapter architecture. book-i-contract.json is the identical planned Book I exit contract shared by both repositories. The contract is not active evidence of teaching.

Run scripts/build_pedagogy.py from the repository root to regenerate maps and inventories. figure-inventory.json and animation-inventory.json are generated plans; their statuses explicitly distinguish uncreated assets. No manuscript chapters are generated.

Every local prerequisite must precede its consumer. Book II imports refer only to named Book I contract chapters. Update both contract copies together; the paired repository check detects drift when both checkouts are available.
