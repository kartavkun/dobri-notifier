import os
from dotenv import load_dotenv
import discord
from src.twitch_bot import TwitchBot
from src.discord_bot import DiscordBot

load_dotenv()

TWITCH_API_TOKEN = os.getenv("TWITCH_API_TOKEN")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

if not TWITCH_API_TOKEN:
    print("Error: TWITCH_API_TOKEN not found. Please set it in your .env file.")
    exit()

if not DISCORD_TOKEN or not DISCORD_CHANNEL_ID:
    print("Error: DISCORD_TOKEN or DISCORD_CHANNEL_ID not found. Please set them in your .env file.")
    exit()

initial_channels = [
    "IvanGO", "senyawei", "glebauster",
    "kartav__", "vudek_", "rainbowtaves", "ksuenoot", "danon_osu",
    "wavewyyy", "steisha_owo", "dahujka_owo", "kuukan_osu", "silversnakeuwu",
    "kkanoyaa", "lofkes_", "kury76", "quizzzzz_", "matrix_632",
    "pokemonyaaa", "j1mbeaam", "f0rz__", "mitor0_", "25mosey",
    "desuqe_", "godroponika", "honashhk", "skyfai_", "razorchik__",
]

twitch_bot = TwitchBot(TWITCH_API_TOKEN, initial_channels)
discord_bot = DiscordBot(twitch_bot, DISCORD_CHANNEL_ID, initial_channels, intents=discord.Intents.default())
discord_bot.run(DISCORD_TOKEN)
