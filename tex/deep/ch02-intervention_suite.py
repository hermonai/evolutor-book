def intervention_suite(model, ids, atol=1e-12):
    if ids.ndim != 2 or ids.shape[0] < 1 or ids.shape[1] < 2:
        raise ValueError("nonempty batch and prefix/future required")
    if ids.dtype != torch.long or ids.min() < 0 or ids.max() >= 4:
        raise ValueError("DNA token indices required")
    if not math.isfinite(atol) or atol < 0:
        raise ValueError("finite nonnegative tolerance required")
    # The existing helper performs +1-mod-V suffix interventions and restores mode.
    errors = [prefix_intervention_error(model, ids, prefix_length=t, vocab_size=4)
              for t in range(1, ids.shape[1])]
    if not all(math.isfinite(e) for e in errors):
        raise ValueError("non-finite intervention output cannot pass")
    return {"errors": errors, "maximum": max(errors), "passes": max(errors) <= atol,
            "atol": atol, "dtype": "float64 reference on CPU"}
