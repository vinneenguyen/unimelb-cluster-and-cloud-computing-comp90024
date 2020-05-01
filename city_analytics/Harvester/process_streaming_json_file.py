import json
import tweepy
import time

# as mentioned by rich on : https://canvas.lms.unimelb.edu.au/courses/17514/discussion_topics/189519
# this py file is going to:
# 1: filter all tweets with specific keywords from the streaming json file, get the users' id of these tweets
# 2. get most recent 200 tweets from those users (see function get_and_write_user_tweet_by_user_id)
# 3. get recent followers of those users, store the followers' id
# 4. repeat step 2 for the followers
# we assume the users' followers are all in Australia

# results: - It took 3 hours using 20 keys to get most recent 50 followers about 800 specific users.
#          - It took another several hours to get tweets from their followers
#          - A 70 MB streaming file can generate approximately 3 GB tweets in total.

# problems: - Require lots of key, each key can only request around 250 follower id in one period. The above test was
#             done using 20 developer accounts.
#           - We have to do the same process everyday otherwise we won't have enough time to analyse the streaming
#             files.

key_list = []
input_file = "27-Apr-1000am-aws.json"
output_file = "out2.json" # store tweets
# our keys
# 0
key_list.append({"consumer_key": "1IN6rVE2D5fXZ3uUSkaKj6sH7",
                 "consumer_secret": "wjHCDcwOlCnTNAoSsdrppK3bUz47BskNwq4GkpdU5qpMHmrqvo",
                 "access_token": "775994541954347008-jANS08q8Nx38WaVIgfJi7eL6u0yWC9h",
                 "access_token_secret": "B2SDzmUVMZvCEZrJgvBAXYbijXAveUmNAkJEs6GszRJ06"})

key_list.append({"consumer_key": "V8E2r2X5gsIR80C9B1fxwBPgE",
                 "consumer_secret": "SoD5ZUzMG2IIOqpYsXCWWskEcx7PWv64A3GYFqaOs2qDYMZf0f",
                 "access_token": "1253291081011093504-BoGx29VgnEIqFpc5BSxR9V8GAGbFTc",
                 "access_token_secret": "ASLlzPC7vA4td6Q82j6ZbxqCZtLc9e7SfBEuinanF52oZ"})

key_list.append({"consumer_key": "asn6yDRU4omWNS7YmcjnsLrAN",
                 "consumer_secret": "TtqUjoRCWv4SDDjabPqTzwO6RF3vgI21UvoOdkvdjPKstcoaLw",
                 "access_token": "1250402484226387968-siuKgew1AZL1dcUCgVunQYlXLUKSmB",
                 "access_token_secret": "zM6XC1BLlLC9luxjo2ge9SzboMPj9mVNal9hjiX0TYfNx"})


def set_authentication_key(key_list, n):
    current_key = key_list[n];
    consumer_key = current_key["consumer_key"]
    consumer_secret = current_key["consumer_secret"]
    access_token = current_key["access_token"]
    access_token_secret = current_key["access_token_secret"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    return api


def load_json():
    """
    load streaming json file
    :return: a list of users' id, only include user who has posted tweets related to those keywords
    """
    user_id = []
    with open(input_file, encoding="utf-8") as f:
        for line in f:
            try:
                json_str = json.loads(line.lower())
                text = json_str["text"]
                # keywords
                if any(str in json_str["text"] for str in (
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


def get_and_write_user_tweet_by_user_id(users_id):
    """
    get and write tweets by user id
    """
    key_index = 0
    api = set_authentication_key(key_list, key_index)
    with open(output_file, 'a') as f:
        for u_id in users_id:
            try:
                # twitter daily 500 millions tweets, total users 336 millions, average 1.5 tweets/per person per day.
                # we collect 100 days tweets from every user's timeline (from 10 Jan), collect most recent 150 or 200 tweets from every user.
                for t in tweepy.Cursor(api.user_timeline, user_id=u_id).items(200):
                    f.write(json.dumps(t._json))
                    f.write("\n")
            except tweepy.RateLimitError:
                if key_index == len(key_list) - 1:
                    key_index = 0
                else:
                    key_index += 1
                print("try to restart with new key")
                api = set_authentication_key(key_list, key_index)
                time.sleep(1000 / (len(key_list) - 1) + 1)
            except tweepy.error.TweepError or Exception:
                pass


def get_user_followers_id(users_id):
    """
    get users' followers id
    :return: a list of followers' id
    """
    key_index = 0
    api = set_authentication_key(key_list, 0)
    i = 0
    users_followers_id = []
    for user_id in users_id:
        try:
            for user in tweepy.Cursor(api.followers, user_id=user_id).items(50):
                i += 1
                print(i)
                print(user._json["id"])
                users_followers_id.append(user._json["id"])
        except tweepy.RateLimitError:
            if key_index == len(key_list) - 1:
                key_index = 0
            else:
                key_index += 1
            print("try to restart with new key")
            api = set_authentication_key(key_list, key_index)
            time.sleep(1000 / (len(key_list) - 1) + 1)
        except tweepy.error.TweepError or Exception:
            pass
    return users_followers_id


users_id = load_json()
print(users_id)
get_and_write_user_tweet_by_user_id(users_id)
print("finish writing user tweets")
print("start to get followers")
followers_id = get_user_followers_id(users_id);
print("finish getting followers")
get_and_write_user_tweet_by_user_id(followers_id)
print("finished")
