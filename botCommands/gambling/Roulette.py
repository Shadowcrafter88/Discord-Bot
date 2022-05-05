import discord
from botCommands.gambling.economy import Economy
from discord.ext import commands
from config import config
import random

class Roulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='roulette'
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def roulette(self, ctx, *args):
        user = ctx.author
        try:
            Economy.openDB(self)
            selected = Economy.getFromId(self, user.id)
            Economy.closeDB(self)

            credits = selected[1]


            if len(args) == 0:
                embed = discord.Embed(title="Bet types",
                                      description="<black/red/green>, <0-36>, <high/low>, <odd/even>", color=config.EMBED_COLOR)
                embed.add_field(name="Info", value="**black/red/green** if bot rolls your color you win\n"
                                                   "**0-36** if bot rolls your number you win\n"
                                                   "**high/low** low = 1-18, high = 19-36\n"
                                                   "**odd/even** odd = 1, 3, 5 ..., 35, even = 2, 4, 6, ..., 36", inline=False)
                embed.add_field(name="Winnnings", value="**black/red** - 2x\n"
                                                        "**0-36** - 35x\n"
                                                        "**high/low** - 2x\n"
                                                        "**odd/even** - 2x", inline=False)
                embed.add_field(name="Numbers", value="Green: **0**\n"
                                                      "Black: **2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35**\n"
                                                      "Red: **1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36**", inline=False)
                embed.add_field(name="Usage", value="**+roulette <bet type> <bet>**", inline=False)
                await ctx.send(embed=embed)
            elif len(args) >= 3:
                embed = discord.Embed(title="You can only bet for one thing!",
                                      description=f"You were trying to bet for {len(args) - 1}.", color=config.ERROR_EMBED_COLOR)
                await ctx.send(embed=embed)
            elif len(args) < 2:
                embed = discord.Embed(title="You have to do a bet and than the bet amount!",
                                      description=f"{config.BOT_PREFIX}roulette <bet> <bet amount>",
                                      color=config.ERROR_EMBED_COLOR)
                await ctx.send(embed=embed)
            else:
                try:
                    betAmount = int(args[len(args) - 1])
                except Exception as e:
                    embed = discord.Embed(title="Your last argument has to be a number!", color=config.ERROR_EMBED_COLOR)
                    await ctx.send(embed=embed)
                    return
                if credits < betAmount:

                    await ctx.send(embed=Economy.sendNotEnoughCredits(self, betAmount, credits))
                elif betAmount <= 0:
                    embed = discord.Embed(title="Your bet has to be greater than 0!", color=config.ERROR_EMBED_COLOR)
                    await ctx.send(embed=embed)
                else:
                    won = False
                    rolled = random.randint(0, 36)

                    if rolled == 2 or rolled == 4 or rolled == 6 or rolled == 8 or rolled == 10 or rolled == 11 or rolled == 13 or rolled == 15 or rolled == 17 or rolled == 20 or rolled == 22 or rolled == 24 or rolled == 26 or rolled == 28 or rolled == 29 or rolled == 31 or rolled == 33 or rolled == 35:
                        color = 0x000000
                        if args[0] == "black":
                            times = 2
                            won = True
                    else:
                        if rolled != 0:
                            color = 0xff0000
                            if args[0] == "red":
                                times = 2
                                won = True
                        else:
                            color = 0x00ff00
                            if args[0] == "green":
                                times = 35
                                won = True
                    try:
                        bet = int(args[0])
                        if bet == rolled:
                            times = 35
                            won = True
                        else:
                            won = False
                    except Exception as e:
                        if args[0] == "odd":
                            if rolled != 0 and (rolled % 2) == 1:
                                times = 2
                                won = True
                        elif args[0] == "even":
                            if rolled != 0 and (rolled % 2) == 0:
                                times = 2
                                won = True
                        elif args[0] == "high":
                            if rolled >= 19:
                                times = 2
                                won = True
                        elif args[0] == "low":
                            if 1 <= rolled <= 18:
                                times = 2
                                won = True
                    embed = discord.Embed(title=f"{user.display_name}", color=color)
                    if won:
                        profit = betAmount * (times - 1)
                        credits += profit
                        embed.add_field(name="You won!", value=f"Ball rolled **{rolled}**", inline=True)
                    else:
                        profit = 0 - betAmount
                        credits -= betAmount
                        embed.add_field(name="You lost!", value=f"Ball rolled **{rolled}**", inline=True)
                    embed.add_field(name="Profit", value=f"**{profit}** credits", inline=False)
                    embed.add_field(name="Your Credits", value=f"{credits}", inline=True)

                    await ctx.send(embed=embed)

                    Economy.openDB(self)
                    Economy.setCredits(self, user.id, credits)
                    Economy.closeDB(self)

        except Exception as e:
            embed = discord.Embed(title=f"You are not registred!",
                                  description=f"Do `{config.BOT_PREFIX}register` to do so.", color=config.ERROR_EMBED_COLOR)
            await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Roulette(bot))
