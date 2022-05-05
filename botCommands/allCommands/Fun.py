import discord
import random
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='hi')
    async def hi(self, ctx):
        await ctx.send('Hello')

    @commands.command(
        name='minecraft')
    async def minecraft(self, ctx):
        embed = discord.Embed(title="Hex", color=0x00fbff)
        embed.set_thumbnail(url="http://hex.ddns.net/Jonas-Hex-Website/Bilder/icon.png")
        embed.add_field(name="Server IP:", value="hex.ddns.net", inline=False)
        embed.add_field(name="Version:", value="1.18.1", inline=False)
        embed.set_footer(text="Join now for free")
        await ctx.send(embed=embed)

    @commands.command(
        name='repeat')
    async def repeat(self, ctx, *args):
        await ctx.send(f'{" ".join(args)}')

    @commands.command(
        name='randnum')
    async def randnum(self, ctx, num1, num2):
        x = int(num1)
        y = int(num2)
        if x < y:
            value = random.randint(x, y)

            embed = discord.Embed(title=f"{value}", color=0x00fbff)
            embed.set_footer(text=f"Zufallszahl zwischen {x} und {y}")
            await ctx.send(embed=embed)
        else:
            value = random.randint(y, x)

            embed = discord.Embed(title=f"{value}", color=0x00fbff)
            embed.set_footer(text=f"Zufallszahl zwischen {x} und {y}")
            await ctx.send(embed=embed)

    @commands.command(
        name='wanted')
    async def wanted(self, ctx, user: discord.Member = None, blackWhite = False, thresh = 100):
        backgroundImg = r'config/databases/pictureManipulation/wanted.jpg'
        tempImg = r'config/databases/pictureManipulation/temp/tempProfile.jpg'


        if user == None:
            user = ctx.author

        wanted = Image.open(backgroundImg)
        asset = user.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((318, 318))

        if blackWhite != False:
            if thresh == 0:
                pfp = pfp.convert('1')
            else:
                fn = lambda x: 255 if x > thresh else 0
                pfp = pfp.convert('L').point(fn, mode='1')

        wanted.paste(pfp, (97, 195))
        wanted.save(tempImg)
        await ctx.send(file=discord.File(tempImg))



    @commands.command(
        name='steve')
    async def steve(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        steve = Image.open(r'config/databases/pictureManipulation/steve.png')
        asset = user.avatar_url_as(size=16)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((8, 8))
        steve.paste(pfp, (4, 0))
        steve = steve.resize((256, 512))
        steve.save(r'config/databases/pictureManipulation/temp/tempProfile.png')
        await ctx.send(file=discord.File(r'config/databases/pictureManipulation/temp/tempProfile.png'))

    @commands.command(
        name='rip')
    async def rip(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        rip = Image.open(r'config/databases/pictureManipulation/rip.png')

        size = 80 - (len(f"{user.nick}") * 3)

        font = ImageFont.truetype(r"config/databases/pictureManipulation/font/ubuntu-title/Ubuntu-Title.ttf", size)

        draw = ImageDraw.Draw(rip)
        try:
            draw.text((330, 284), f"{user.display_name}", font=font, fill=(49, 49, 49))
        except Exception as e:
            draw.text((330, 284), f"{user.display_name}", font=font, fill=(49, 49, 49))


        rip.save(r'config/databases/pictureManipulation/temp/tempProfile.png')
        await ctx.send(file=discord.File(r'config/databases/pictureManipulation/temp/tempProfile.png'))


def setup(bot):
    bot.add_cog(Fun(bot))