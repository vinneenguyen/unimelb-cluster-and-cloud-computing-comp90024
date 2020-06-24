from threading import Thread
import json
import utils.collect as collect
import math


# This file is used to collect tweets for a given topic.
#
# Input parameters in json format, includes: topic, keywords, and a list twitter developer accounts.
#
# The number of threads used to collect only depends on the number of developer accounts
# provided, every 4 accounts for 1 thread to achieve maximum efficiency.
# ie, 4 accounts 1 thread, 6 accounts 2 thread, 12 accounts 3 threads etc.
#
# Loads for each thread depends on the number of accounts that the thread is allocated, that is more accounts
# more loads to keep workload balance.

class myThread(Thread):
    def __init__(self, user_index, key_index, thread_id, users_ids, topic, keywords, accounts):
        Thread.__init__(self)
        self.user_index = user_index
        self.key_index = key_index
        self.thread_id = thread_id
        self.users_ids = users_ids
        self.topic = topic
        self.keywords = keywords
        self.accounts = accounts
        print('threadID:', thread_id, ' start.')

    def run(self):
        print("thread : " + str(self.thread_id) + " gets" + str(self.user_index[0]) + " to " + str(self.user_index[1]))
        print(
            "thread : " + str(self.thread_id) + " gets keys" + str(self.key_index[0]) + " to " + str(self.key_index[1]))
        line_index = 0
        ids = []
        # specify key for each thread
        key_index = self.key_index[0]
        key_start = self.key_index[0]
        key_end = self.key_index[1]
        # each thread write tweets into its own files
        with open(self.topic + "_tweets-thread-" + str(self.thread_id) + ".json", 'a') as out:
            with open(self.topic + "_status-thread-" + str(self.thread_id) + ".txt", 'a') as out_status:
                for id in self.users_ids:
                    line_index += 1
                    # a thread only process the ids in its allocated range
                    if line_index < self.user_index[0]:
                        continue
                    elif line_index > self.user_index[1]:
                        break
                    ids.append(id)
                    if line_index % 10 == 0:
                        # get tweets
                        tweets = collect.get_tweets_by_user_ids(ids, key_index, key_start, key_end,
                                                                accounts=self.accounts,
                                                                keywords=self.keywords)
                        for tweet in tweets[1:]:
                            if tweet['place'] is not None and tweet['place']['country_code'] != "AU":
                                continue
                            out.write(json.dumps(tweet) + "\n")
                        key_index = tweets[0] + 1  # use next key
                        if key_index > key_end:
                            key_index = key_start
                        print("next key is : " + str(key_index))
                        out_status.write("finished : " + str(line_index) + " users\n")
                        out.flush()
                        out_status.flush()
                        ids = []
                        print("finished : " + str(line_index))


def allocate_key(accounts_len, num):
    """ allocate keys to each thread
    rules: keys are not uniformly distributed, try best to give each thread 4 keys firstly
    ie. 10 keys: [0,3],[4,7],[8,9]
        9 keys: [0,3],[4,7],[8,8]
        8 keys: [0,3],[4,7] etc.
    """
    res = []
    for i in range(num):
        if i == num - 1:
            sub_res = [i * 4, accounts_len - 1]
            res.append(sub_res)
        else:
            sub_res = [i * 4, i * 4 + 3]
            res.append(sub_res)
    return res


def allocate_users(users_len, accounts_len):
    """ allocate users to each thread, loads are not uniformly distributed
        a thread with more keys will be allocated more loads
    """
    res = []
    num = math.ceil(accounts_len / 4)
    chunk_size = math.ceil(users_len / accounts_len)
    for i in range(num):
        if i == num - 1:
            sub_res = [chunk_size * i * 4, users_len]
            res.append(sub_res)
        else:
            sub_res = [chunk_size * i, chunk_size * (i + 4) - 1]
            res.append(sub_res)
    return res


def main(user_file, input_parameter):
    """
    :param user_file: a file of unique users ids
    :param input_parameter: input in designed json format
    :return: multiple json files of tweets related to the specific topic
    """
    # read parameters from parameter file
    with open(input_parameter) as input:  # read input parameters
        for line in input:
            parameters_json = json.loads(line)

    topic = parameters_json["topic"]
    keywords = parameters_json["keywords"]
    accounts = []
    users_ids = []
    for key in parameters_json['accounts']:
        accounts.append(key)

    with open(user_file) as f:
        for line in f:
            users_ids.append(line)

    num_thread = math.ceil(len(accounts) / 4)

    divided_keys = allocate_key(len(accounts), num_thread)  # allocate keys to each threads
    divided_users = allocate_users(len(users_ids), len(accounts))  # allocate users ids to each thread
    for i in range(num_thread):
        t = myThread(divided_users[i], divided_keys[i], i, users_ids, topic, keywords, accounts)
        t.start()


if __name__ == "__main__":
    user_file = "sources/all-unique-users.txt"
    input_parameter = "sources/input_parameter"
    main(user_file, input_parameter)
