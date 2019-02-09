import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
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
async def stream(ctx,*, link = ""):
    user_roles = [r.name.lower() for r in ctx.message.author.roles]
    name = link.replace("https://www.twitch.tv/", "")
    stream_api_url = "https://api.twitch.tv/kraken/streams/" + name.lower() + "?client_id=crpbtpk4268166xba7gthc84azfrjs"
    r = requests.get(stream_api_url)
    stream = r.json()
    if stream["stream"] is None:
        msg3 = await ctx.send("You are currently not live. Please be patient and try again later.")
        await bot.delete_message(ctx.message)
        time.sleep(10)
        await bot.delete_message(msg3)
    else:
        if "twitch certified" not in user_roles:
            msg2 = await bot.say("You are not a verified streamer!")
            await bot.delete_message(ctx.message)
            time.sleep(5)
            await bot.delete_message(msg2)
        pass
        if link == "":
            msg = await bot.send_message(ctx.message.channel, "You need to give a stream link!")
            await bot.delete_message(ctx.message)
            time.sleep(5)
            await bot.delete_message(msg)
        else:
            followers = stream["stream"]["channel"]["followers"]
            embed=discord.Embed(title=name + " is now Live :red_circle:", description="Hey everyone!"+name+" is currently live streaming from BigCityRP.com! Come watch their stream")
            embed.set_author(name="Click here to watch the stream!", url="https://www.twitch.tv/"+name)
            embed.set_thumbnail(url=stream["stream"]["channel"]["logo"])
            embed.add_field(name="Stream Title", value=stream["stream"]["channel"]["status"], inline=True)
            print(name)
            streammsg = await bot.send_message(bot.get_channel("388072089611141133"), embed=embed)
            mention = await bot.send_message(bot.get_channel("388072089611141133"), "@here")
            await bot.delete_message(ctx.message)
        if stream["stream"] is None:
            await bot.delete_message(streammsg)
    

@bot.command(pass_context = True)
async def info(ctx, member: discord.Member = None):
    author = ctx.message.author.mention
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

@bot.command(pass_context = True)
async def warn(ctx,user:discord.User,*reason:str):
  user_roles = [r.name.lower() for r in ctx.message.author.roles]

  if "admins" not in user_roles:
    if "bot developer" not in user_roles:
        if "directors" not in user_roles:
            if "owner" not in user_roles:
                if "co-owners" not in user_roles:
                    if "moderators" not in user_roles:
                        return await ctx.send("You do not have the correct role!")
  pass
  if not reason:
    await ctx.send("Please provide a reason")
    return
  reason = ' '.join(reason)
  for current_user in report['users']:
    if current_user['name'] == user.name:
      current_user['reasons'].append(reason)
      break
  else:
    report['users'].append({
      'name':user.name,
      'reasons': [reason,]
    })
  with open('reports.json','w+') as f:
    json.dump(report,f)
  await ctx.message.delete()
  await ctx.send("**"+ user.name + " was warned for: **" + reason )
  await ctx.send(user, "Hey **" + user.name+ "**, you were warned for: **"+ reason+ "**")

@bot.command(pass_context = True)
async def embed(ctx, name, role, rpnames, rpjobs, email, location, hexcode):
    embed=discord.Embed(title= name, url="https://www.bigcityrp.com", description="BigCityRP Management Team", color=0x0000ff)
    embed.set_thumbnail(url="https://s3.amazonaws.com/appforest_uf/f1541509370161x472942849155515460/Webp.net-resizeimage%20%281%29.png")
    embed.add_field(name="Role", value= role, inline=True)
    embed.add_field(name="Discord", value= ctx.message.author, inline=False)
    embed.add_field(name="RP Name(s)", value= rpnames, inline=False)
    embed.add_field(name="RP Job title", value=rpjobs, inline=False)
    embed.add_field(name="E-mail", value= email, inline=False)
    embed.add_field(name="Location", value= location, inline=False)
    embed.add_field(name="Steam Hex", value= hexcode, inline=False)
    await bot.say(embed=embed) 

@bot.command(pass_context = True)
async def pwarn(ctx,user:discord.User,*reason:str):
  user_roles = [r.name.lower() for r in ctx.message.author.roles]

  if "admins" not in user_roles:
    if "bot developer" not in user_roles:
        if "directors" not in user_roles:
            if "owner" not in user_roles:
                if "co-owners" not in user_roles:
                    if "moderators" not in user_roles:
                        return await bot.say("You do not have the correct role!")
  pass
  if not reason:
    await bot.say("Please provide a reason")
    return
  reason = ' '.join(reason)
  for current_user in report['users']:
    if current_user['name'] == user.name:
      current_user['reasons'].append(reason)
      break
  else:
    report['users'].append({
      'name':user.name,
      'reasons': [reason,]
    })
  with open('reports.json','w+') as f:
    json.dump(report,f)
  await bot.delete_message(ctx.message)
  await bot.send_message(user, "Hey **" + user.name+ "**, you were warned for: **"+ reason+ "**")

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

bot.loop.create_task(change_status())
bot.run(TOKEN)