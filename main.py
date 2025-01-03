import os
from dotenv import load_dotenv
from discord import Intents, Client, Message

# Loading discord token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

