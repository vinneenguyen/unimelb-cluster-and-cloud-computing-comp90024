import Twitter.unimelb.utils.collect as collect
import Twitter.unimelb.utils.process as process
import json
# todo: this file is going to be merged with 'get_followers_by_userid'


input_json = ""
input_user_id = "stream_unique_user.txt"
output_json = "t3.json"
out_status = "t.txt"


def main():
    with open(input_user_id) as f:
        users_id = []
        cnt = 0
        key_start = 0
        key_end = 4
        key_index = key_start
        with open(output_json, 'a') as out:
            with open(out_status, 'a') as out_index:
                for line in f:
                    cnt += 1
                    # print(str(cnt) + " : " + line)
                    users_id.append(line)
                    if cnt % 10 == 0:
                        tweets = collect.get_tweets_by_user_ids(users_id, key_index, key_start, key_end)
                        for tweet in tweets[1:]:
                            if tweet['place'] is not None and tweet['place']['country_code'] != "AU":
                                continue
                            out.write(process.process_json(tweet) + "\n")
                        key_index = tweets[0] + 1  # use next key
                        if key_index >= key_end:
                            key_index = key_start
                        print("next key is : " + str(key_index))
                        out_index.write("finished : " + str(cnt) + " users\n")
                        out.flush()
                        out_index.flush()
                        users_id = []
                        print("finished : " + str(cnt))

if __name__ == "__main__":
    main()
