import requests
import socket
import discord
from discord.ext import commands
from discord.utils import get

#rewrite_compatible

class utilities:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def ship(self,ctx):
        await ctx.send(":cruise_ship:")
        await ctx.message.delete(ctx.message)

    @commands.command(pass_context = True)
    async def help(self,ctx, subject = ""):
        await ctx.message.delete()
        user_roles = [r.name.lower() for r in ctx.message.author.roles]
        if subject == "":
            embed=discord.Embed(title=" ", description="Please provide which subject you need help with:")
            embed.set_author(name="Help")
            embed.add_field(name="?help links", value="List of all useful links", inline=False)
            embed.add_field(name="?help utilities", value="List with general usefull commands", inline=False)
            embed.add_field(name="?help streams", value="List of all commands relevant to verified streamers", inline=False)
            embed.add_field(name="?help admin", value="List of commands relevant to staff members", inline=True)
            await ctx.send(embed=embed)
            return
        if subject == "links":
            embed=discord.Embed(title=" ")
            embed.set_author(name="Links help", icon_url="https://bigcityrp.com/forums/uploads/monthly_2018_12/logo.png.c3e1b5a1aa66740a744dd70417cce913.png")
            embed.add_field(name="?forums", value="Provides link to BigCityRP Forums", inline=False)
            embed.add_field(name="?webpanel", value="Provides link to BigCityRP webpanel", inline=False)
            embed.add_field(name="?rules", value="Provides link to our server rules", inline=False)
            embed.add_field(name="?donate", value="Provides link to where you can donate to our community", inline=False)
            embed.add_field(name="?support", value="Provides link to BigCityRP Support", inline=False)
            await ctx.message.author.send(embed=embed)
        if subject == "utilities":
            embed=discord.Embed(title=" ")
            embed.set_author(name="Utilities help", icon_url="https://bigcityrp.com/forums/uploads/monthly_2018_12/logo.png.c3e1b5a1aa66740a744dd70417cce913.png")
            embed.add_field(name="?cache", value="Provides instructions on how to clear your game cache", inline=False)
            embed.add_field(name="?status", value="Shows the current server status and player count", inline=False)
            embed.add_field(name="?meta", value="Provides the definition of metagaming", inline=False)
            await ctx.message.author.send(embed=embed)
        if subject == "streams":
            level1 = ["owners","co-owners","directors","admins","moderators","bot developer","certified streamers"]
            if not any(people in user_roles for people in level1):
                return await self.bot.say("This is only meant for streamers and staff members!")
            embed=discord.Embed(title=" ", description="Keep in mind; some of these commands are limited to certain members")
            embed.set_author(name="Streams help", icon_url="https://bigcityrp.com/forums/uploads/monthly_2018_12/logo.png.c3e1b5a1aa66740a744dd70417cce913.png")
            embed.add_field(name="?fix", value="In case announcements are not working, you can attempt to use this command" , inline=False)
            embed.add_field(name="?announce [Twitch username]", value="Manually announce your stream in case the bot isnt operational", inline=False)
            embed.add_field(name="?add [Discord member] [Twitch username]", value="Add a streamer to the verified streamers list", inline=False)
            embed.add_field(name="?remove [Twitch username]", value="Remove a streamer from the verified streamers list", inline=False)
            embed.add_field(name="?list", value="Get a list of all the verified streamers", inline=True)
            await ctx.message.author.send(embed=embed)
        if subject == "admin":
            level1 = ["owners","co-owners","directors","admins","moderators","bot developer"]
            if not any(people in user_roles for people in level1):
                return await self.bot.say("This is only meant for staff members!")
            embed=discord.Embed(title=" ")
            embed.set_author(name="Admin help", icon_url="https://bigcityrp.com/forums/uploads/monthly_2018_12/logo.png.c3e1b5a1aa66740a744dd70417cce913.png")
            embed.add_field(name="?mute [Discord user]", value="Mute a certain Discord user", inline=False)
            embed.add_field(name="?warn [Discord user]", value="Warn a user in-chat", inline=False)
            embed.add_field(name="?pwarn [Discord user]", value="Warn a user via private message", inline=False)
            embed.add_field(name="?warnings [Discord user]", value="Show a users warning history", inline=False)
            embed.add_field(name="?ban [Discord user]", value="Ban a user", inline=False)
            embed.add_field(name="?say [message]", value="Have the bot say your message", inline=False)
            embed.add_field(name="?clear [number]", value="Have the bot clear an amount of messages in the channel", inline=False)
            embed.add_field(name="?id [server number] [id]", value="Get player info by player ID on the server", inline=True)
            await ctx.message.author.send(embed=embed)
        

    @commands.command(pass_context = True)
    async def civ(self, ctx, member: discord.Member = None):
        user_roles = [r.name.lower() for r in ctx.message.author.roles]
        role = discord.utils.get(member.guild.roles, name='Civilian')

        if "bot developer" not in user_roles:
            return await ctx.send("You do not have permission to do that")
        pass

        if member == "":
            await ctx.say(":x: No user Mentioned")
        await ctx.message.author.add_roles(role)
        await ctx.message.delete()

    @commands.command(pass_context = True)
    async def meta(self, ctx):
        author = ctx.message.author
        embed = discord.Embed(desciption = "Meta Lesson")
        embed.set_author(name = "RP Lesson #234 with")
        embed.add_field(name = author, value = "Metagaming is a term used in role-playing games, which describes a player's use of real-life knowledge concerning the state of the game to determine their character's actions, when said character has no relevant knowledge or awareness under the circumstances. ")
        embed.set_footer(text = "Enjoy!")
        await ctx.send(embed = embed)

    @commands.command(pass_context = True)
    async def clear(self, ctx, number : int):
        await ctx.message.delete()
        user_roles = [r.name.lower() for r in ctx.message.author.roles]
        level1 = ["owners","co-owners","directors","admins","moderators","bot developer"]
        if not any(people in user_roles for people in level1):
            return await ctx.send("You are not allowed to do this!")
        if not number:
            return await ctx.send("Please tell me how many messages I have to clear for you")
        await ctx.channel.purge(limit=number)
        await ctx.send(f"I deleted {number} messages for you!")

    @commands.command(pass_context = True)
    async def say(self, ctx,*, message = ""):
        user_roles = [r.name.lower() for r in ctx.message.author.roles]
        if "bot developer" or "directors" in user_roles:
            await ctx.send(message)
            await ctx.message.delete()

    @commands.command(pass_context = True)
    async def message(self, ctx, member: discord.Member = None, *, message):
        user_roles = [r.name.lower() for r in ctx.message.author.roles]
        if "bot developer" in user_roles:
            await ctx.message.author.send(message)
            await ctx.message.delete()

    @commands.command(pass_context = True)
    async def mechadd(self, ctx, member:discord.User=None):
        await ctx.message.delete()
        user_roles = [r.name.lower() for r in ctx.message.author.roles]
        level1 = ["owners","co-owners","directors","admins","moderators","bot developer","shop owner"]
        if not any(people in user_roles for people in level1):
            return await ctx.say("You are not allowed to do this!")
        role = discord.utils.get(member.guild.roles, name='Mechanic')
        await member.add_roles(role)
    
    @commands.command(pass_context = True)
    async def mechrem(self, ctx, member:discord.User=None):
        await ctx.message.delete()
        user_roles = [r.name.lower() for r in ctx.message.author.roles]
        level1 = ["owners","co-owners","directors","admins","moderators","bot developer","shop owner"]
        if not any(people in user_roles for people in level1):
            return await ctx.send("You are not allowed to do this!")
        role = discord.utils.get(member.guild.roles, name='Mechanic')
        await member.remove_roles(role)

    @commands.command(pass_context = True)
    async def towadd(self, ctx, member:discord.User=None):
        await ctx.message.delete()
        user_roles = [r.name.lower() for r in ctx.message.author.roles]
        level1 = ["owners","co-owners","directors","admins","moderators","bot developer","shop owner"]
        if not any(people in user_roles for people in level1):
            return await ctx.send("You are not allowed to do this!")
        role = discord.utils.get(member.guild.roles, name='Tow Driver')
        await member.add_roles(role)

    @commands.command(pass_context = True)
    async def towrem(self, ctx, member:discord.User=None):
        await ctx.message.delete()
        user_roles = [r.name.lower() for r in ctx.message.author.roles]
        level1 = ["owners","co-owners","directors","admins","moderators","bot developer","shop owner"]
        if not any(people in user_roles for people in level1):
            return await ctx.send("You are not allowed to do this!")
        role = discord.utils.get(member.guild.roles, name='Tow Driver')
        await member.remove_roles(role)

    @commands.command(pass_context = True)
    async def id(self, ctx, server = None, id2 = None):
        await ctx.message.delete()
        user_roles = [r.name.lower() for r in ctx.message.author.roles]
        level1 = ["owners","co-owners","directors","admins","moderators","bot developer"]
        if not any(people in user_roles for people in level1):
            return await ctx.send("You are not allowed to do this!")
        if not server:
            return await ctx.send("Please tell me wich server the player is on")
        if not id2:
            return await ctx.send("Please give me a player ID")
        if server == "1":
            response = requests.get("http://66.150.121.131:30150/players.json")
            svr = "NY Public 1"
        if server == "2":
            response = requests.get("http://66.150.121.131:30151/players.json")
            svr = "NY Public 2"
        if server == "3":
            response = requests.get("http://66.150.121.131:30142/players.json")
            svr = "NY Public 3"
        json_data = response.json()
        for player in json_data:
            if int(id2) == player["id"]:
                embed=discord.Embed(title=" ", color=0xff8000)
                embed.set_author(name=f"Player information of ID {id2}")
                embed.add_field(name='Name', value=player["name"], inline=True)
                embed.add_field(name='Steam ID', value=player["identifiers"][0], inline=True)
                embed.add_field(name='Server', value=svr, inline=True)
                await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(utilities(bot))