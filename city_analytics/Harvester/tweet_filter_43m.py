import tweepy
import json

# This file is used to filter the tweets from the large 43 million tweet file. Basically, two steps are used.
# 1. Firstly check if the user has the location service on, if so, check the 'place' parameter to filter the tweets with
# country code 'AU' or country 'Australia'. If the user turn on the location service, there is no need to further check
# the user's profile, text, description etc.
# 2. In the case the user turn off the location, check the user's profile, description and the content about the tweets.
# These information are matched with a list of keywords, if anyone keyword is matched, we then treat the user as in
# Australia and record it.

# only 1 key is enough for this process.


out_tweet_file = "out_tweet2.json" # store tweets in Australia
out_user_id = "out_user_id2.txt" # store Australian users id
count = 0

tweet_ids = []


def lookup_tweets(tweet_IDs, api):
    with open(out_tweet_file, 'a') as out_tweet:
        with open(out_user_id, 'a') as out_id:
            full_tweets = []
            tweet_count = len(tweet_IDs)
            try:
                for i in range(int(tweet_count / 100) + 1):
                    # Catch the last group if it is less than 100 tweets
                    end_loc = min((i + 1) * 100, tweet_count)
                    # full_tweets.extend()
                    tmp_statues_list = api.statuses_lookup(id_=tweet_IDs[i * 100:end_loc])
                    for status in tmp_statues_list:
                        # first check whether the user has turn on the location service, if so, we only need to check
                        # their locations, there is no need to further check their profiles.
                        if status._json["place"] is not None:
                            if status._json["place"]["country_code"] == 'AU' or status._json["place"]["country"] == 'Australia':
                                full_tweets.append(status._json)
                                out_tweet.write(json.dumps(status._json))
                                out_tweet.write("\n")
                                out_id.write(status._json["user"]["id_str"] + "\n")
                            continue
                        # if the user turn off the location service, check their profile to decide whether they are in
                        # Australia or not. We treat the user as in Australia if they mentioned some keywords about
                        # Australia in there 'text', 'description' or 'location', this 'location' is different from the
                        # previous location. We have removed keyword 'victoria' because there are so many place in the
                        # world named victoria.
                        info_summary = (status._json["text"] + " " + status._json["user"]["description"] + " " +
                                        status._json["user"]["location"]).lower()
                        if status._json["lang"] == "en" and any(
                                str in info_summary for str in ('australia', 'melbourne', 'sydney', 'brisbane',
                                                                'adelaide', 'gold coast', 'goldcoast', 'gold-coast',
                                                                'canberra', 'south australia',
                                                                'hobart', 'darwin', 'cairns', 'perth',
                                                                'new south wales', 'western australia',
                                                                'queensland', 'australian capital territory',
                                                                'tasmania', 'australian', 'aussie')):
                            full_tweets.append(status._json)
                            out_tweet.write(json.dumps(status._json))
                            out_tweet.write("\n")
                            out_id.write(status._json["user"]["id_str"] + "\n")
                return full_tweets
            except tweepy.error.RateLimitError:
                print("reach limit")
            except tweepy.TweepError:
                print('error')


consumer_key = '9jkA4TZaE85RW1ChGzs3NotrI'
consumer_secret = 'pDbJcjlcZ4hKT7n7jNT9YSRKPIVNf7aIegdzthGwtb1eg97nlc'
access_token = '988328066442117121-57t34wyyj2PmUP43KDe4Rpf6VZTqSvq'
access_token_secret = 'd3IvraqYRY12IWhU1xFuhzpLnz98B1pF4uy23QzOs6epl'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

with open("all.csv") as f:
    with open("status.txt", 'a') as out_status: # this file is used as an indicator of task progress.
        index = 0
        index_wan = 0
        total = 43311762
        for line in f:
            try:
                tweet_id = line.split(",")[0]
                tweet_ids.append(tweet_id)
            except Exception:
                pass
            index += 1
            if index == 1001 or index_wan * 1000 + index == total:
                lookup_tweets(tweet_ids, api)
                index = 0
                index_wan += 1
                tweet_ids = []
                out_status.write("finish : " + str(index_wan) + " 000 \n")
                print("finish : ", str(index_wan), " 000")
                out_status.flush()


print("all finished")
