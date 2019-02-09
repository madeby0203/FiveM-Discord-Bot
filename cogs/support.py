import discord
import json
from discord.utils import get
from discord.ext import commands
from discord import Emoji

#rewrite_compatible

class support:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def addclient(self, ctx,*, user=""):
        await ctx.message.delete()
        member = discord.utils.get(ctx.message.guild.members, name=user)
        if member is None:
            member = discord.utils.get(ctx.message.guild.members, display_name=user)
        embed=discord.Embed(title=" ", color=0xffff00)
        embed.add_field(name="Another user was added to the ticket!", value=member.mention, inline=False)
        await ctx.message.channel.send(embed=embed)
        await ctx.message.channel.set_permissions(member, read_messages=True)

    @commands.command(pass_context = True)
    async def new(self, ctx, *,topic = ""):
        await ctx.message.delete()
        if topic == "":
            subject = "No subject given"
        else:
            subject = topic
        with open('tickets.json', encoding='utf-8') as f:
            try:
                tickets = json.load(f)
            except ValueError:
                tickets = {}
                tickets['client'] = []
        everyone_perms = discord.PermissionOverwrite(read_messages=False)
        my_perms = discord.PermissionOverwrite(read_messages=True)
        support = self.bot.get_channel(id=542312691885277184)
        overwrites = {
            ctx.message.author: discord.PermissionOverwrite(read_messages=True),
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.get_role(502907158547922944): discord.PermissionOverwrite(read_messages=True),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        Tid = tickets["client"][-1]["id"]+1
        tickets["client"].append({
            "name": ctx.message.author.id,
            "topic":subject,
            "id": Tid,
        })
        with open('tickets.json','w+') as f:
            json.dump(tickets,f)
        channel = await ctx.guild.create_text_channel(f'Ticket-{Tid}', overwrites=overwrites, category=support)
        embed=discord.Embed(title=" ", description="Thank you contacting the Support Team of the BigCityRP Community. A Support Member will be with you as soon as they are available.  \n \nPlease provide a detailed description of the support issue in the chat below. If you would like to have anyone else added to this ticket, please list them in the chat so they may be added by our Support Team.", color=0xff8000)
        embed.set_author(name=f"Hi {str(ctx.message.author)}")
        embed.add_field(name="Subject", value=subject, inline=True)
        embed.add_field(name="Ticket ID", value=Tid, inline=True)
        await channel.send(embed=embed)
        log=discord.Embed(title=" ", description=f"By {ctx.message.author} with ID {Tid}", color=0x26ff00)
        log.set_author(name="Ticket opened")
        log.add_field(name="Subject", value=f"{subject} - <#{channel.id}>", inline=False)
        channel = self.bot.get_channel(542375515424686082)
        await channel.send(embed=log)

    @commands.command(pass_context = True)
    async def close(self, ctx,*, reason = ""):
        if ctx.message.channel.category != 542312691885277184:
            await ctx.message.delete()
            ID = ctx.message.channel.name.split("-",1)[1]
            file = open(f"ticket-{ID}.txt", "w")
            async for message in ctx.message.channel.history(limit = 500, reverse = True):
                file.write(f"{str(message.author)} - {message.content}\n")
            file.close()
            sendfile = discord.File(fp = f"ticket-{ID}.txt", filename= f"ticket-{ID}-transcript.txt")
            log=discord.Embed(title=" ", description=f"By {ctx.message.author}", color=0xff0000)
            log.set_author(name="Ticket closed")
            log.add_field(name="ID", value=ctx.message.channel, inline=False)
            with open('tickets.json', encoding='utf-8') as f:
                tickets = json.load(f)
            for ticket in tickets["client"]:
                if str(ticket["id"]) ==ID:
                    client = ticket["name"]
                    member = discord.utils.get(ctx.message.guild.members, id=client)
            channel = self.bot.get_channel(542375515424686082)
            await member.send("Your support ticket with ID {ID} was closed. I have attached the transcript in case you need it for future reference.", file=sendfile)
            await channel.send(embed=log, file = sendfile)
            await ctx.message.channel.delete()

    @commands.command(pass_context = True)
    async def tickets(self, ctx, member:discord.Member = ""):
        if member is None:
            return await ctx.send("Please mention a discord user")
        with open('tickets.json', encoding='utf-8') as f:
            try:
                tickets = json.load(f)
            except ValueError:
                tickets = {}
                tickets['client'] = []
        ticketlist = []
        for user in tickets["client"]:
            if user["name"] == member.id:
                ticketlist.append(str(user["id"]) +" - "+user["topic"])
        if not ticketlist:
            await ctx.send("This user has never opened a support ticket")
        else:
            await ctx.send(f"```Markdown\n <list of tickets of {member}:> \n"+" \n ".join(ticketlist)+ "```")

    @commands.command(pass_context = True)
    async def transcript(self, ctx, id = ""):
        if id is None:
            return await ctx.send("Please give me a Ticket ID")
        try:
            sendfile = discord.File(fp = f"ticket-{id}.txt", filename= f"ticket-{id} chat log.txt")
            await ctx.send(f"This is the chat of ticket {id}", file=sendfile)
        except:
            await ctx.send(f"I was not able to find a transcript with ID {id}. It is possible that this ticket has not been closed yet")

    @commands.command(pass_context = True)
    async def rename(self, ctx, name = ""):
        await ctx.message.delete()
        if name is None:
            return await ctx.send("Please give me the new name of the channel")
        ID = ctx.message.channel.name.split("-",1)[1]
        await ctx.message.channel.edit(reason = "Renaming of support ticket", name = f"{name}-{ID}")

    @commands.command(pass_context = True)
    async def tag(self, ctx, name = ""):
        await ctx.message.delete()
        if name is None:
            return await ctx.send("Please tell me who to tag; dev, admin, owner")
        await ctx.message.channel.edit(reason = "Adding tag to support ticket", name = f"{name}-{ctx.message.channel.name}")

def setup(bot):
    bot.add_cog(support(bot))