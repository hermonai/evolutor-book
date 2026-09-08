def seed_summary(values):
    values = tuple(float(v) for v in values)
    if len(values) < 2 or not all(math.isfinite(v) for v in values):
        raise ValueError("at least two finite values required")
    return {"individual": values, "mean": statistics.mean(values),
            "median": statistics.median(values), "sample_sd": statistics.stdev(values),
            "min": min(values), "max": max(values)}
