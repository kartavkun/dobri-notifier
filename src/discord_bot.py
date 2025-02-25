import discord
import asyncio
import time

class DiscordBot(discord.Client):
    def __init__(self, twitch_bot, discord_channel_id, initial_channels, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.twitch_bot = twitch_bot
        self.discord_channel_id = discord_channel_id
        self.initial_channels = initial_channels  # Сохраняем initial_channels как атрибут
        self.streaming_channels = set()

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        await self.check_stream_status()

    async def check_stream_status(self):
        while True:
            try:
                # Используем self.initial_channels вместо initial_channels
                streams = await self.twitch_bot.fetch_streams(self.initial_channels)
                current_streaming_channels = {
                    (stream.user.name, stream.game_name, stream.title)
                    for stream in streams
                }

                new_streaming_channels = current_streaming_channels - self.streaming_channels

                if new_streaming_channels:
                    self.streaming_channels.update(new_streaming_channels)

                    for channel_name, game_name, stream_title in new_streaming_channels:
                        await self.send_discord_notification(channel_name, game_name, stream_title)
            except Exception as e:
                print(f"Error during stream check: {e}")

            await asyncio.sleep(60)

    async def send_discord_notification(self, channel_name, game_name, stream_title):
        channel = await self.fetch_channel(self.discord_channel_id)
        role_id = 1216401731517415514
        mention = f"<@&{role_id}>"

        user = await self.twitch_bot.fetch_users([channel_name])

        if user:
            avatar_url = user[0].profile_image
            stream = await self.twitch_bot.fetch_streams([channel_name])

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

                await channel.send(content=mention, embed=embed)
