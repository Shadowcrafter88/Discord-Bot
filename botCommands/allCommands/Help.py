import discord
from discord.ext import commands
from discord.ui import Button, View
import traceback

from config import config

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        aliases=["hilfe", "h"],
        name='help')
    async def help(self, ctx):

        commandListMusic = ["play", "queue", "skip", "disconnect",
                            "loop", "clear", "shuffle", "pause",
                            "resume", "prev", "songinfo", "history",
                            "volume"]

        commandListGambling = ["register", "profile", "daily",
                               "work", "trivia", "roulette",
                               "blackjack", "flip"]

        commandListFun = ["~~steve~~", "~~wanted~~", "~~rip~~", "chat", "userinfo"]

        commandListReminder = ["reminder", "reminders", "delReminder"]

        commandListMinecraft = ["server.minecraft.start", "server.minecraft.stop", "minecraft", "online"]

        commandListOwner = ["server.start", "raspberry.update", "raspberry.execute", "py.add",
                            "reload", "edittest", "loadtest", "serverList", "\"give me admin\"",
                            "setCredits"]


        name = f"{self.bot.user}"
        name = name[:-5]
        embed = discord.Embed(title=f"{name} Hilfe", color=config.EMBED_COLOR)

        embed.set_thumbnail(url=f"{self.bot.user.display_avatar.url}")

        commandString = ""
        for i in range(len(commandListMusic)):
            if i % 5 == 0:
                commandString += f"\n> `{commandListMusic[i]}`"
            else:
                commandString += f", `{commandListMusic[i]}`"
        embed.add_field(name="Music    :headphones:", value=commandString, inline=False)

        commandString = ""
        for i in range(len(commandListFun)):
            if i % 5 == 0:
                commandString += f"\n> `{commandListFun[i]}`"
            else:
                commandString += f", `{commandListFun[i]}`"
        embed.add_field(name="Fun    :rainbow:", value=commandString, inline=False)

        commandString = ""
        for i in range(len(commandListReminder)):
            if i % 5 == 0:
                commandString += f"\n> `{commandListReminder[i]}`"
            else:
                commandString += f", `{commandListReminder[i]}`"
        embed.add_field(name="Reminder    :bookmark_tabs:", value=commandString, inline=False)

        commandString = ""
        for i in range(len(commandListGambling)):
            if i % 5 == 0:
                commandString += f"\n> `{commandListGambling[i]}`"
            else:
                commandString += f", `{commandListGambling[i]}`"
        embed.add_field(name="Gambling    :game_die:", value=commandString, inline=False)

        if ctx.message.guild.id == config.OWNDER_SERVER:
            commandString = ""
            for i in range(len(commandListMinecraft)):
                if i % 2 == 0:
                    commandString += f"\n> `{commandListMinecraft[i]}`"
                else:
                    commandString += f", `{commandListMinecraft[i]}`"
            embed.add_field(name="Minecraft    :pick:", value=commandString, inline=False)

        if ctx.message.guild.id == config.OWNDER_SERVER:
            role = discord.utils.get(ctx.guild.roles, id=863493406570709032)
            if role in ctx.author.roles:
                commandString = ""
                for i in range(len(commandListOwner)):
                    if i % 3 == 0:
                        commandString += f"\n> `{commandListOwner[i]}`"
                    else:
                        commandString += f", `{commandListOwner[i]}`"
                embed.add_field(name="Owner   :trophy:", value=commandString, inline=False)

        discordLink = Button(label="Join our Discord", url="https://discord.gg/vPCbqGPPMB")
        view = View()
        view.add_item(discordLink)

        embed.set_footer(text=f"Requested von {ctx.author.name} {ctx.author.id}", icon_url=f"{ctx.author.display_avatar.url}")
        await ctx.send(embed=embed, view=view)


    @commands.command(
        name='serverList',
        aliases=["list"])
    @commands.has_permissions(administrator=True)
    async def serverList(self, ctx):
        try:
            name = f"{self.bot.user}"
            name = name[:-5]
            guildList = f"{name} is in the following Discord Servers:\n```"
            i = 1
            for guild in self.bot.guilds:
                guildName = guild.name
                if len(guildName) >= 23:
                    guildName = guildName[:23] + "..."
                else:
                    while len(guildName) <= 25:
                        guildName += " "
                guildName += " {:6s}".format(str(guild.member_count))
                guildList += "{:6s}".format(str(i))
                guildList += f"{guildName}\n"
                i += 1
            guildList += "```"

            await ctx.send(guildList)
        except Exception:
            traceback.print_exc()



def setup(bot):
    bot.add_cog(Help(bot))