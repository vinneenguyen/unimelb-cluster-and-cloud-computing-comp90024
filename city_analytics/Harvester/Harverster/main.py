import tweepy
import Twitter.unimelb.utils.APIKEYS as keys


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        """Called when raw data is received from connection.

            write the received data into a file
        """
        # todo: clean the tweet then store the data into couch db & local disk
        try:
            with open('25-Apr-2030pm.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error :" % str(e))
        return True


api = keys.get_api(keys.key_list, 0)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

myStream.filter(locations=[110.46, -44.02, 154.46, -11.695])
# todo : get stream user id, follower id, check their id with "sources/users/all-unique-users.txt"
#        if it is a new user, get their tweets, append their id to 'all-unique-users.txt'
#        clean store in couch db
