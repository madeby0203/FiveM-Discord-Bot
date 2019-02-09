import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
from configparser import ConfigParser
import socket
import sys
import time
import configparser
import json
import requests
import datetime
from itertools import cycle

bot = commands.Bot(command_prefix = "*")
bot.remove_command('help')

with open('reports.json', encoding='utf-8') as f:
  try:
    report = json.load(f)
  except ValueError:
    report = {}
    report['users'] = []

@bot.event
async def on_ready():
    print("===================================")
    print("Logged in as: %s"%bot.user.name)
    print("ID: %s"%bot.user.id)
    print('Server count:', str(len(bot.guilds)))
    print('User Count:',len(set(bot.get_all_members())))
    print("Py Lib Version: %s"%discord.__version__)
    print('Servers connected to:')
    for guild in bot.guilds:
        print(str(guild.id) +" "+ guild.name)
    print("===================================")

@bot.command(pass_context = True)
async def info(ctx, member: discord.Member = None):
    embed=discord.Embed(title="BigCityRP Help", description="We strive to maintain the highest possible level of RP. If you have any concerns about issues, we encourage you to file a report on our forums.", color=0xff0000)
    embed.set_thumbnail(url="https://s3.amazonaws.com/appforest_uf/f1541509370161x472942849155515460/Webp.net-resizeimage%20%281%29.png")
    embed.add_field(name="Forums", value="https://bigcityrp.com/forums/", inline=False)
    embed.add_field(name="Support", value="http://bigcityrp.com/forums/index.php?/support/", inline=True)
    embed.add_field(name="Rules", value="https://bigcityrp.com/forums/index.php?/topic/4005-server-rules/", inline=False)
    embed.add_field(name="Donations", value="http://bigcityrp.com/forums/index.php?/donate/", inline=False)
    embed.add_field(name="Whitelist Jobs and Servers Applications", value="https://goo.gl/DpTEyH", inline=False)
    embed.add_field(name="Teamspeak IP", value="BigCityRP.com", inline=False)
    embed.set_footer(text = "See you later!")
    await ctx.send(embed=embed)
    await ctx.send("Requested by: "+ctx.message.author.mention)
    await ctx.message.delete()

extensions = ["links","status","welcome","logs","admin","filters","utilities","support","streams"]

@bot.command(pass_context = True)
async def load(ctx):
    user_roles = [r.name.lower() for r in ctx.message.author.roles]
    if "bot developer" not in user_roles:
        await ctx.send("You do not have permission to do that!")
        await ctx.message.delete()
    pass
    await ctx.message.delete()
    for extension in extensions:
        try:
            bot.load_extension("cogs."+extension)
        except Exception as error:
            await ctx.send(extension + "could not be loaded...\n" +error)
            print(extension + "could not be loaded...")
            print(error)

@bot.command(pass_context = True)
async def unload(ctx):
    user_roles = [r.name.lower() for r in ctx.message.author.roles]
    if "bot developer" not in user_roles:
        await ctx.send("You do not have permission to do that!")
        await ctx.message.delete()
    pass
    await ctx.message.delete()
    for extension in extensions:
        try:
            bot.unload_extension("cogs."+extension)
        except Exception as error:
            print(extension + "could not be unloaded...")
            print(error)

for extension in extensions:
    try:
        bot.load_extension("cogs."+extension)
    except Exception as error:
        print(extension + "could not be loaded...")

parser = ConfigParser()
parser.read("config.ini")
TOKEN = parser.get("settings","token")
bot.run(TOKEN)

