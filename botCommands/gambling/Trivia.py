from discord.ext import commands
import discord
from botCommands.gambling.handler.triviaHandler import TriviaClass
from config import config
from discord.ext.commands import cooldown, BucketType

class Trivia(commands.Cog):
    @commands.command(aliases=["tr"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def trivia(self, ctx, difficulty: str.lower = None):
        if difficulty == None:
            embed = discord.Embed(title="Trivia", colour=config.EMBED_COLOR)
            embed.add_field(name="Difficulties:", value="easy, medium, hard", inline=False)
            embed.add_field(name="Payout:", value="**easy** - 10\n"
                                                  "**medium** - 20\n"
                                                  "**hard** - 30\n"
                                                  "**2 options** - 1x\n"
                                                  "**3 options** - 1.2x\n"
                                                  "**4 options** - 1.5x", inline=False)
            await ctx.send(embed=embed)
        elif difficulty not in ("easy", "medium", "hard"):
           await ctx.send("Difficulty not avaliable")
        else:
            embed = discord.Embed(title="Trivia starting!", colour=config.EMBED_COLOR)
            message = await ctx.send(embed=embed)
            trivia = TriviaClass(ctx, message, difficulty)
            await trivia.trivia()

def setup(bot):
    bot.add_cog(Trivia(bot))
