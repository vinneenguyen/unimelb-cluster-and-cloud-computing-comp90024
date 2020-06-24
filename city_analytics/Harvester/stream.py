from cloudant.client import CouchDB
import utils.APIKEYS as keys
import utils.process as process
import utils.export as export
import tweepy
import couchdb
import json
import time
import os

users = set()
key_len = len(keys.key_list)

with open("sources/all-unique-users.txt") as f:
    for line in f:
        users.add(line)


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        """Called when raw data is received from connection.
            store the new tweet into couchDB
            store new users into a file, the file is name by date under specific folder:
            ie. new-users-24.txt under folder May-2020
        """
        global users
        # todo: clean the tweet then store the data into couch db & local disk
        js = json.loads(process.process_json(json.loads(data)))
        try:
            # if js["covid_related"] == "True":  # set the doc id
            export.save_tweet(json.dumps(js), coviddb, covidsafedb, symptomdb)
            # else:
        except Exception as e:
            print(e)

        user_id = js["user"]["id_str"]
        if user_id not in users:
            users.add(user_id)
            date = time.strftime("%d-%H")
            # the folder path use to store new users
            dir_path = os.path.join(os.path.abspath('.'), 'new-users/' + time.strftime("%B-%Y"))
            # this is called at the first time receiving new tweet each month, create a folder with respect to that
            # month to store new users for that month.
            if os.path.exists(dir_path) == False:
                os.mkdir(dir_path)
                print("folder: " + dir_path + " created!")
            # write new user ids into a file, the file is named by the date of current day
            with open("new-users/" + time.strftime("%B-%Y") + "/new-user-" + date + ".txt", 'a') as out:
                with open("sources/all-unique-users.txt", 'a') as out2:
                    out2.write(str(user_id) + "\n")
                    out.write(str(user_id) + "\n")
                    out.flush()
                    out2.flush()
                print(len(users))
        return True


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

api = keys.get_api(keys.key_list, 0)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

# add a filter to collect tweets in Australia
myStream.filter(locations=[110.46, -44.02, 154.46, -11.695])
