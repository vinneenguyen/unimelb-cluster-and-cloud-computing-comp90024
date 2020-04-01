from collections import Counter


def sum_counters(counters):
    """
    Add all counters together
    counters: collections.Counter objects
    """

    counts_all = Counter()
    list(map(counts_all.update, counters))

    return counts_all


if __name__ == "__main__":
    a = Counter('gallahad')  # a new counter from an iterable
    b = Counter({'red': 4, 'blue': 2})  # a new counter from a mapping
    c = Counter(cats=4, dogs=8)
    print(sum_counters([a, b, c]))
