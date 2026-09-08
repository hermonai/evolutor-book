def token_metrics(logits, targets):
    """Unweighted next-base loss; all supplied positions are scored."""
    if logits.ndim != 3 or targets.shape != logits.shape[:2] or targets.numel() == 0:
        raise ValueError("expected nonempty logits [B,T,V] and targets [B,T]")
    if not torch.isfinite(logits).all():
        raise ValueError("non-finite logits")
    if targets.dtype != torch.long or targets.min() < 0 or targets.max() >= logits.shape[-1]:
        raise ValueError("target indices outside vocabulary")
    loss = F.cross_entropy(logits.reshape(-1, logits.shape[-1]), targets.reshape(-1))
    nats = float(loss)
    return {"nats_per_base": nats, "perplexity": math.exp(nats),
            "bits_per_base": nats / math.log(2),
            "accuracy": float((logits.argmax(-1) == targets).double().mean())}

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

def delay_oracle(sequence, lag):
    if type(lag) is not int or lag < 1 or lag >= len(sequence):
        raise ValueError("lag must leave at least one scored position")
    return tuple(sequence[:-lag])

def seed_summary(values):
    values = tuple(float(v) for v in values)
    if len(values) < 2 or not all(math.isfinite(v) for v in values):
        raise ValueError("at least two finite values required")
    return {"individual": values, "mean": statistics.mean(values),
            "median": statistics.median(values), "sample_sd": statistics.stdev(values),
            "min": min(values), "max": max(values)}
