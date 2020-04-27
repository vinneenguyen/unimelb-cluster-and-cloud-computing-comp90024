import tweepy
import json
import couchdb
import sys

consumer_key = "1IN6rVE2D5fXZ3uUSkaKj6sH7"

consumer_secret = "wjHCDcwOlCnTNAoSsdrppK3bUz47BskNwq4GkpdU5qpMHmrqvo"

access_token = "775994541954347008-jANS08q8Nx38WaVIgfJi7eL6u0yWC9h"

access_token_secret = "B2SDzmUVMZvCEZrJgvBAXYbijXAveUmNAkJEs6GszRJ06"

# try and connect to the couchdb instance
try:
    server = 'INPUT couchdb server'
    couch = couchdb.Server(server)
    # tweetdb = couch.create('tweet')
    tweetdb = couch['tweet']

except Exception as e:
    print('Connection unsuccessful')
    sys.exit()


# This is the listener, responsible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

        try:
            # set the doc id
            doc = {
                '_id': decoded['id_str']
            }
            # update the rest of the json object into doc
            doc.update(decoded)

            print(tweetdb.save(doc),'\n')
        except Exception as e:
            print(e)
            print()
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, l)
    stream.filter(locations=[110.95, -54.83, 159.29, -11.35])
