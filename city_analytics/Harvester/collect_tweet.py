import time
import utils.collect as collect
import utils.process as process
import utils.export as export
from cloudant.client import CouchDB
import couchdb


def main(users):
    users_id = []
    cnt = 0
    key_start = 0
    key_end = 3
    key_index = key_start
    for user in users:
        cnt += 1
        users_id.append(user)
        if cnt % 2 == 0:
            tweets = collect.get_tweets_by_user_ids(users_id, key_index, key_start, key_end)
            for tweet in tweets[1:]:
                print(type(tweet))
                if tweet['place'] is not None and tweet['place']['country_code'] != "AU":
                    continue
                js = process.process_json(tweet)
                export.save_tweet(js, coviddb, covidsafedb, symptomdb)
            key_index = tweets[0] + 1  # use next key
            if key_index >= key_end:
                key_index = key_start
            print("next key is : " + str(key_index))
            users_id = []
            print("finished : " + str(cnt))


# couchDB server
server_addr = "172.26.131.173" # todo dynamic ip
client = CouchDB("admin", "password", url='http://' + server_addr + ':5984', connect=True)
mydb1 = "tweet-covid" #
mydb2 = "tweet-covid-symptom" #
mydb3 = "tweet-covid-covidsafe" #

# create databases if not exist
export.create_db(mydb1, client)
export.create_db(mydb2, client)
export.create_db(mydb3, client)

# get databases
try:
    couch_server = couchdb.Server("http://admin:password@" + server_addr + ":5984/")
    coviddb = export.get_db(mydb1, couch_server)
    covidsafedb = export.get_db(mydb2, couch_server)
    symptomdb = export.get_db(mydb3, couch_server)
except Exception as e:
    print('Connection unsuccessful')
    print(e)

# get the new users file for current day
path = "new-users/" + time.strftime("%B-%Y") + "/new-user-" + time.strftime("%d-%H") + ".txt"
users = set()
with open(path) as f:
    for line in f:
        users.add(line)
try:
    main(users)
except Exception as e:
    print(e)