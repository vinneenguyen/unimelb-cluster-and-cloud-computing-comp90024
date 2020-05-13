import APIKEYS as keys
import collect as collect
import tweepy

# api = keys.set_authentication_key(keys.key_list, 0)
# todo : this file will be merged with 'get_tweets_by_userid'
i = 0
with open("../sources/user_id.txt") as f:
    users_id = []
    cnt = 0
    key_index = 0
    with open("../results/followers/follower_id.txt", 'a') as out:
        with open("../results/followers/index.txt", 'a') as out_index:
            for line in f:
                cnt += 1
                # print(str(cnt) + " : " + line)
                users_id.append(line)
                if cnt % 10 == 0:
                    out_index.flush()
                    followers = collect.get_followers_id(users_id,key_index)
                    key_index=followers[0]+1 # use next key
                    if key_index >= len(keys.key_list)-1:
                        key_index = 0
                    print("next key is : "+ str(key_index))
                    followers2 = list(set(followers[1:]))  # remove duplicate
                    out_index.write("finished : " + str(cnt) + " users\n")
                    for id in followers2:
                        out.write(str(id) + "\n")
                    out.flush()
                    users_id = []
                    print("finished : "+ str(cnt))
