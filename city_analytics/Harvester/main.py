import schedule
import os


def run_collect_tweet():
    os.system("python3 collect_tweet.py")


# start collecting tweets from new users of that day
# run everyday 11:55 pm
schedule.every().day.at("23:55").do(run_collect_tweet)

while True:
    schedule.run_pending()
