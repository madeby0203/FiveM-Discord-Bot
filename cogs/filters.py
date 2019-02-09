import discord
import json
from discord.ext import commands

#rewrite_compatible

class filters:
    def __init__(self, bot):
        self.bot = bot

    with open('blacklist.json', encoding='utf-8') as f:
        try:
            blacklist = json.load(f)
        except ValueError:
            blacklist = {}
            blacklist['words'] = []

    async def on_message(self, message):
        errormsg = "You did not use the correct format for a **Sales Listing**. Please do not chat in this channel. \nThe correct format is: \nSale title:\nSale price:\nDescription:"
        contents = message.content.split(" ")
        for word in contents:
            with open('blacklist.json', encoding='utf-8') as f:
                try:
                    blacklist = json.load(f)
                except ValueError:
                    blacklist = {}
                    blacklist['words'] = []
            if word.lower() in blacklist['words']:
                await message.delete()
                await message.channel.send(message.author.mention + " Please refrain from using inappropriate, derogatory language here. You will be muted if you continue.")
                reason = "Use of an inappropriate word"
                with open('reports.json', encoding='utf-8') as f:
                    try:
                        report = json.load(f)
                    except ValueError:
                        report = {}
                        report['users'] = []
                for current_user in report['users']:
                    if current_user['name'] == message.author.name:
                        current_user['reasons'].append(reason)
                        break
                else:
                    report['users'].append({
                    'name':message.author.name,
                    'reasons': [reason,]
                    })
                with open('reports.json','w+') as f:
                    json.dump(report,f)
        if message.channel == self.bot.get_channel(520271399739326465): #Only allow format in #sale-listings
            if (message.content.lower().__contains__("sale title:")):
                if (message.content.lower().__contains__("sale price:")): 
                    if (message.content.lower().__contains__("description:")): 
                        print("succesfull sale listing")

                    else: 
                        await message.author.send(errormsg)
                        await message.delete()
                else: 
                    await message.author.send(errormsg)
                    await message.delete()
            else: 
                await message.author.send(errormsg)
                await message.delete()
        if message.channel == self.bot.get_channel(427226349925564416): #only allow images to be sent
            if not message.attachments:
                if not message.author.bot:
                    user_roles = [r.name.lower() for r in message.author.roles]
                    level1 = ["bot developer", "owners"]
                    for role in level1:
                        if role not in user_roles:
                            print("Not a photo!")
                            await message.delete()
                            await message.author.send("Please do not chat in the #screenshots channel. You can use Discord reactions or chat in other channels like #general or #offtopic. Thank you!")
                        else:
                            print("Permission used in #screenshots")
            else:
                print("Thats a photo!")
                print(message.attachments)

def setup(bot):
    bot.add_cog(filters(bot))