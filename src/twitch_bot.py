from twitchio.ext import commands

class TwitchBot:
    def __init__(self, token, initial_channels):
        self.bot = commands.Bot(token=token, prefix='!', initial_channels=initial_channels)

    async def fetch_streams(self, user_logins):
        return await self.bot.fetch_streams(user_logins=user_logins)

    async def fetch_users(self, names):
        return await self.bot.fetch_users(names=names)
