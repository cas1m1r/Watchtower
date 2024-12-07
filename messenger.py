# Tripwire integration for Discord
# Get security alerts from your TripWires sent directly to your
# private discord server channels.
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv
import os

# Load Webook URL
if not os.path.isfile('.env'):
    print('[!!] Missing .env file')
    exit()
load_dotenv()
WEBHOOK = os.getenv('WEBHOOK')


class DiscordMsg:
    def __init__(self, msgType, msgData):
        self.mode = msgType
        self.data = msgData

    # Depending on mode may send different type of message

    def send_message(self):
        # Send a message
        webhook = DiscordWebhook(
            url=WEBHOOK,
            rate_limit_retry=True,
            content=self.data['content'])
        webhook.execute()
        return
