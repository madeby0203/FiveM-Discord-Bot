import requests
import socket
import asyncio
import discord
from discord.ext import commands

#rewrite_compatible

class status:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def status(self,ctx):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('66.150.121.131', 30150))
        if result == 0:
            response = requests.get("http://66.150.121.131:30150/players.json")
            json_data = response.json()
            if len(json_data) == 0:
                countNY1 = str(len(json_data))+" Players"
            else: 
                countNY1 = str(len(json_data)-1)+" Players"
            P1 = ":white_check_mark: NY Public 1"
        else:
            P1 = ":x: NY Public 1"
            countNY1 = "0 Players"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result2 = sock.connect_ex(('66.150.121.131', 30151))
        if result2 == 0:
            P2 = ":white_check_mark: NY Public 2"
            response2 = requests.get("http://66.150.121.131:30151/players.json")
            json_data2 = response2.json()
            if len(json_data2) == 0:
                countNY2 = str(len(json_data2))+" Players"
            else: 
                countNY2 = str(len(json_data2)-1)+" Players"
        else:
            P2 = ":x: NY Public 2"
            countNY2 = "0 Players"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result2 = sock.connect_ex(('66.150.121.131', 30141))
        if result2 == 0:
            P3 = ":white_check_mark: NY Public 3"
            response3 = requests.get("http://66.150.121.131:30141/players.json")
            json_data3 = response3.json()
            if len(json_data3) == 0:
                countNY3 = str(len(json_data3))+" Players"
            else: 
                countNY3 = str(len(json_data3)-1)+" Players"
        else:
            P3 = ":x: NY Public 3"
            countNY3 = "0 Players"
        embed=discord.Embed(description="Server status")
        embed.add_field(name = P1, value = countNY1, inline=True)
        embed.add_field(name = P2, value = countNY2, inline=True)
        embed.add_field(name = P3, value = countNY3, inline=True)
        embed.set_footer(text = f"BigCityRP - Requested by {ctx.author}")
        history = ctx.channel.history(limit = 10)
        print(history)
        async for old_message in ctx.channel.history(limit = 20):
            for old_embed in old_message.embeds:
                if old_embed.description == "Server status":
                    await old_message.delete()
        await ctx.send(embed = embed)
        await ctx.message.delete()

            
def setup(bot):
    bot.add_cog(status(bot))