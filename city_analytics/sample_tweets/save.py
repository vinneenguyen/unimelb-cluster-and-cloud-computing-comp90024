import json
import couchdb
import sys


consumer_key = "1IN6rVE2D5fXZ3uUSkaKj6sH7"

consumer_secret = "wjHCDcwOlCnTNAoSsdrppK3bUz47BskNwq4GkpdU5qpMHmrqvo"

access_token = "775994541954347008-jANS08q8Nx38WaVIgfJi7eL6u0yWC9h"

access_token_secret = "B2SDzmUVMZvCEZrJgvBAXYbijXAveUmNAkJEs6GszRJ06"

# try and connect to the couchdb instance
try:
    server = "http://admin:password@172.26.131.173:5984/"
    couch = couchdb.Server(server)
    try:
        tweetdb = couch['twitter4']
    except:
        tweetdb = couch.create('twitter4')

except Exception as e:
    print('Connection unsuccessful')
    sys.exit()



with open('test_tweet.json') as f:
    lines = f.readlines()


print(len(lines))

for tweet in lines:
    try:
        data = json.loads(tweet)

    except json.decoder.JSONDecodeError: # illegal text
        tweet = {}

    try:
          # set the doc id
        doc = {
            '_id': data['id_str']
            }

        # update the rest of the json object into doc
        doc.update(data)

        (tweetdb.save(doc))
    except Exception as e:
        print(e)





# if __name__ == '__main__':

#     l = StdOutListener()
#     auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(access_token, access_token_secret)
#     stream = tweepy.Stream(auth, l)
#     stream.filter(locations=[110.95, -54.83, 159.29, -11.35])            

                                                                                                                                                   1,1           Top
