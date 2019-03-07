import discord
import json
from discord.utils import get
from discord.ext import commands
from discord import Emoji
from configparser import ConfigParser

#rewrite_compatible

class support:
    def __init__(self, bot):
        self.parser = ConfigParser()
        self.parser.read("config.ini")
        self.perms = list(map(int, self.parser.get("settings","permissions").split(",")))
        self.bot = bot

    @commands.command(pass_context = True)
    async def addclient(self, ctx,*, user=""):
        if ctx.message.channel.category == self.bot.get_channel(543909220022484993):
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
        support = self.bot.get_channel(id=543909220022484993)
        overwrites = {
            ctx.message.author: discord.PermissionOverwrite(read_messages=True, attach_files=True),
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.get_role(441798963834781707): discord.PermissionOverwrite(read_messages=True),
            ctx.guild.get_role(440017482833723393): discord.PermissionOverwrite(read_messages=True),
            ctx.guild.get_role(441798756996743178): discord.PermissionOverwrite(read_messages=True),
            ctx.guild.get_role(482387364489199616): discord.PermissionOverwrite(read_messages=True),
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
        embed=discord.Embed(title=" ", description=f"Hi {ctx.message.author.mention} \nThank you contacting the Support Team of the BigCityRP Community. A Support Member will be with you as soon as they are available.  \n \nPlease provide a detailed description of the support issue in the chat below. If you would like to have anyone else added to this ticket, please list them in the chat so they may be added by our Support Team.", color=0xff8000)
        embed.add_field(name="Subject", value=subject, inline=True)
        embed.add_field(name="Ticket ID", value=Tid, inline=True)
        await channel.send(embed=embed)
        log=discord.Embed(title=" ", description=f"By {ctx.message.author} with ID {Tid}", color=0x26ff00)
        log.set_author(name="Ticket opened")
        log.add_field(name="Subject", value=f"{subject} - <#{channel.id}>", inline=False)
        channel = self.bot.get_channel(543909793446887464)
        await channel.send(embed=log)

    @commands.command(pass_context = True)
    async def close(self, ctx,*, reason = ""):
        if ctx.message.channel.category == self.bot.get_channel(543909220022484993):
            if ctx.message.channel == self.bot.get_channel(546658382149582848):
                return ctx.message.delete()
            if not reason:
                rsn = "No reason specified"
            else:
                rsn = reason
            await ctx.message.delete()
            ID = ctx.message.channel.name.split("-")[-1]
            print(ID)
            file = open(f"ticket-{ID}.txt", "w")
            async for message in ctx.message.channel.history(limit = 500, reverse = True):
                file.write(f"{str(message.author)} - {message.content}\n")
            file.close()
            sendfile = discord.File(fp = f"ticket-{ID}.txt", filename= f"ticket-{ID}-transcript.txt")
            log=discord.Embed(title=" ", description=f"By {ctx.message.author}", color=0xff0000)
            log.set_author(name="Ticket closed")
            log.add_field(name="ID", value=ctx.message.channel, inline=True)
            log.add_field(name="Reason", value=rsn, inline=True)
            with open('tickets.json', encoding='utf-8') as f:
                tickets = json.load(f)
            for ticket in tickets["client"]:
                if str(ticket["id"]) ==ID:
                    client = ticket["name"]
                    member = discord.utils.get(ctx.message.guild.members, id=client)
            channel = self.bot.get_channel(543909793446887464)
            await channel.send(embed=log, file = sendfile)
            await ctx.message.channel.delete()
            embed=discord.Embed(title=" ")
            embed.set_author(name="Your ticket was closed")
            embed.set_thumbnail(url=ctx.message.author.avatar_url)
            embed.add_field(name=f"{ctx.message.author.display_name} closed your ticket:", value=rsn, inline=False)
            embed.set_footer(text="I attached the transcript in case you need it in the future")
            await member.send(file=sendfile, embed=embed)

    @commands.command(pass_context = True)
    async def tickets(self, ctx, member:discord.Member = ""):
        if not any(role.id in self.perms for role in ctx.author.roles):
            return await ctx.send("You are not allowed to do this!")
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
        if not any(role.id in self.perms for role in ctx.author.roles):
            return await ctx.send("You are not allowed to do this!")
        if id is None:
            return await ctx.send("Please give me a Ticket ID")
        try:
            sendfile = discord.File(fp = f"ticket-{id}.txt", filename= f"ticket-{id} chat log.txt")
            await ctx.send(f"This is the chat of ticket {id}", file=sendfile)
        except:
            await ctx.send(f"I was not able to find a transcript with ID {id}. It is possible that this ticket has not been closed yet")

    @commands.command(pass_context = True)
    async def rename(self, ctx, *,name = ""):
        if not any(role.id in self.perms for role in ctx.author.roles):
            return await ctx.send("You are not allowed to do this!")
        print(ctx.message.channel.category)
        print(self.bot.get_channel(543909793446887464))
        if ctx.message.channel.category == self.bot.get_channel(543909220022484993):
            await ctx.message.delete()
            if name is None:
                return await ctx.send("Please give me the new name of the channel")
            ID = ctx.message.channel.name.split("-")[-1]
            embed=discord.Embed(title=" ", color=0xffff00)
            embed.add_field(name="Ticket was renamed", value=f"New channel name is {name}-{ID}", inline=False)
            await ctx.message.channel.edit(reason = "Renaming of support ticket", name = f"{name}-{ID}")
            await ctx.send(embed=embed)

    @commands.command(pass_context = True)
    async def tag(self, ctx, name = ""):
        if not any(role.id in self.perms for role in ctx.author.roles):
            return await ctx.send("You are not allowed to do this!")
        if ctx.message.channel.category == self.bot.get_channel(543909220022484993):
            await ctx.message.delete()
            if name is None:
                return await ctx.send("Please tell me who to tag; dev, admin, owner")
            await ctx.message.channel.edit(reason = "Adding tag to support ticket", name = f"{name}-{ctx.message.channel.name}")

def setup(bot):
    bot.add_cog(support(bot))