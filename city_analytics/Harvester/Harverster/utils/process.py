from textblob import TextBlob
import json
"""
input : a json
output: a json in our format
"""

def sentiment_analyse(input_json):
    text = input_json["text"]
    analyse = TextBlob(text)
    if analyse.sentiment.polarity > 0:
        return "positive"
    if analyse.sentiment.polarity == 0:
        return "neutral"
    else:
        return "negative"


def check_covid_related(input_json):
    """check if the tweet is related to COVID-19"""
    if any(str in json.dumps(input_json["text"]).lower() for str in (
            'coronavirus', 'covid', 'pandemic', 'epidemic', 'cases', 'confirmed', 'recovered', 'deaths',
            'health', 'vaccine', 'vaccination', 'symptom', 'social distance', 'fomite', 'outbreak',
            'community spread', 'contact tracing', 'martial law', 'self-quarantine', 'quarantine',
            'index case', 'super-spreader', 'superspreader', 'isolation', 'contagious', 'infections',
            'virus', 'covidsafe', 'safe', 'breathing', 'breath', 'fever', 'bodyache', 'fatigue', 'smell loss',
            'taste loss', 'nausea', 'cold','antibody','mers','sars')):
        return "True"
    else:
        return "False"


def build_json(input_json, sentiment=None, covid_related=False):
    """
    build json, add new entity sentiment, covid_related
    """
    create_at = input_json["created_at"]
    id = input_json["id"]
    id_str = input_json["id_str"]
    text = input_json["text"]

    entities = {}
    entities["hashtags"] = input_json["entities"]["hashtags"]
    # Represents other Twitter users mentioned in the text of the Tweet.
    entities["user_mentions"] = input_json["entities"]["user_mentions"]

    user = {}
    user["id"] = input_json["user"]["id"]
    user["id_str"] = input_json["user"]["id_str"]
    user["name"] = input_json["user"]["name"]
    user["screen_name"] = input_json["user"]["screen_name"]
    user["location"] = input_json["user"]["location"]
    # user‘s description, sometime a user may mention their location here
    user["description"] = input_json["user"]["description"]
    # account created date
    user["created_at"] = input_json["user"]["created_at"]
    # This field must be true for the current user to attach geographic data when using POST statuses / update
    user["geo_enabled"] = input_json["user"]["geo_enabled"]
    # When true, indicates that the user has a verified account.
    user["verified"] = input_json["user"]["verified"]

    place = None
    if input_json["place"] is not None:
        place = {}
        # ID representing this place.
        place["id"] = input_json["place"]["id"]
        # URL representing the location of additional place metadata for this place
        place["url"] = input_json["place"]["url"]
        place["place_type"] = input_json["place"]["place_type"]
        place["name"] = input_json["place"]["name"]
        place["full_name"] = input_json["place"]["full_name"]
        place["country_code"] = input_json["place"]["country_code"]
        place["country"] = input_json["place"]["country"]
        # A bounding box of coordinates which encloses this place.
        place["bounding_box"] = input_json["place"]["bounding_box"]

    # Number of times this Tweet has been retweeted
    retweet_count = input_json["retweet_count"]
    # Indicates approximately how many times this Tweet has been liked by Twitter users
    favorite_count = input_json["favorite_count"]
    # is_quote_status = input_json["is_quote_status"]
    # quoted_status_id = input_json["quoted_status_id"]
    # This field only surfaces when a Tweet contains a link. Content or media.
    # possibly_sensitive = input_json["possibly_sensitive"]
    lang = input_json["lang"]
    sentiment = sentiment
    covid_related = covid_related

    js = json.dumps(
        {"create_at": create_at, "id": id, "id_str": id_str, "text": text, "entities": entities, "user": user,
         "place": place, "retweet_count": retweet_count, "favorite_count": favorite_count,
         # "possibly_sensitive": possibly_sensitive,
         "lang": lang, "sentiment": sentiment, "covid_related": covid_related})
    return js


def process_json(input_json):
    """input: an json obj in original format"""
    sentiment = sentiment_analyse(input_json)
    covid_related = check_covid_related((input_json))
    js = build_json(input_json, sentiment, covid_related)
    return js


