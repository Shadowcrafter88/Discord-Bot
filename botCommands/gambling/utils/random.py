import secrets

from collections.abc import Sequence, Set
from copy import copy

choice = secrets.choice
randbits = secrets.randbits


def sample(population, k):
    """Chooses k unique random elements from a population sequence or set."""
    if isinstance(population, Set):
        population = tuple(population)
    if not isinstance(population, Sequence):
        raise TypeError(
            "Population must be a sequence or set.  For dicts, use list(d)."
        )

    n = len(population)
    population = copy(population)

    if not 0 <= k <= n:
        raise ValueError("Sample larger than population or is negative")

    results = []
    for i in range(k):
        results.append(population.pop(secrets.randbelow(n - i)))

    return results


def shuffle(population):
    """Returns a shuffled list"""
    return sample(population, len(population))


def randint(a, b):
    """Return random integer in range [a, b], including both end points."""
    a, b = int(a), int(b)
    return secrets.randbelow(b - a + 1) + a
