import discord
import datetime
from discord.ext import commands

#rewrite_compatible

class links:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def wl(self, ctx):
        await ctx.send("<https://bigcityrp.com/forums/index.php?/application/form/3-white-list-application/>")
        await ctx.message.delete()

    @commands.command(pass_context = True)
    async def forums(self, ctx):
        embed=discord.Embed(color=0x0080ff)
        embed.add_field(name="Forums", value="https://bigcityrp.com/forums/index.php", inline=False)
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command(pass_context = True)
    async def webpanel(self, ctx):
        embed=discord.Embed(color=0x0080ff)
        embed.add_field(name="Webpanel", value="https://bigcityrp.com/panel/login.php", inline=False)
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command(pass_context = True)
    async def rules(self,ctx):
        embed=discord.Embed(color=0x0080ff)
        embed.add_field(name="Server Rules", value="https://bigcityrp.com/forums/index.php?/topic/4005-server-rules/", inline=False)
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command(pass_context = True)
    async def hex(self, ctx):
        await ctx.send("To Obtain your Hex Code please go to <http://vacbanned.com/> (You want the Steam3ID (64bit)) ")
        await ctx.message.delete()

    @commands.command(pass_context = True)
    async def cache(self, ctx):
        await ctx.send("**Step 1.** Close FiveM completely \n**Step 2.** Right click your FiveM Shortcut and click 'Open File Location'\n**Step 3.** Double click FiveM Application Data > Cache \n**Step 4.** Delete all files and folders EXCEPT the 'game' folder. \n**Step 5.** Reopen FiveM and connect to the server.")
        await ctx.message.delete()
        
    @commands.command(pass_context = True)
    async def christmas(self, ctx):
        delta = datetime.datetime(2018, 12, 25) - datetime.datetime(2018, 12, 25).now()
        await ctx.send(f"{delta.days} days and {delta.seconds/3600} hours until christmas")

    @commands.command(pass_context = True)
    async def donate(self, ctx):
        embed=discord.Embed(color=0x0080ff)
        embed.add_field(name="Donations", value="https://bigcityrp.com/forums/index.php?/donate/", inline=False)
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command(pass_context = True)
    async def support(self, ctx):
        embed=discord.Embed(color=0x0080ff)
        embed.add_field(name="Support", value="https://bigcityrp.com/forums/index.php?/support/", inline=False)
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command(pass_context = True)
    async def powergaming(self, ctx):
        embed=discord.Embed(color=0x0080ff)
        embed.add_field(name="Powergaming", value="Exploiting routes of roleplay or game mechanics to gain an unfair advantage over someone else.", inline=False)
        embed.set_footer(text="For more rules and definitions please visit our forums")
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command(pass_context = True)
    async def copbaiting(self, ctx):
        embed=discord.Embed(color=0x0080ff)
        embed.add_field(name="Copbaiting", value="Forcing RP with members of the police department through unrealistic actions no real human would do.", inline=False)
        embed.set_footer(text="For more rules and definitions please visit our forums")
        await ctx.send(embed=embed)
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(links(bot))