import os
import asyncio
from discord.ext import commands


class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        name='server.minecraft.start',
        aliases=[" server.minecraft.start", "minecraft.server.start",
                 "start", " start", "starten"])
    async def startMinecraftServer(self, ctx):
        text = "== Minecraft Server ==\n" \
               "Suche nach anderen Server Instanzen..."
        message = await ctx.send(text)
        response = os.popen(f"ping 192.168.178.2 -c 4").read()
        if "4 received" in response:
            text += "\nVorhandene Instanz gefunden!\n" \
                    "Der server ist bereits online!\n" \
                    "Wenn nicht bitte einen @OWNER fragen!"
            await message.edit(content=f"{text}")
            return
        os.popen('/home/pi/Discord_Bot/Scripts/serverEtherwake.sh')
        text += "\nKeine anderen Instanzen gefunden!\n" \
                "Starte den Server..."
        await message.edit(content=f"{text}")
        online = 0
        count = 0
        loading = "|--------------------|"
        while online == 0:
            response = os.popen(f"ping 192.168.178.2 -c 4").read()
            if "4 received" in response:
                online = 1

            await message.edit(
                content=f"{text}\n{(loading[:((count % 8) + 1)] + '==' + loading[((count % 8) + 3):(20 - (count % 8) - 3)] + '==' + loading[(20 - (count % 8) + 1):])}")
            count += 1
            if count > 100:
                text += "\nServer konnte nicht gestartet werden!"
                await message.edit(content=f"{text}")
                print("! Start von {0} fehlgeschlagen".format(ctx.author.name))
                return
        text += "\nServer gestartet!\n" \
                "ssh Verbindung wird hergestell..."
        await message.edit(content=f"{text}")
        os.popen(f"sshpass -p uB0n_S ssh server@hex.ddns.net -p 12890 -t sh ./screen.sh")
        text += "\nssh Verbindung ist hergestellt!\n" \
                "Minecraft Server wird gestartet..."
        await message.edit(content=f"{text}")
        await asyncio.sleep(10)
        text += "\nMinecraft Server ist gestartet!\nYou can now join >>hex.ddns.net<<"
        await message.edit(content=f"{text}")
        print("- Minecraft Server von {0} gestartet".format(ctx.author.name))


    @commands.command(
        name='server.minecraft.stop',
        aliases=[" server.minecraft.stop", "minecraft.server.stop",
                 "stop.minecraft.server", "stoppen"])
    async def ServerMinecraftStop(self, ctx):
        os.popen('/home/pi/Discord_Bot/botScripts/serverMinecraftStop.sh')
        await ctx.send(f"Minecraft Server ist gestoppt!")
        print("- Minecraft Server von {0} gestoppt".format(ctx.author.name))
        await asyncio.sleep(80)
        print("- Server von {0} heruntergefahren".format(ctx.author.name))


    @commands.command(
        name='server.online',
        aliases=["so", "online",
                 " server.online", " online"])
    async def serverOnline(self, ctx):
        await ctx.send('Checking...')
        response = os.popen(f"ping 192.168.178.2 -c 4").read()
        if "4 received" in response:
            await ctx.send('`{0}`'.format(response))
            await ctx.send(':white_check_mark:  **Online **  :white_check_mark:')
        else:
            await ctx.send('`{0}`'.format(response))
            await ctx.send(':red_circle:  **Offline **  :red_circle:')


def setup(bot):
    bot.add_cog(Server(bot))