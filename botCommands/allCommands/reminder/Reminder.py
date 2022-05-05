import os
import asyncio
import discord
import datetime
from botCommands.allCommands.reminder import TimeManager
from discord.ext import commands
from config import config


class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        TimeManager.createDB()


    @commands.command(
        name='reminder',
        aliases=["remember", "remind"])
    async def reminder(self, ctx, time:str=None, *msg):
        if time is None:
            embed = discord.Embed(title="Reminder", description="!h reminder <time> <message>",
                                  colour=config.EMBED_COLOR, )
            embed.add_field(name="Time", value="amount of minutes + **m**\n"
                                               "amount of hours + **h**\n"
                                               "amount of days + **d**")
            embed.add_field(name="Message", value="The message you want to receive.")
            embed.add_field(name="Information",
                            value="The time must not be greater then 5 days.\n"
                                  "\"m h d\" is the pattern for the time you must use. (~~1d12m~~)\n"
                                  "15 is the maximum amount of reminders.",
                            inline=False)
            await ctx.send(embed=embed)
            return
        if TimeManager.getRemindersAmount(ctx.author.id) >= 15:
            embed = discord.Embed(title="Reminder", description="!h reminder <time> <message>",
                                  colour=config.ERROR_EMBED_COLOR, )
            embed.add_field(name="Time", value="amount of minutes + **m**\n"
                                               "amount of hours + **h**\n"
                                               "amount of days + **d**")
            embed.add_field(name="Message", value="The message you want to receive.")
            embed.add_field(name="Information",
                            value="The time must not be greater then 5 days.\n"
                                  "\"m h d\" is the pattern for the time you must use. (~~1d12m~~)\n"
                                  "**15 is the maximum amount of reminders.**",
                            inline=False)
            await ctx.send(embed=embed)
            return
        try:
            message = " ".join(msg)
            addedTime = datetime.timedelta()
            currTime = datetime.datetime.now()

            if time.find('m') != -1:
                index = time.find('m')
                addedTime += datetime.timedelta(minutes=int(time[:index]))
                time = time[(index + 1):]
            if time.find('h') != -1:
                index = time.find('h')
                addedTime += datetime.timedelta(hours=int(time[:index]))
                time = time[(index + 1):]
            if time.find('d') != -1:
                index = time.find('m')
                addedTime += datetime.timedelta(days=int(time[:index]))
            if addedTime > datetime.timedelta(days=5):
                embed = discord.Embed(title="Reminder", description="!h reminder <time> <message>",
                                      colour=config.ERROR_EMBED_COLOR)
                embed.add_field(name="Time", value="amount of minutes + **m**\n"
                                                   "amount of hours + **h**\n"
                                                   "amount of days + **d**")
                embed.add_field(name="Message", value="The message you want to receive.")
                embed.add_field(name="Information",
                                value="**The time must not be greater then 5 days.**\n"
                                      "\"m h d\" is the pattern for the time you must use. (~~1d12m~~)\n"
                                      "15 is the maximum amount of reminders.",
                                inline=False)
                await ctx.send(embed=embed)
                return
            sendTime = currTime + addedTime
            sendTime = sendTime.strftime("%Y-%m-%d %H:%M:%S")
            TimeManager.addReminder(id=ctx.author.id, time=sendTime, message=message)
            embed = discord.Embed(title=f"Reminder at {sendTime}", description=message, colour=config.EMBED_COLOR)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(e)

    @commands.command(
        name='reminders',
        aliases=["remembers"])
    async def reminders(self, ctx):
        try:
            reminders = TimeManager.getReminders(ctx.author.id)
            embed = discord.Embed(title="Your reminders:", colour=config.EMBED_COLOR)
            for reminder in reminders:
                embed.add_field(name=reminder[2], value=reminder[1], inline=True)
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @commands.command(
        name='delReminder',
        aliases=["delRemember"])
    async def delReminder(self, ctx, *msg):
        message = " ".join(msg)
        TimeManager.removeReminder(id=ctx.author.id, message=message)
        embed = discord.Embed(title=(message + " deleted if existed!"), colour=config.EMBED_COLOR)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Reminder(bot))