import telebot
import requests
import json
from config import telebot_api, twitter_bearer

headers = {"Authorization": "Bearer {}".format(twitter_bearer)}


bot=telebot.TeleBot(telebot_api)
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,"Hi there, to register for airdrop, please use command /register")


@bot.message_handler(commands=['register'])
def register_command(message):
    # with open("airdrop_users.json", "r") as read_file:
    #     data = json.load(read_file)
    # if f"{message.from_user.id}" in data.keys():
    #     bot.send_message(message.chat.id,"Sorry, you can only register once")
    # else:
    bot.send_message(message.chat.id,"Send me your user name of twitter with @.\nExample: @elonmusk")
    bot.register_next_step_handler(message, check_user)


def check_user(message):
    bot.send_message(message.chat.id, f"Searching for you ({message.text}) in twitter, please wait...")
    twitter_username = message.text[1:]
    find_response = requests.request("GET", f"https://api.twitter.com/2/users/by/username/{twitter_username}", headers=headers)
    try:
        find_json = find_response.json()
        if "errors" in find_json:
            bot.send_message(message.chat.id,"I can't find you. Please, check your input and try again.\nExample: @coingecko")
            bot.register_next_step_handler(message, check_user)
        else:
            name = find_json["data"]["name"]
            global user_twitter_id
            user_twitter_id = find_json["data"]["id"]
            bot.send_message(message.chat.id, f"{name}, I found you 😎. Provide your wallet address, where you will receive airdrop tokens.")
            bot.register_next_step_handler(message, check_wallet)
    except:
        bot.send_message(message.chat.id,"Your username should be without space. Please, provide correct username.\nExample: @coingecko")
        bot.register_next_step_handler(message, check_user)


def check_wallet(message):
    if message.text[0:2] == "0x" and len(message.text) == 42:
        bot.send_message(message.chat.id, "Great, registration complete. I will notify you, when you will receive tokens.\nHave a good day!")
        with open("airdrop_users.json", "r") as read_file:
            data = json.load(read_file)
        data[f"{message.from_user.id}"] = {"twitter_id": user_twitter_id, "wallet_address": message.text}
        with open("airdrop_users.json", "w") as write_file:
            json.dump(data, write_file)
    else:
        bot.send_message(message.chat.id, "Check your wallet address. It should start with 0x")
        bot.register_next_step_handler(message, check_wallet)
        

bot.infinity_polling()