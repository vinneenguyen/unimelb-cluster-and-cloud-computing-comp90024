import sys
from pathlib import Path
import json
from collections import Counter
import re
from pprint import pprint

LANGNAMES = {'ar': 'Arabic', 'bn': 'Bengali', 'cs': 'Czech', 'da': 'Danish',
             'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish',
             'fa': 'Persian', 'fi': 'Finnish', 'fil': 'Filipino', 'fr': 'French',
             'he': 'Hebrew', 'hi': 'Hindi', 'hu': 'Hungarian', 'id': 'Indonesian',
             'it': 'Italian', 'ja': 'Japanese', 'ko': 'Korean', 'msa': 'Malay',
             'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese',
             'ro': 'Romanian', 'ru': 'Russian', 'sv': 'Swedish', 'th': 'Thai',
             'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu', 'vi': 'Vietnamese',
             'zh-cn': 'Chinese Simplified', 'zh-tw': 'Chinese Traditional'}


def remove_trails(text):
    """
    Remove unwanted trailing characters from json text
    text: line of json text
    """

    text = text.rstrip()  # remove trailing whitespace (\n)
    text = re.sub(r"(?<=}),?]?}?$", "", text)  # remove unwanted trailing ',' ']' '}'

    return text


def parse_tweet(text):
    """
    Parse for Tweet Data Dictionary in json text, under field "doc"
    text: line of json text
    """

    try:
        data = json.loads(text)
        tweet = data["doc"]
    except json.decoder.JSONDecodeError:  # illegal text
        tweet = {}

    return tweet


def extract_hashtags(tweet):
    """
    Extract hashtags from Tweet Data Dictionary and convert to lowercase
    tweet: Tweet Data Dictionary
    """

    if not tweet:
        return []

    hashtags = tweet["entities"]["hashtags"]
    names = [tag["text"].lower() for tag in hashtags]  # lowercased hashtag names (without #)

    return names


def extract_language(tweet):
    """
    Extract language from Tweet Data Dictionary
    """

    return tweet.get("lang", "")


class Tweet:
    """Process line of json text for single tweet data"""

    def __init__(self, text):
        """
        text: line of json text
        """

        self.text = text

        # Tweet data
        text_clean = remove_trails(text)
        self.data = parse_tweet(text_clean)

        # Extract information
        self.hashtags = extract_hashtags(self.data)
        self.lang = extract_language(self.data)  # language


if __name__ == "__main__":
    root = Path(sys.argv[1])  # project directory

    # Data
    datafile = root / "data" / "tinyTwitter.json"
    with open(datafile, encoding="utf8") as f:
        lines = f.readlines()
    print(lines[0])  # 1st line
    print(lines[1])  # 2nd line
    print(lines[-1])  # last line

    # Test remove_trails(...)
    print(remove_trails('{"id":"1212","doc":{"_id":"1212"}},\n'))
    assert remove_trails('{"id":"1212","doc":{"_id":"1212"}},\n') == '{"id":"1212","doc":{"_id":"1212"}}'
    assert remove_trails('{"id":"1212","doc":{"_id":"1212"}}]}\n') == '{"id":"1212","doc":{"_id":"1212"}}'

    # Test remove_trails(...) real data
    lines_clean = list(map(remove_trails, lines))
    print(*lines_clean[:3], sep="\n")

    # Test parse_tweet(...)
    print(parse_tweet('{"id":"1212","doc":{"_id":"1212"}}'))
    assert parse_tweet('{"id":"1212","doc":{"_id":"1212"}}') == {"_id": "1212"}
    assert not parse_tweet('{"total_rows":215443567,"offset":211386044,"rows":[')  # illegal text -> empty tweet data

    # Test parse_tweet(...) real data
    tweets = [t for t in map(parse_tweet, lines_clean) if t]  # skip illegal lines
    pprint(tweets[-1])

    # Test extract_hashtags(...)
    hashcounts = Counter()
    for t in tweets:
        hashnames = extract_hashtags(t)
        hashcounts.update(hashnames)
    print(hashcounts)

    # Test extract_language(...)
    langcounts = Counter(map(extract_language, tweets))
    print(langcounts)

    # Test Tweet(...)
    tweets_pro = [t for t in map(Tweet, lines) if t.data]  # drop badly formatted lines

    # Count hashtags, languages
    hashcounts_pro = Counter()
    langcounts_pro = Counter()
    for t in tweets_pro:
        hashcounts_pro.update(t.hashtags)
        langcounts_pro[t.lang] += 1
    print(hashcounts_pro)
    print(langcounts_pro)
