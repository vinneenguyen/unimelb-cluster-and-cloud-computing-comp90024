import tweepy


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        """Called when raw data is received from connection.

            write the received data into a file
        """
        try:
            with open('25-Apr-2030pm.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True


API_Key2 = "V8E2r2X5gsIR80C9B1fxwBPgE"
API_Secret_Key2 = "SoD5ZUzMG2IIOqpYsXCWWskEcx7PWv64A3GYFqaOs2qDYMZf0f"
Access_Token2 = "1253291081011093504-BoGx29VgnEIqFpc5BSxR9V8GAGbFTc"
Access_Token_key = "ASLlzPC7vA4td6Q82j6ZbxqCZtLc9e7SfBEuinanF52oZ"

auth = tweepy.OAuthHandler(API_Key2, API_Secret_Key2)
auth.set_access_token(Access_Token2, Access_Token_key)

api = tweepy.API(auth)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
#track=['job', 'covid'],


myStream.filter(locations=[110.46,-44.02,154.46,-11.695])
