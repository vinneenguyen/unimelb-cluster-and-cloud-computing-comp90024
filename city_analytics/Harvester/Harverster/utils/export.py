import json
from cloudant.client import CouchDB

symptom_list = ['smell loss', 'taste loss', 'sore throat', 'difficulty breathing', 'joint pain']
covid_app_list = ['covid app', 'covid safe', ]
punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~…"""


def save_tweet(tweet, coviddb, covidsafedb, symptomdb):
    try:
        data = json.loads(tweet)
        # print(data)
    except json.decoder.JSONDecodeError:  # illegal text
        pass
    except Exception as e:
        print(e)

    try:
        # check sentiment, add sentiment as a partition key
        if data['SA4'] != -1:
            if data['SA4_source'] == 'geo':
                doc = {'_id': "geo:" + data['id_str']}
            else:
                doc = {'_id': "name:" + data['id_str']}
        else:
            doc = {'_id': "none:" + data['id_str']}
        # update the rest of the json object into doc
        doc.update(data)

        try:
            if any(s in data["text"].translate(
                    data["text"].maketrans(punctuation, " " * len(punctuation))).lower().split(" ") for s in (
                           'fever', 'bodyache', 'fatigue', 'vomit', 'diarrhoea', 'headache', 'tiredness',
                           'nausea', 'cough')):
                symptomdb.save(doc)
            elif any(s in data["text"].lower() for s in symptom_list):
                symptomdb.save(doc)
        except Exception as e:
            print("symptom : " + str(e))

        try:
            if any(s in data["text"].lower().split(" ") for s in (
                    'covidsafe', 'covidapp', 'covidapp')):
                covidsafedb.save(doc)
            elif any(s in data["text"].lower() for s in covid_app_list):
                covidsafedb.save(doc)
        except Exception as e:
            print("covidsafe :" + str(e))
        print("saved: " + tweet)
        coviddb.save(doc)
    except Exception as e:
        print("tweet : " + str(e))


def create_db(mydb, couch_server):
    try:
        couch_server[mydb]
    except KeyError:
        couch_server.create_database(mydb, partitioned=True)


def get_db(mydb, couch_server):
    try:
        db = couch_server[mydb]
    except:
        db = couch_server.create(mydb)
    return db
