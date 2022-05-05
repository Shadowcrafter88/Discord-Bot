import discord
from discord.ext import commands
from config import config
import datetime
import random
import time

from botCommands.gambling.economy import Economy


class Manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economy = Economy()

    @commands.Cog.listener()
    async def on_ready(self):
        Economy.createDB(self)

    @commands.command(
        name="register"
    )
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def register(self, ctx):
        member = ctx.author

        Economy.openDB(self)

        try:
            selected = Economy.getFromId(self, member.id)
            embed = discord.Embed(title="You are already registred!", color=config.ERROR_EMBED_COLOR)
            embed.set_thumbnail(url=f"{member.display_avatar.url}")
            embed.add_field(name="Id", value=f"{selected[0]}", inline=True)
            embed.add_field(name="Credits", value=f"{selected[1]}", inline=True)
            await ctx.send(embed=embed)
        except Exception as e:
            Economy.setStartingCredits(self, member.id)

            embed = discord.Embed(title="Account registerd!",
                                  description="Your account has been saved to our databases.", color=config.EMBED_COLOR)
            await ctx.send(embed=embed)

        Economy.closeDB(self)


    @commands.command(
        aliases=["setMoney", "set_money", "set_credits"],
        name='setCredits'
    )
    @commands.has_permissions(administrator=True)
    async def setCredits(self, ctx, amount=1000, user: discord.Member = None):
        if ctx.message.guild.id == 283525994583818240:
            if user == None:
                user = ctx.author
            try:
                id = user.id
            except Exception as e:
                embed = discord.Embed(title=f"User {user.display_name} not found!", color=config.ERROR_EMBED_COLOR)
                await ctx.send(embed=embed)
                return

            try:
                Economy.openDB(self)
                Economy.setCredits(self, id, amount)
                Economy.closeDB(self)

            except Exception as e:
                embed = discord.Embed(title=f"{user.display_name} is not registerd!", color=config.ERROR_EMBED_COLOR)
                await ctx.send(embed=embed)
                return
            else:
                embed = discord.Embed(title=f"{user.display_name}'s credits set to {amount}!",
                                      description=f"The credits of {user.id} were set to {amount}.",
                                      color=config.EMBED_COLOR)
                await ctx.send(embed=embed)

    @commands.command(
        aliases=["show", "user", "money", "credits"],
        name='profile'
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def profile(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
            you = True
        try:
            Economy.openDB(self)
            selected = Economy.getFromId(self, user.id)
            Economy.closeDB(self)
            embed = discord.Embed(title=f"{user.display_name}", color=config.EMBED_COLOR)
            embed.set_thumbnail(url=f"{user.display_avatar.url}")
            embed.add_field(name="Id", value=f"{selected[0]}", inline=True)
            embed.add_field(name="Credits", value=f"{selected[1]}", inline=True)
            await ctx.send(embed=embed)
        except Exception as e:
            if you:
                embed = Economy.sendNotRegistred(self, True)
            else:
                embed = Economy.sendNotRegistred(self, False)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 72000, commands.BucketType.user)
    async def daily(self, ctx):
        try:
            daily = random.randint(50, 200)
            credits = Economy.ocAddCredits(self, ctx.author.id, daily)
            embed = discord.Embed(title=f"You got {daily} credits from daily!", description=f"You can use this command every 20 hours.",
                                  color=config.EMBED_COLOR)
            embed.add_field(name="Profit", value=f"**{daily}** credits", inline=False)
            embed.add_field(name="Your Credits", value=f"{credits}", inline=True)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = Economy.sendNotRegistred(self, True)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        try:
            work = random.randint(10, 70)
            credits = Economy.ocAddCredits(self, ctx.author.id, work)
            embed = discord.Embed(title=f"You got {work} credits from work!",
                                  description=f"You can use this command every hour.",
                                  color=config.EMBED_COLOR)
            embed.add_field(name="Profit", value=f"**{work}** credits", inline=False)
            embed.add_field(name="Your Credits", value=f"{credits}", inline=True)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = Economy.sendNotRegistred(self, True)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def broke(self, ctx):
        #try:
            credits = Economy.ocGetCredits(id=ctx.author.id)
            print(credits)
            if credits < 10:
                broke = random.randint(10, 30)
                credits = Economy.ocAddCredits(self, ctx.author.id, broke)
                embed = discord.Embed(title=f"You got {broke} credits from being broke!",
                                      description=f"You can use this command every time\n"
                                                  "you got less than **10** credits.",
                                      color=config.EMBED_COLOR)
                embed.add_field(name="Profit", value=f"**{broke}** credits", inline=False)
                embed.add_field(name="Your Credits", value=f"{credits}", inline=True)
            else:
                embed = discord.Embed(title=f"You cant use this command with more than 10 credits!",
                                      description=f"You can use this command every time\n"
                                                  "you got less than **10** credits.",
                                      color=config.EMBED_COLOR)
                embed.add_field(name="Your Credits", value=f"{credits}", inline=False)
            await ctx.send(embed=embed)
        #except Exception as e:
        #    embed = Economy.sendNotRegistred(self, True)
        #    await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Manager(bot))