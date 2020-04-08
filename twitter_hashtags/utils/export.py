from collections import Counter

from utils.twitter import LANGNAMES


def print_hashcounts(hashcounts, top=None):
    """
    Nicely print top most common hashtags and their counts in hashcounts
    hashcounts: Counter object of hashtag counts
    top: number of most common hashtags (defaults to all hashtags)
    """

    top = len(hashcounts) if not top else top  # defaults to full length of hashcounts

    print(f"Top {top} most common hashtags:")
    for i, (tag, count) in enumerate(hashcounts.most_common(top)):
        print(f"{i+1}. {tag}, {count}")


def print_langcounts(langcounts, top=None):
    """
    Nicely print top most common languages and their counts in langcounts
    langcounts: Counter object of language counts
    top: number of most common languages (defaults to all languages)
    """

    top = len(langcounts) if not top else top  # defaults to full length of langcounts

    print(f"Top {top} most common languages:")
    for i, (lang, count) in enumerate(langcounts.most_common(top)):
        print(f"{i+1}. {LANGNAMES.get(lang, 'Undefined')} ({lang}), {count}")


if __name__ == "__main__":
    # Test print_hashcounts(...)
    hashcounts = Counter(dict([('climatechange', 6), ('scottyfrommarketing', 6), ('auspol', 6), ('australiaburns', 5)]))
    print_hashcounts(hashcounts)

    # Test print_langcounts(...)
    langcounts = Counter(dict([('en', 832), ('und', 69), ('fr', 18), ('pt', 17), ('es', 16)]))
    print_langcounts(langcounts)
