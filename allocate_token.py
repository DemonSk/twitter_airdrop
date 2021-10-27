import json

like = 0.00000012
retweet = 0.00000024


def allocate(tweet_id):
    with open("airdrop_tweets.json", "r") as read_file:
        data = json.load(read_file)
    with open("airdrop_users.json", "r") as file:
        users = json.load(file)
    winners = data[tweet_id]["winners"]
    for winner in winners:
        allocation = 0.00000001
        user_id = list(winner.keys())[0]
        liked = winner[user_id]["like"]
        retweeted = winner[user_id]["retweet"]
        if liked == 1:
            allocation = '{0:.8f}'.format(float(allocation) + like)
        if retweeted == 1:
            allocation = '{0:.8f}'.format(float(allocation) + retweet)
        user_earnings = users[user_id]["earned"]
        user_earnings = '{0:.8f}'.format(float(allocation) + float(user_earnings))
        users[user_id]["earned"] = user_earnings
    with open("airdrop_users.json", "w") as write_file:
        json.dump(users, write_file)


allocate("1445639687326953472")