import requests
import json


def get_tweets_likes(tweet_id, header):
    like_url = "https://api.twitter.com/2/tweets/{}/liking_users".format(tweet_id)
    like_response = requests.request("GET", like_url, headers=header).json()
    retweet_url = "https://api.twitter.com/2/tweets/{}/retweeted_by".format(tweet_id)
    rewteet_response = requests.request("GET", retweet_url, headers=header).json()
    with open('likes.json', 'w') as outfile:
        json.dump(like_response["data"], outfile)
    with open('retweet.json', 'w') as outfile:
        json.dump(rewteet_response["data"], outfile)
    return "done"