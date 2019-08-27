def random_sequence(a, m, r_0, size):
    r = r_0
    for _ in range(size):
        r = (a * r) % m
        yield r / m
