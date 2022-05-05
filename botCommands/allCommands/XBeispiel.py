import discord
from discord.ext import commands
from discord.ui import Button, View


class XBeispiel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        aliases=["button"],
        name='buttonTest'
    )
    async def buttonTest(self, ctx):
        btn1 = Button(
            label="Test",
            style=discord.ButtonStyle.green,
            emoji="😊"
        )
        view = View()
        view.add_item(btn1)
        await ctx.send("Test 123", view=view)

    @commands.command()
    async def htmlTest(self, ctx):
        await ctx.send("Test")
        try:
            await ctx.message.add_reaction("<:white_check_mark:824906654385963018>")
            await ctx.send("Should have worked")
        except Exception as e:
            await ctx.send(e)
            await ctx.send("Error")


    @commands.command()
    async def Test123(self, ctx):
        user = await self.bot.fetch_user(207376974815952896)
        await user.send("@DanielCST/おにい ちゃん#1987 The server room is on fire!")
        user = await self.bot.fetch_user(675399364172185622)
        await user.send("@DanielCST/おにい ちゃん#1987 The server room is on fire!")

    @commands.command()
    async def userTest(self, ctx):
        if ctx.author.id == 675399364172185622:
            await ctx.send("Yes")
        else:
            await ctx.send("No")

        if ctx.author.id == 675631473902092293 or ctx.author.id == 755456244612857947 or ctx.author.id == 675399364172185622:
            await ctx.send("Minecraft Server ist gestoppt!!!")
            return



def setup(bot):
    bot.add_cog(XBeispiel(bot))