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
             "access_token_secret": "zM6XC1BLlLC9luxjo2ge9SzboMPj9mVNal9hjiX0TYfNx"}, {
                'consumer_key': 'bBAyCzuDVTwZ4a5cEdXZsCBtD',
                'consumer_secret': 'ULRqMIeXV4g5UZRsUYAutQLoA9KGc2LBgtzUm11J4DApoxIi1v',
                'access_token': '988328066442117121-ttz85CDp8aGRzs2AzmoeWAFJ1HQrFmq',
                'access_token_secret': 'ApDqhTbpsAOGoYnhQQqbLjlosHPUBzVKlxm1wS2PBG8Q7'}, {
                'consumer_key': 'NzTjQ8zRqPwZ4cLSEEWUdVdjw',
                'consumer_secret': '5CVujT15x27zV9rWjRQnXKndzhv0X8Vs8f12gBce2yv5rvvYg6',
                'access_token': '757469703547879424-Kh4SPuIszS5H5KB6Y94rdVBEytD6dqZ',
                'access_token_secret': 'yo2FJonTg4MzDxfPEsNbxHePusYGUlvlfn1pM3Mnu389d'}, {
                'consumer_key': 'JKzUa3F0yiNLq460kORxe0KM2',
                'consumer_secret': '1efpSOFxA0VF3IIOor16jIguTcOOIdO9dd8znDQRvE6fRQY4FT',
                'access_token': '757469703547879424-PQCqCVPhItFqIljX7PxSH6BDbyqg5Mh',
                'access_token_secret': 's146GWiClnBv7s2VOBsEMzZjTnNTj82LX9H9kWT8k7LDY'}, {
                'consumer_key': '2pyIOUL88DZC0eJoB3g8rEi2c',
                'consumer_secret': 'YBVeCMvY52i7alwuyraEDfsPLZZS7DzsiH7I8OSvXdg2G0JrcR',
                'access_token': '990483629007491072-f07UmvW6ujV0RIkjjvkM9ztSl0hjHaU',
                'access_token_secret': 'UwPV29gRobeC4QKzJF4IAKVI0tIzrtgcgOs8CRA8lDB5Y'}, {
                'consumer_key': 'ggj5065prOE3U9rDBlBHFgstv',
                'consumer_secret': 'fhBeZNpLA13JTQtLGcyUZRfTpcdQ52LEqBktM38ZvO9JODh5no',
                'access_token': '886915377829105665-MiqALJmL4lBWA6LjDkjeakxXyRehnow',
                'access_token_secret': 'sYAViam2W9FkONZF35CoPpYqwl151BWO65HkdAINeIdbj'}, {
                'consumer_key': 'vIhYVId1iqF9OXe0nsm8PuQS7',
                'consumer_secret': 'EFc6HECXyH11AoZeDGnO0UBpzYtR2tubK25Iy6aGTi94UJANyM',
                'access_token': '757469703547879424-clpaRO4SevGYXNpNJadb2YCegtz3lkY',
                'access_token_secret': '9YrIkbIh5kR2Zu0jq1mAKBW5bisSHqz5AhJmCe1w1S2BM'}, {
                'consumer_key': 'UJOUOdb8vrA2dyHEfzwDeufVx',
                'consumer_secret': 'DJVDZF92CBLzWww1a45FSzP4rxvIJghN8srppvuI9SsCjK4F8R',
                'access_token': '757469703547879424-ERJSqNGrxa8SKIINx8xzsZPMCKbRzYn',
                'access_token_secret': 'I67D4DCuAiNfiPycHRpiKQBLkEtGiAUXCVIl3KwT3ckGV'},
            {
                'consumer_key': '7uf9G5wsuEbbPzNcCjdKhF5zU',
                'consumer_secret': 'NhBpgB9wI0tZmjCbpFCIArgdUVN9UxxEq63dl3KifxlS7BMr30',
                'access_token': '990483629007491072-GhTtxz6SqsNekF0OT95zgC0Cz2fKfzv',
                'access_token_secret': 'cLJzxmvKqTrKaF49NcVvUbSVSuTFvh4IiePuS1A2fJZ8E'}, {
                'consumer_key': 'RTxrXZb25k4TayGJYYixoONIb',
                'consumer_secret': 'gzL3qLlwLucxjjjS1muxw5mO7gcQiI7VI5EXaxNBRmf5gWxVqc',
                'access_token': '990483629007491072-Ih9zkACSaRwR8xbvCnw2r6D1qG6WiQa',
                'access_token_secret': '5ew3Ql9L1myi7m9M2FxnaHNiJz4rENk1Iz9kBIiAFqDWg'}, {
                'consumer_key': 'U8ujyUy7xu39Il4cJV6az2jLI',
                'consumer_secret': 'GsmDj5ceZnSur4ypNrnCEXbLR8PpI7HH7GabdUiwRnf0IIrt7c',
                'access_token': '990483629007491072-d9YeEMLvDZB7AvGHXbY0qvT6m4h1Ygd',
                'access_token_secret': 'pxlbXeq3RcsnlJx84JQ2dTSlKXUQ7tiEkP6c2vpTRYnUC'}, {
                'consumer_key': 'UYbVXHko0nfcvz5TGEdt9Udbg',
                'consumer_secret': 'HcLLApNSz2eAk9df32Nknxn5ZNiN6vBNtB1MVEzCGs1pa1sYut',
                'access_token': '886915377829105665-OiF9lZQ7OXj6DuHNGB0T1CErsmsH7iM',
                'access_token_secret': '1uAytoX0ETdOvFmqaKFrDXOQej8mWPrEoSENnWw45GgFz'}, {
                'consumer_key': '9jkA4TZaE85RW1ChGzs3NotrI',
                'consumer_secret': 'pDbJcjlcZ4hKT7n7jNT9YSRKPIVNf7aIegdzthGwtb1eg97nlc',
                'access_token': '988328066442117121-57t34wyyj2PmUP43KDe4Rpf6VZTqSvq',
                'access_token_secret': 'd3IvraqYRY12IWhU1xFuhzpLnz98B1pF4uy23QzOs6epl'}, {
                'consumer_key': 'pgfsBn29xx7WjIeQw2FgUzOhu',
                'consumer_secret': '7wAY43hjOqDS6zx0LNci56uwzdq4mcLiokOhF2jEKkTuSMoG5v',
                'access_token': '988328066442117121-ZwhKFqZJLuq3mSSGjm9MAXVZNHMn7je',
                'access_token_secret': 'qFiPcqj4v33kAniIbdgSHEjI8yezi2vo3bnDw85XSdcbb'}, {
                'consumer_key': 'kiLz9KGKoly1YqlFniL91Avcl',
                'consumer_secret': 'Ff7NxXzN9eUrHOWyWyjlscXwLSC3pUMwYBaVMmy37mOe6yNVUg',
                'access_token': '925304770193104897-UiszSjN3pO0faPZNyd1E6bwgEW68jJy',
                'access_token_secret': 'mqIOj8W9oYNSoqY5KrX1GmPGEXZkTq9IYSNsfsJVRS1k5'}, {
                'consumer_key': 'UlcKpGAMU5fW9uHi1xmEHlfF1',
                'consumer_secret': 'sHRmEho9FwnOjHYzaNFj010DR0YyoCdW7Ino1l13L9EfeWCr52',
                'access_token': '925304770193104897-XMkXssOdzi2Olfw9cBA4YhCYFq4Nl4P',
                'access_token_secret': 'NR1OQYnZeM756wbfgXClNG3VCXKSBu8rTfD8UMK7uaeHR'}, {
                'consumer_key': '3UeohllAkEkmHQxSAKBnKFbU6',
                'consumer_secret': 'HZZCJOJwEQeurIzHfblFeXkcT2BXCne4fKFyTx3FdZvTferoPf',
                'access_token': '925304770193104897-BAmZXEjwQIZNvfls0sakdGouFhMJC9l',
                'access_token_secret': 'MPLpKgXlgEdYkMH2MAkUM1Q6hWlLuUvQULOS6dvchbt66'}, {
                'consumer_key': 'WPOiyomOxUf0oB1n0mOGyyLFs',
                'consumer_secret': '8sPNhBpzPDgefscDKU6bAXLzTNTiCyx7fgQs9x8zgyecrKz8cj',
                'access_token': '886915377829105665-9Ed7FM0bMeSeReD9FePZYdOl2dURlXP',
                'access_token_secret': '4BGkCVdANs20i5riW5kDbztKzVsC8z3eDogjGCnsKVb7j'}, {
                'consumer_key': 'irCPmhuFx4dcLcK6YsrzOXXYa',
                'consumer_secret': 'mwdFyjK0CBuDSF4lrMJKnNlOQxafAnXblHEynJuFjlbyhDkv0v',
                'access_token': '1261882567764000769-hUlP9daIp8oXXSDjb2ye0o4dyJHbgD',
                'access_token_secret': 'j3wd47x1o4wXA6IDPFvY1rkoxK2XKUuI80tTgYTMO6x4g'}
            ]


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
