import discord
from discord.ext import commands

#rewrite_compatible

class logs:
    def __init__(self, bot):
        self.bot = bot

    async def on_message_delete(self, message):
        if message.guild == self.bot.get_guild(325842626601549827):
            msg = message.content
            ath = message.author
            channel = message.channel
            attach = ''.join(str(e) for e in message.attachments)
            embed = discord.Embed(description = str(msg + attach))
            embed.set_author(name = "Message deleted")
            embed.add_field(name = "Written by:", value = str(ath), inline = False)
            embed.add_field(name = "Channel:", value = channel, inline = True)
            channel = self.bot.get_channel(511217531852292096)
            await channel.send(embed = embed)
            print(message.guild.audit_logs(limit=10, before=None, after=None, reverse=None, user=message.guild.me, action=None))

    async def on_message_edit(self, before, after):
        if before.content == "":
            return
        if before.guild == self.bot.get_guild(325842626601549827):
            print("message edited")
            print(before.content)
            print(after.content)
            embed = discord.Embed(description = str(before.author))
            embed.set_author(name = "Message edited by:")
            embed.add_field(name = "Original", value = before.content, inline = True)
            embed.add_field(name = "New", value = after.content, inline = False)
            embed.add_field(name = "Channel:", value = before.channel, inline = True)
            channel = self.bot.get_channel(523065024726564904)
            await channel.send(embed = embed)   
            print(before.guild.audit_logs(limit=10, before=None, after=None, reverse=None, user=None, action=None))

def setup(bot):
    bot.add_cog(logs(bot))