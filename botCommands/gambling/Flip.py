import discord
from botCommands.gambling.economy import Economy
from discord.ext import commands
from config import config
import random

class Flip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        aliases=["coinFlip", "coin"],
        name='flip'
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def flip(self, ctx, *args):
        user = ctx.author
        try:
            Economy.openDB(self)
            selected = Economy.getFromId(self, user.id)
            Economy.closeDB(self)
            credits = selected[1]

        except Exception as e:
            embed = Economy.sendNotRegistred(self, True)
            await ctx.send(embed=embed)

        else:
            if len(args) == 0 or len(args) > 2:
                embed = discord.Embed(title="Bet types",
                                      description="<1/2>, <tails/heads>",
                                      color=config.EMBED_COLOR)
                embed.add_field(name="Info",
                                value="**tails/heads** if the coin lands on the side you bet on you win.\n",
                                inline=False)
                embed.add_field(name="Winnnings", value="**tails/heads** - 2x\n"
                                                        "**1/2** - 2x", inline=False)
                embed.add_field(name="Usage", value=f"**{config.BOT_PREFIX}flip <bet amount>**", inline=False)
                await ctx.send(embed=embed)
            else:
                try:
                    betAmount = int(args[len(args) - 1])
                except Exception as e:
                    embed = discord.Embed(title="Your last argument has to be a number!",
                                          color=config.ERROR_EMBED_COLOR)
                    await ctx.send(embed=embed)
                else:
                    if credits < betAmount:
                        embed = discord.Embed(title="You don't have enough credits!", color=config.ERROR_EMBED_COLOR)
                        embed.add_field(name="Your credits:", value=f"{credits}", inline=False)
                        embed.add_field(name="Your bet:", value=f"{betAmount}", inline=False)
                        await ctx.send(embed=embed)
                    else:
                        won = False
                        flip = random.randint(0, 36)

                        if args[0] == "1":
                            if flip >= 19:
                                coinFlip = "1"
                                won = True
                            else:
                                coinFlip = "0"

                        elif args[0] == "0":
                            if 1 <= flip <= 16:
                                coinFlip = "0"
                                won = True
                            else:
                                coinFlip = "1"

                        elif args[0] == "tails" or args[0] == "tail" or args[0] == "number":
                            if flip >= 19:
                                coinFlip = "tails"
                                won = True
                            else:
                                coinFlip = "heads"

                        elif args[0] == "heads" or args[0] == "head":
                            if 1 <= flip <= 16:
                                coinFlip = "heads"
                                won = True
                            else:
                                coinFlip = "tails"
                        else:
                            embed = discord.Embed(title="Bet types",
                                                  description="<1/2>, <tails/heads>",
                                                  color=config.EMBED_COLOR)
                            embed.add_field(name="Info",
                                            value="**tails/heads** if the coin lands on the side you bet on you win.\n",
                                            inline=False)
                            embed.add_field(name="Winnnings", value="**tails/heads** - 2x\n"
                                                                    "**1/2** - 2x", inline=False)
                            embed.add_field(name="Usage", value=f"**{config.BOT_PREFIX}flip <bet amount>**",
                                            inline=False)
                            await ctx.send(embed=embed)
                            return

                        embed = discord.Embed(title=f"{user.display_name}", color=config.EMBED_COLOR)
                        if won:
                            profit = betAmount
                            credits += betAmount
                            embed.add_field(name="You won!", value=f"Coin flipped **{coinFlip}**", inline=True)
                        else:
                            profit = 0 - betAmount
                            credits -= betAmount
                            embed.add_field(name="You lost!", value=f"Coin flipped **{coinFlip}**", inline=True)
                        embed.add_field(name="Profit", value=f"**{profit}** credits", inline=True)
                        embed.add_field(name="Your Credits", value=f"{credits}", inline=False)
                        await ctx.send(embed=embed)

                        Economy.openDB(self)
                        Economy.setCredits(self, user.id, credits)
                        Economy.closeDB(self)



def setup(bot):
    bot.add_cog(Flip(bot))
