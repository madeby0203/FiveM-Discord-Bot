import discord
from discord.utils import get
from discord.ext import commands
from discord import Emoji

#rewrite_compatible

class welcome:
    def __init__(self, bot):
        self.bot = bot

    #async def on_ready(self):
    #    YES = get(self.bot.get_all_emojis(), name='YES')
    #    embed=discord.Embed(title="Thank you for joining in!")
    #    embed.add_field(name="I have read the above rules and information", value="Please press YES to confirm and to continue into our Discord!", inline=False)
    #    await self.bot.purge_from(channel = self.bot.get_channel("522815463680638977"), limit = 1)
    #    msg = await self.bot.send_message(self.bot.get_channel("522815463680638977"), embed = embed)
    #    await self.bot.add_reaction(msg, YES)

    #async def on_reaction_add(self, reaction, user):
    #    if reaction.message.channel == self.bot.get_channel("522815463680638977"):
    #        if isinstance(reaction.emoji, Emoji):
    #            if reaction.emoji.name == 'YES':
    #                civilian = discord.utils.get(user.server.roles, name='Civilian')
    #                newmember = discord.utils.get(reaction.message.server.roles, name='New Members')
    #                await self.bot.add_roles(user, civilian)
    #               await self.bot.remove_roles(user, newmember)
    #                await self.bot.add_roles(user, civilian)
    #                await self.bot.remove_roles(user, newmember)
    #                print("Correct emoji")

    
    async def on_member_join(self,member):
        if member.guild is self.bot.get_guild("325842626601549827"):
            embed=discord.Embed(title="")
            embed.set_author(name="User joined the server", icon_url="https://s3.amazonaws.com/appforest_uf/f1541509370161x472942849155515460/Webp.net-resizeimage%20%281%29.png")
            embed.set_thumbnail(url= member.avatar_url)
            embed.add_field(name="Username", value=member, inline=True)
            embed.add_field(name="Date account creation", value=member.created_at, inline=True)
            channel = self.bot.get_channel(443255438364901376)
            await channel.send(embed=embed)

    @commands.command(pass_context = True)
    async def welcome(self,ctx):
        embed1=discord.Embed(title="Welcome to the BigCityRP community!", description="Before you join in on all the fun, please read this to find out about all the rules and important information you might need!")
        embed2=discord.Embed(title="Discord rules", description="Anyone caught breaking these will be muted, kicked or banned.  \n - Discord is OUT OF CHARACTER \n- Usernames that are not taggable via a Smartphone or are insulting/racist/inappropriate are not allowed \n- Spamming channels will result in a mute or kick \n- Do not distribute pirated software, game hacks and such \n- Be respectful \n- Inappropriate 'playing' status' will result in a kick \n- Advertising of any form, including dm will result in a ban \n- Do your best to keep your messages in the correct channel")
        embed3=discord.Embed(title="Server Rules", description="Before you join our servers, we would like you to take a look at out rules! Please take your time with getting to know them! \nYou can find our rules here: https://goo.gl/UnEgPk")
        embed4=discord.Embed(title="Community Staff", description="- All staff members volunteer their time here and are not paid, real life always comes first. If you do not get a response from them right away, that is probably why. If you require assistance but none are available, please make a Discord support ticket. \n- We have 6 staff roles as follows \n**- Moderators** : The “bread and butter” of our community. They have the essentials to maintain a safe and happy server. \n **- Administrators** : The workhorses of the Management Team. \n**- Directors** : Work hand in hand with the ​full authority of the Owner​, serving at the highest level of the Management Team. \n** - Owner** : The top authority in the community. \n**- Game Developers** : Work directly with the Owner and Directors to bring about new scripts and other features to the community servers.\n**- Web Developers** : Work directly with the Owner and Directors to develop other community-related features, such as the Web Panel, Forums ")
        await ctx.send(embed = embed1)
        await ctx.send(embed = embed2)
        await ctx.send(embed = embed3)
        await ctx.send(embed = embed4)

def setup(bot):
    bot.add_cog(welcome(bot))