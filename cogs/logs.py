import discord
from discord.ext import commands

#rewrite_compatible

class logs:
    def __init__(self, bot):
        self.bot = bot

    async def on_command(self, ctx):
        if ctx.message.guild == self.bot.get_guild(325842626601549827):
            embed=discord.Embed(title=" ", color=0xffff00)
            embed.set_author(name="Executed command")
            embed.add_field(name="Command:", value=ctx.command, inline=True)
            embed.add_field(name="Arguments:", value=ctx.kwargs, inline=False)
            embed.add_field(name="User:", value=ctx.author, inline=True)
            embed.add_field(name="Channel:", value=ctx.channel, inline=True)
            embed.add_field(name="Cog:", value=ctx.cog, inline=True)
            channel = self.bot.get_channel(552174763255136256)
            await channel.send(embed = embed)

    #async def on_command_error(self, ctx, error):
    #    if ctx.message.guild == self.bot.get_guild(325842626601549827):
    #        embed=discord.Embed(title=" ", color=0xff0000)
    #        embed.set_author(name="Command Error")
    #        embed.add_field(name="Command:", value=ctx.command, inline=True)
    #        embed.add_field(name="Arguments:", value=ctx.kwargs, inline=False)
    #        embed.add_field(name="User:", value=ctx.author, inline=True)
    #        embed.add_field(name="Channel:", value=ctx.channel, inline=True)
    #        embed.add_field(name="Error:", value=error, inline=True)
    #        channel = self.bot.get_channel(552174763255136256)
    #        await channel.send("<@153259480715362304>", embed = embed)

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
            print(message.guild.audit_logs(limit=10, before=None, after=None, reverse=None, user=None, action=None))

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