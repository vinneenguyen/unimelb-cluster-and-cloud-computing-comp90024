import tweepy
import json
import time
import utils.APIKEYS as keys

# default keywords for our topic COVID-19
default_keywords = ['coronavirus', 'covid', 'pandemic', 'epidemic', 'cases', 'confirmed', 'recovered', 'deaths',
                    'health', 'vaccine', 'vaccination', 'symptom', 'social distance', 'fomite', 'outbreak',
                    'community spread', 'contact tracing', 'martial law', 'self-quarantine', 'quarantine',
                    'index case', 'super-spreader', 'superspreader', 'isolation', 'contagious', 'infections',
                    'virus', 'covidsafe', 'safe', 'breathing', 'breath', 'fever', 'bodyache', 'fatigue',
                    'smell loss', 'taste loss', 'nausea', 'cold', 'antibody', 'mers', 'sars']


# 1.2 GB csv file
def extract_tweets_from_csv(tweet_IDs, api):
    """
    collect tweets from the 1.2 GB csv file
    """

    out_tweet_file = "json_day1_38.json"  # output file for extract_tweets_from_csv
    out_user_id = "out_user_id2.txt"  # output file for extract_tweets_from_csv
    count = 0
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
                            if status._json["place"]["country_code"] == 'AU' or \
                                    status._json["place"]["country"] == 'Australia':
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
                pass


# normal tweet
def load_json():
    """
    load streaming json file
    :return: a list of users' id, only include user who has posted tweets related to those keywords
    """
    user_id = []
    input_file = "27-Apr-1000am-aws.json"  # input file for load_json
    output_file = "user-tweets-by-id.json"  # output file for get_and_write_user_by_user_id
    with open(input_file, encoding="utf-8") as f:
        for line in f:
            try:
                json_str = json.loads(line.lower())
                text = json_str["text"]
                # keywords
                if any(s in json_str["text"] for s in (
                        'coronavirus', 'covid', 'pandemic', 'epidemic', 'cases', 'confirmed', 'recovered', 'deaths',
                        'health', 'vaccine', 'vaccination', 'symptom', 'social distance', 'fomite', 'outbreak',
                        'community spread', 'contact tracing', 'martial law', 'self-quarantine', 'quarantine',
                        'index case', 'super-spreader', 'superspreader', 'isolation', 'contagious', 'infections',
                        'virus')):
                    user_id.append(json_str["user"]["id"])
            except Exception:
                pass
    print("total " + str(len(user_id)) + " ids in this file")
    f.close()
    return user_id


def get_tweets_by_user_ids(user_ids, current_key, key_start, key_end, accounts=keys.key_list, keywords=default_keywords,
                           since_id=1256191641607647236):
    """
        get all tweets from a lsit of users
        return all tweets in a list
    :param user_ids: a list of user ids
    :param current_key: the current key used for Twitter api
    :param accounts: twitter account credentials
    :param keywords: keywords related to topic
    :return: a list of tweets of these users
    """
    key_list = accounts
    key_index = current_key
    api = keys.get_api(key_list, key_index)
    tweets = []
    #                   1233495710621995014 : 28 Feb 2020
    #                   1236083901673570304 : 7 Mar 2020
    #                   1245310749045653504 : 1 Apr 2020
    #                   1256191641607647236 : 1 May 2020
    for id in user_ids:
        try:
            t = tweepy.Cursor(api.user_timeline, user_id=id,
                              since_id=since_id).items()
            for tweet in t:
                if any(s in json.dumps(tweet._json["text"]).lower() for s in keywords):
                    # the harvester only collect tweets in Australia
                    if tweet._json['place'] is not None and tweet._json['place']['country_code'] != "AU":
                        continue
                    tweets.append(tweet._json)
        except tweepy.error.RateLimitError:
            key_len = key_end - key_start
            if key_index == key_end:
                key_index = key_start
            else:
                key_index += 1
            print("try to restart with new key: " + str(key_index))
            api = keys.get_api(key_list, key_index)
            time_sleep = 0  # if key number is larger than 4, there is no need to stop harvester
            if key_len < 4:
                # stop a certain amount time to avoid api keep hitting the limit
                time_sleep = (4 - key_len) * 225 / key_len
            time.sleep(time_sleep)
            continue
        except Exception as e:
            print(e)
            continue
    tweets.insert(0, key_index)
    return tweets


def get_followers_ids(users_id, key_index):
    """
    @:param users_id : a list of users id
    get users' followers id
    :return: a list of followers' id
    """
    api = keys.get_api(keys.key_list, key_index)
    followers_id = []
    for user_id in users_id:
        try:
            # followers = tweepy.Cursor(api.followers, user_id=user_id).items(50)
            # for follower in followers:
            for follower in tweepy.Cursor(api.followers, user_id=user_id, count=10).items(10):
                js = follower._json
                if "status" in js:
                    if js['status']['place'] is not None and js['status']['place']['country_code'] == 'AU':
                        followers_id.append(follower._json["id"])
        except tweepy.RateLimitError:
            print("finished key:" + str(key_index) + "  waiting for a new key")
            if key_index == len(keys.key_list) - 1:
                key_index = 0
            else:
                key_index += 1
            api = keys.get_api(keys.key_list, key_index)
            time.sleep(900 / (len(keys.key_list)) + 1)
            continue
        except tweepy.error.TweepError or Exception:
            pass
    followers_id.insert(0, key_index)  # append the current key to the list
    return followers_id
