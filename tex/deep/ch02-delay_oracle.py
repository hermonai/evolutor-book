def delay_oracle(sequence, lag):
    if type(lag) is not int or lag < 1 or lag >= len(sequence):
        raise ValueError("lag must leave at least one scored position")
    return tuple(sequence[:-lag])
