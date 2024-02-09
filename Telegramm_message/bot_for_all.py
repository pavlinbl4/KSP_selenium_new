"""
хочу написать бота, в которого можно добавлять разные модули
"""

import telebot
import os
from dotenv import load_dotenv


def telegram_bot():
    load_dotenv()
    token = os.environ.get('token')
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Напиши что мне делать")

    @bot.message_handler(content_types=["text"])
    def send_text(message):

        if message.text.lower() == "a":
            bot.send_message(message.chat.id, "I am waiting for your order")
            print("Statr any function")
            bot.send_message(message.chat.id, "I am your servant")


        elif message.text.lower() == "boss":
            bot.send_message(message.chat.id, "Boss I'am working")


        else:
            bot.send_message(message.chat.id, "wrong command")

    bot.polling(none_stop=True)


if __name__ == '__main__':
    telegram_bot()
