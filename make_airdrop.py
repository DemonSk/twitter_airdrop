import requests
import json
from config import twitter_bearer
from twitter_info import get_tweets_likes


headers = {"Authorization": "Bearer {}".format(twitter_bearer)}
user_id = 1086713836185497601
url = f"https://api.twitter.com/2/users/{user_id}/tweets"
response = requests.request("GET", url, headers=headers).json()
response_data = response["data"]
with open("airdrop_tweets.json", "r") as read_file:
    airdrop_tweet = json.load(read_file)
id = 0
# for id in range(1, len(response_data)):
#     tweet_info = response_data[id]
#     if tweet_info['id'] in airdrop_tweet:
#         break
#     elif tweet_info['text'][0:1] == "@":
#         pass
#     else:
#         airdrop_tweet[f"{tweet_info['id']}"]
tweet_info = response_data[2]
if tweet_info['text'][0:1] != "@" and tweet_info['id'] not in airdrop_tweet:
    with open("airdrop_users.json", "r") as user_file:
        airdrop_users = json.load(user_file)
    get_tweets_likes(tweet_info['id'], headers)
    with open("likes.json", "r") as likes_file:
        users_likes = json.load(likes_file)
    with open("retweet.json", "r") as retweets_file:
        users_retweets = json.load(retweets_file)
    registered_data = list(airdrop_users.values())
    registered_users = [
        registered_data[i]["twitter_id"] for i in range(len(airdrop_users))
    ]
    winners = []
    retweets_data = [users_retweets[i]["id"] for i in range(len(users_retweets))]
    for like in range(len(users_likes)):
        user = users_likes[like]["id"]
        if user in registered_users:
            if user in retweets_data:
                winners.append({user: {"like": 1, "retweet": 1}})
            else:
                winners.append({user: {"like": 1, "retweet": 0}})
    airdrop_tweet[f"{tweet_info['id']}"] = {"winners": winners}
    with open("airdrop_tweets.json", "w") as write_file:
        json.dump(airdrop_tweet, write_file)