import asyncio
import os
from dotenv import load_dotenv
import discord
from twitchio.ext import commands
import time  # Импортируем модуль для получения времени

load_dotenv()

TWITCH_API_TOKEN = os.getenv("TWITCH_API_TOKEN")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

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

intents = discord.Intents.default()
intents.message_content = True

class DiscordBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.twitch_bot = commands.Bot(token=TWITCH_API_TOKEN, prefix='!', initial_channels=initial_channels)
        self.streaming_channels = set()

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        await self.check_stream_status()

    async def check_stream_status(self):
        while True:
            try:
                # Получаем информацию о стримах
                streams = await self.twitch_bot.fetch_streams(user_logins=initial_channels)

                # Сохраняем данные о стримах (имя, категория, название)
                current_streaming_channels = {
                    (stream.user.name, stream.game_name, stream.title)
                    for stream in streams
                }
                
                # Находим новые стримы
                new_streaming_channels = current_streaming_channels - self.streaming_channels

                if new_streaming_channels:
                    self.streaming_channels.update(new_streaming_channels)

                    for channel_name, game_name, stream_title in new_streaming_channels:
                        await self.send_discord_notification(channel_name, game_name, stream_title)
            except Exception as e:
                print(f"Error during stream check: {e}")

            await asyncio.sleep(60)  # Проверять каждые 60 секунд

    async def send_discord_notification(self, channel_name, game_name, stream_title):
        channel = await self.fetch_channel(DISCORD_CHANNEL_ID)

        # ID роли, которую нужно упомянуть
        role_id = 1216401731517415514
        mention = f"<@&{role_id}>"  # Формат упоминания роли

        # Получаем информацию о пользователе через Twitch API
        user = await self.twitch_bot.fetch_users(names=[channel_name])

        if user:
            avatar_url = user[0].profile_image

            stream = await self.twitch_bot.fetch_streams(user_logins=[channel_name])

            if stream:
                thumbnail_url = stream[0].thumbnail_url.format(width=1280, height=720)
                timestamp = int(time.time())
                thumbnail_url_with_cache_bust = f"{thumbnail_url}?{timestamp}"

                embed = discord.Embed(
                    title=f"{stream_title}",
                    url=f"https://www.twitch.tv/{channel_name}",
                    color=0x6441a5
                )
                embed.set_author(
                    name=f"{channel_name} запустил стрим на Twitch",
                    url=f"https://twitch.tv/{channel_name}",
                    icon_url=avatar_url
                )
                embed.add_field(name="Игра:", value=f"{game_name}", inline=True)
                embed.set_image(url=thumbnail_url_with_cache_bust)

                # Отправляем одно сообщение с упоминанием роли и Embed
                await channel.send(content=mention, embed=embed)

discord_bot = DiscordBot(intents=intents)
discord_bot.run(DISCORD_TOKEN)
