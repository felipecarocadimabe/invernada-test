from itertools import cycle


def calculate_dv(rut_without_db):
    reverse = map(int, reversed(str(rut_without_db)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(reverse, factors))
    return (-s) % 11

