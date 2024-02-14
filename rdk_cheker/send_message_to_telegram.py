import requests
import os
from dotenv import load_dotenv


def send_telegram_message(text: str):
    load_dotenv()
    token = os.environ.get('old_token')
    channel_id = os.environ.get('channel_id')

    url = "https://api.telegram.org/bot"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
        "chat_id": channel_id,
        "text": text
    })

    if r.status_code != 200:
        raise Exception("post_text error")


if __name__ == '__main__':
    send_telegram_message('test message')
