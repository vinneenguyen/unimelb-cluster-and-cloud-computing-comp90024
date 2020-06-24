from textblob import TextBlob
import json
import ast
import math
import time

"""
input : a json
output: a json in our format
"""

pathSA4 = "SA4_area_coordinates.json"

with open("generate_localities.ipynb") as f:
    for line in f:
        js = json.loads(line)
        city_to_SA4 = ast.literal_eval(js['cells'][5]['outputs'][0]['text'][1])


def sentiment_analyse(input_json):
    text = input_json["text"]
    analyse = TextBlob(text)
    if analyse.sentiment.polarity > 0:
        return "positive"
    if analyse.sentiment.polarity == 0:
        return "neutral"
    else:
        return "negative"


def check_SA4_with_geo(input_json):
    """
        calculate the distance between the tweet geo location with the boundaries of each statistics area,
        return the area code with minimum distance. If the minimum distance is greater than 10 we treat it
        as not in Australia or location point is not accurate.
    """
    with open(pathSA4) as f:
        for line in f:
            SA4_json = json.loads(line)
    # longitude: [input_json['geo']['coordinates'][1]
    # latitude: input_json['geo']['coordinates'][0]
    input_geo_point = [input_json['geo']['coordinates'][1], input_json['geo']['coordinates'][0]]
    sa4_code = -1  # default -1
    min_distance = 999999999999
    for i in range(len(SA4_json['features'])):
        feature = SA4_json['features'][i]
        cur_sa4_code = feature['properties']['sa4_code_2016']
        for j in range(len(feature['geometry']['coordinates'])):
            coordinate = feature['geometry']['coordinates'][j]
            for k in range(len(coordinate[0])):
                try:
                    point = coordinate[0][k]  # point[0] : longitude, point[1] : latitude
                    cur_distance = math.sqrt(
                        (input_geo_point[0] - point[0]) ** 2 + (input_geo_point[1] - point[1]) ** 2)
                    if cur_distance < min_distance:
                        sa4_code = cur_sa4_code
                        min_distance = cur_distance
                except TypeError:
                    pass
    return -1 if min_distance > 10 else str(sa4_code) + ",geo"


def check_SA4_with_name(input_json):
    """1st: check tweet['place']['name'], this is going to provide the most accurate of the city name
       2nd: check tweet['user']['location']
       3rd: if still cannot match, return -1
    """
    if input_json['place'] is not None:
        try:
            city = input_json['place']['name'].split(" ")[0].lower()
            return str(city_to_SA4[city]) + ",name"
        except KeyError:
            try:
                city = input_json['user']['location'].split(',')[0].lower()
                # print(city)
                return str(city_to_SA4[city]) + ",name"
            except Exception:
                return -1
        except Exception:
            return -1
    else:
        try:
            city = input_json['user']['location'].split(',')[0].lower()
            return str(city_to_SA4[city]) + ",name"
        except KeyError:
            return -1


def check_SA4(input_json):
    if input_json['geo'] is not None:
        return check_SA4_with_geo(input_json)
    else:
        return check_SA4_with_name(input_json)


def check_covid_related(input_json):
    """check if the tweet is related to COVID-19"""
    if any(str in json.dumps(input_json["text"]).lower() for str in (
            'coronavirus', 'covid', 'pandemic', 'epidemic', 'cases', 'confirmed', 'recovered', 'deaths',
            'health', 'vaccine', 'vaccination', 'symptom', 'social distance', 'fomite', 'outbreak',
            'community spread', 'contact tracing', 'martial law', 'self-quarantine', 'quarantine',
            'index case', 'super-spreader', 'superspreader', 'isolation', 'contagious', 'infections',
            'virus', 'covidsafe', 'safe', 'breathing', 'breath', 'fever', 'bodyache', 'fatigue', 'smell loss',
            'taste loss', 'nausea', 'cold', 'antibody', 'mers', 'sars')):
        return "True"
    else:
        return "False"


def build_json(input_json, sentiment=None, covid_related=False, SA4_and_sorurce=None):
    """
    build json, add new entity sentiment, covid_related, SA4 code and SA4 source.
    """
    create_at = input_json["created_at"]
    # id = input_json["id"]
    id_str = input_json["id_str"]
    text = input_json["text"]

    # entities = None
    # if input_json["entities"]["hashtags"] is not None:
    #     entities = {}
    #     entities["hashtags"] = input_json["entities"]["hashtags"]

    user = {}
    user["id_str"] = input_json["user"]["id_str"]
    user["location"] = input_json["user"]["location"]
    # user["description"] = input_json["user"]["description"]
    geo = None
    if input_json["geo"] is not None:
        geo = input_json["geo"]
    place = None
    if input_json["place"] is not None:
        place = {}
        # ID representing this place.
        # place["id"] = input_json["place"]["id"]
        place["place_type"] = input_json["place"]["place_type"]
        place["name"] = input_json["place"]["name"]
        # place["full_name"] = input_json["place"]["full_name"]
        place["country_code"] = input_json["place"]["country_code"]
        # place["country"] = input_json["place"]["country"]
        # A bounding box of coordinates which encloses this place.
        # place["bounding_box"] = input_json["place"]["bounding_box"]

    lang = input_json["lang"]
    sentiment = sentiment
    covid_related = covid_related
    # sentiment = input_json["sentiment"]
    # covid_related = input_json["covid_related"]
    SA4 = -1
    SA4_source = None
    if SA4_and_sorurce != -1:
        SA4 = int(SA4_and_sorurce.split(",")[0])
        SA4_source = SA4_and_sorurce.split(",")[1]

    # SA3 = SA3
    # SA2 = SA2
    # js = json.dumps(
    #     {"create_at": create_at, "id_str": id_str, "text": text, "entities": entities, "user": user,
    #      "geo": geo, "place": place, "lang": lang, "sentiment": sentiment, "covid_related": covid_related, "SA4": SA4,
    #      "SA4_source": SA4_source})
    js = json.dumps(
        {"timestamp": round(time.time() * 1000), "create_at": create_at, "id_str": id_str, "lang": lang,
         "sentiment": sentiment, "covid_related": covid_related, "SA4": SA4, "SA4_source": SA4_source,
         "text": text, "user": user, "geo": geo, "place": place, })
    return js


def process_json(input_json):
    """input: an json obj in original format"""
    sentiment = sentiment_analyse(input_json)
    covid_related = check_covid_related((input_json))
    SA4_and_sorurce = check_SA4(input_json)
    js = build_json(input_json, sentiment, covid_related, SA4_and_sorurce)
    return js
