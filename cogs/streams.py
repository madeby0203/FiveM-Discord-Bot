import discord
import asyncio
import json
import requests
from configparser import ConfigParser
from discord.utils import get
from discord.ext import commands
from discord import Emoji

#rewrite_compatible

class streams:
    def __init__(self, bot):
        self.bot = bot
        self.loaded = True
        self.parser = ConfigParser()
        self.parser.read("config.ini")
        self.perms = list(map(int, self.parser.get("settings","permissions").split(",")))
    def __unload(self):
        print("unloaded!")
        self.loaded = not self.loaded

    with open('streamers.json', encoding='utf-8') as f:
        try:
            streamers = json.load(f)
        except ValueError:
            streamers = {}
            streamers['users'] = []

    async def streamingstatus(self):
        while "streams" in self.bot.cogs:
            with open('streamers.json', encoding='utf-8') as f:
                try:
                    streamers = json.load(f)
                except ValueError:
                    streamers = {}
                    streamers['users'] = []
            for streamer in streamers["users"]:
                print("Checking status")
                if "online" in streamer["status"]:
                    username = streamer["twitch"]
                    streaming = discord.Streaming(name = f"{username} live on BigCityRP", url= f"https://www.twitch.tv/{username}", twitch_name= username)
                    await self.bot.change_presence(activity=streaming)
                if "streams" in self.bot.cogs:
                    await asyncio.sleep(20)

    async def on_ready(self):
        await self.bot.send_message(self.bot.get_channel("510315701664219136"),"STREAMER BOT ACTIVE")

    @commands.command(pass_context = True)
    async def fix(self, ctx):
        user_roles = [r.name.lower() for r in ctx.message.author.roles]
        level1 = ["owners","co-owners","directors","bot developer"]
        if not any(people in user_roles for people in level1):
            return await ctx.send("This is only meant for streamers and staff members!")
        self.bot.unload_extension("cogs.streams")
        self.bot.load_extension("cogs.streams")
        await ctx.message.author.send("I fixed the bot for you. Atleast I hope...")

    @commands.command(pass_context = True)
    async def remove(self, ctx,*,twitch = None):
        if not any(role.id in self.perms for role in ctx.author.roles):
            return await ctx.send("You are not allowed to do this!")
        await ctx.message.delete()
        with open('streamers.json', encoding='utf-8') as f:
            try:
                streamers = json.load(f)
            except ValueError:
                streamers = {}
                streamers['users'] = []
        if not twitch:
            return await ctx.send("You did not tell me which Twitch user to remove!")
        for streamer in streamers["users"]:
            if twitch == streamer["twitch"]:
                print("found username")
                streamers["users"].remove(streamer)
                await ctx.send(f"I deleted {twitch} from the list!")
                with open('streamers.json','w+') as f:
                    json.dump(streamers,f)

    @commands.command(pass_context = True)
    async def list(self, ctx):
        if not any(role.id in self.perms for role in ctx.author.roles):
            return await ctx.send("You are not allowed to do this!")
        await ctx.message.delete()
        with open('streamers.json', encoding='utf-8') as f:
            try:
                streamers = json.load(f)
            except ValueError:
                streamers = {}
                streamers['users'] = []
        twitch_list = []
        for users in streamers["users"]:
            twitch_list.append(users["twitch"]+" - "+users["discord"])
        complete_list = "- "+"\n- ".join(twitch_list)
        for chunk in [complete_list[i:i+1900] for i in range(0, len(complete_list), 1900)]:
            await ctx.send(f"```{chunk}```")
    @commands.command(pass_context = True)
    async def add(self, ctx, discord2:discord.Member,*, twitch):
        if not any(role.id in self.perms for role in ctx.author.roles):
            return await ctx.send("You are not allowed to do this!")
        await ctx.message.delete()
        with open('streamers.json', encoding='utf-8') as f:
            try:
                streamers = json.load(f)
            except ValueError:
                streamers = {}
                streamers['users'] = []
        stream_api_url = "https://api.twitch.tv/kraken/users/" + twitch + "?client_id=crpbtpk4268166xba7gthc84azfrjs"
        request = requests.get(stream_api_url)
        twitchuser = request.json()
        if "display_name" in twitchuser:
            for streamer in streamers['users']:
                if streamer['discord'] == discord2:
                    await ctx.send(f"{discord2} is already registered as "+streamer["twitch"])
                    return
                if streamer["twitch"] == twitch:
                    await ctx.send(discord2+" is already registered as "+streamer["twitch"])
                    return
            else:
                streamers['users'].append({
                'discord':str(discord2.id),
                'twitch':twitch,
                'status':"offline",
                })
            with open('streamers.json','w+') as f:
                json.dump(streamers,f)
            role = discord.utils.get(ctx.message.guild.roles, name='Certified Streamers')
            await discord2.add_roles(role)
            await ctx.send(f"I succesfully added **{twitch}** to the streamers list!")
        else:
            await ctx.send("The submitted username is not a valid Twitch username")

    async def online(self):
        await self.bot.wait_until_ready()
        while "streams" in self.bot.cogs:
            print(self.loaded)
            with open('streamers.json', encoding='utf-8') as f:
                try:
                    streamers = json.load(f)
                except ValueError:
                    streamers = {}
                    streamers['users'] = []
            print("Start")
            if "streams" in self.bot.cogs:
                print("Checking streamers...")
                for streamer in streamers['users']:
                    name = streamer["twitch"]
                    if "online" in streamer["status"]:
                        print("Checking online user")
                        api_call = "https://api.twitch.tv/kraken/streams/" + name + "?client_id=crpbtpk4268166xba7gthc84azfrjs"
                        request = requests.get(api_call)
                        api_result = request.json() 
                        if api_result["stream"] is None:
                            print("Streamer is no longer online")
                            channel2 = self.bot.get_channel(388072089611141133)
                            streamer['status'] = "offline"
                            with open('streamers.json','w+') as f:
                                json.dump(streamers,f)
                            async for message in channel2.history(limit = 10):
                                if (message.content.lower().__contains__(name)):
                                    await message.delete()
                    if "offline" in streamer["status"]:
                        print("Checking offline user")
                        api_call = "https://api.twitch.tv/kraken/streams/" + name + "?client_id=crpbtpk4268166xba7gthc84azfrjs"
                        request = requests.get(api_call)
                        api_result = request.json() 
                        if api_result["stream"] is not None:
                            if (str(api_result["stream"]["channel"]["status"]).lower().__contains__("bigcityrp")): 
                                channel = api_result["stream"]["channel"]
                                embed=discord.Embed(title=" ", description="Come watch their stream and join their "+str(channel["followers"])+" followers!", color=0x800080)
                                embed.set_author(name=f"{name} is currently streaming BigCityRP!", url=f"https://www.twitch.tv/{name}", icon_url="https://store-images.microsoft.com/image/apps.62877.13510798882435159.83304528-3c17-4158-ae2b-42ab78113763.c0314240-05b1-494a-a4ba-f5bde491422f?mode=scale&q=90&h=300&w=300")
                                embed.set_thumbnail(url=channel["logo"])
                                embed.add_field(name="Stream title:", value=channel["status"], inline=True)
                                msgchannel = self.bot.get_channel(388072089611141133)
                                await msgchannel.send(f"{name} is now online! @here", embed = embed)
                                print("Streamer is now online!")    
                                streamer['status'] = "online"
                            with open('streamers.json','w+') as f:
                                json.dump(streamers,f)                
                    if "streams" in self.bot.cogs:
                        await asyncio.sleep(2)
            else:
                return print("Failed to fix")

def setup(bot):
    bot.add_cog(streams(bot))
    bot.loop.create_task(streams(bot).online())
    bot.loop.create_task(streams(bot).streamingstatus())