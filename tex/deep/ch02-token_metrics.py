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
