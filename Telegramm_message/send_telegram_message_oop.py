import os
import requests
from dotenv import load_dotenv


class TelegramMessenger:
    def __init__(self):
        load_dotenv()
        self.token = os.environ.get('old_token')
        self.channel_id = os.environ.get('channel_id')
        self.base_url = "https://api.telegram.org/bot"

    def send_message(self, text):
        method = f"{self.base_url}{self.token}/sendMessage"
        response = requests.post(method, data={
            "chat_id": self.channel_id,
            "text": text
        })

        if response.status_code != 200:
            raise Exception("Error sending message")


# Example usage:
if __name__ == "__main__":
    telegram_messenger = TelegramMessenger()
    message_text = "Hello, this is a test message!"

    try:
        telegram_messenger.send_message(message_text)
        print("Message sent successfully")
    except Exception as e:
        print(f"Error: {e}")
