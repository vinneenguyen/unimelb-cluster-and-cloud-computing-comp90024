import tweepy

key_list = [{"consumer_key": "1IN6rVE2D5fXZ3uUSkaKj6sH7",
             "consumer_secret": "wjHCDcwOlCnTNAoSsdrppK3bUz47BskNwq4GkpdU5qpMHmrqvo",
             "access_token": "775994541954347008-jANS08q8Nx38WaVIgfJi7eL6u0yWC9h",
             "access_token_secret": "B2SDzmUVMZvCEZrJgvBAXYbijXAveUmNAkJEs6GszRJ06"},
            {"consumer_key": "V8E2r2X5gsIR80C9B1fxwBPgE",
             "consumer_secret": "SoD5ZUzMG2IIOqpYsXCWWskEcx7PWv64A3GYFqaOs2qDYMZf0f",
             "access_token": "1253291081011093504-BoGx29VgnEIqFpc5BSxR9V8GAGbFTc",
             "access_token_secret": "ASLlzPC7vA4td6Q82j6ZbxqCZtLc9e7SfBEuinanF52oZ"},
            {"consumer_key": "asn6yDRU4omWNS7YmcjnsLrAN",
             "consumer_secret": "TtqUjoRCWv4SDDjabPqTzwO6RF3vgI21UvoOdkvdjPKstcoaLw",
             "access_token": "1250402484226387968-siuKgew1AZL1dcUCgVunQYlXLUKSmB",
             "access_token_secret": "zM6XC1BLlLC9luxjo2ge9SzboMPj9mVNal9hjiX0TYfNx"},
            {"consumer_key': 'irCPmhuFx4dcLcK6YsrzOXXYa",
             "consumer_secret': 'mwdFyjK0CBuDSF4lrMJKnNlOQxafAnXblHEynJuFjlbyhDkv0v",
             "access_token': '1261882567764000769-hUlP9daIp8oXXSDjb2ye0o4dyJHbgD",
             "access_token_secret': 'j3wd47x1o4wXA6IDPFvY1rkoxK2XKUuI80tTgYTMO6x4g"}]


def get_api(key_list, n, wait_on_rate_limit=False, wait_on_rate_limit_notify=False):
    current_key = key_list[n];
    consumer_key = current_key["consumer_key"]
    consumer_secret = current_key["consumer_secret"]
    access_token = current_key["access_token"]
    access_token_secret = current_key["access_token_secret"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=wait_on_rate_limit,
                     wait_on_rate_limit_notify=wait_on_rate_limit_notify)
    return api
