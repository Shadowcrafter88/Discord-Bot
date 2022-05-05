import discord
from botCommands.gambling.economy import Economy
from discord.ext import commands
from config import config
import botCommands.gambling.handler.blackjackHandler
import random

class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        aliases=["bj"],
        name='blackjack'
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def blackjack(self, ctx, *args):
        user = ctx.author
        if len(args) == 0:
            embed = discord.Embed(title="Blackjack")
            embed.add_field(name="Currently no Details available", value="", inline=False)
            await ctx.send(embed=embed)
            return
        try:
            bet = int(args[0])
            Economy.openDB(self)
            selected = Economy.getFromId(self, user.id)
            Economy.closeDB(self)
            credits = selected[1]

            if credits < bet:
                await ctx.send(embed=Economy.sendNotEnoughCredits(self, bet, credits))
            elif bet <= 0:
                embed = discord.Embed(title="Your bet has to be greater than 0!", color=config.ERROR_EMBED_COLOR)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Blackjack starting!", colour=config.EMBED_COLOR)
                message = await ctx.send(embed=embed)

                handler = botCommands.gambling.handler.blackjackHandler.BlackjackClass(bet=bet, credits=credits,
                                                                                       ctx=ctx,
                                                                                       message=message)
                await handler.blackjackRecursion()
        except Exception as e:
            embed = Economy.sendNotRegistred(self, True)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Blackjack(bot))
