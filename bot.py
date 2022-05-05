import os
import json
import time

import discord
from discord.ext import commands
from discord.ext import tasks

from config import config
from botCommands.musicbot.audiocontroller import AudioController
from botCommands.musicbot.settings import Settings
from botCommands.musicbot.utils import guild_to_audiocontroller, guild_to_settings

import botCommands.allCommands.Userinfo
import botCommands.allCommands.Server
#import botCommands.allCommands.Fun
import botCommands.allCommands.Owner
import botCommands.allCommands.Help
import botCommands.allCommands.XBeispiel
import botCommands.allCommands.chatBot.Chat
import botCommands.allCommands.reminder.Reminder
from botCommands.allCommands.reminder import TimeManager

import botCommands.gambling.Manager
import botCommands.gambling.Roulette
import botCommands.gambling.Flip
import botCommands.gambling.Blackjack
import botCommands.gambling.Trivia

cogs = [botCommands.allCommands.Userinfo,
        botCommands.allCommands.Server,
        #botCommands.allCommands.Fun,
        botCommands.allCommands.Owner,
        botCommands.allCommands.Help,
        botCommands.allCommands.XBeispiel,
        botCommands.allCommands.chatBot.Chat,

        botCommands.gambling.Manager,
        botCommands.gambling.Roulette,
        botCommands.gambling.Flip,
        botCommands.gambling.Blackjack,
        botCommands.gambling.Trivia,
        botCommands.allCommands.reminder.Reminder]

initial_extensions = ['botCommands.musicbot.commands.music',
                      'botCommands.musicbot.commands.general',
                      'botCommands.musicbot.plugins.button']
#fffffffffffffffffffffffff
test = False
#fffffffffffffffffffffffff
if test == True:
    bot = commands.Bot(command_prefix=config.TEST_BOT_PREFIX,
                       pm_help=True, case_insensitive=True, help_command=None)
else:
    bot = commands.Bot(command_prefix=config.BOT_PREFIX,
                       pm_help=True, case_insensitive=True, help_command=None)

for i in range(len(cogs)):
    try:
        cogs[i].setup(bot)
    except Exception as e:
        print(e)

if __name__ == '__main__':

    config.ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
    config.COOKIE_PATH = config.ABSOLUTE_PATH + config.COOKIE_PATH

    if config.BOT_TOKEN == "":
        print("Error: No bot token!")
        exit

    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(e)

async def status_task():
    await bot.change_presence(activity=discord.Game('!h help'), status=discord.Status.online)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} ({bot.user.id})\n')
    guild_count = 0
    biggest_server_users = 0
    biggest_server_name = ""
    for guild in bot.guilds:
        await register(guild)
        if guild.member_count > biggest_server_users:
            biggest_server_users = guild.member_count
            biggest_server_name = guild.name

        guild_count += 1
        print("Joined {}".format(guild.name))

    print(config.STARTUP_COMPLETE_MESSAGE)

    bot.loop.create_task(status_task())

    data = json.load(open("config/databases/infos.json"))
    if data["is_reloaded"] == True:
        channel = bot.get_channel(data["channel_id"])

        embed = discord.Embed(title=f"{bot.user.display_name} Reloaded", colour=config.EMBED_COLOR)
        embed.set_thumbnail(url=bot.user.display_avatar.url)
        embed.add_field(name=f"Server Count: {guild_count}", value=f"The biggest Server is **{biggest_server_name}**\n"
                                                                   f"with **{biggest_server_users}** users", inline=False)
        await channel.send(embed=embed)

        reloadInfo = {
            'is_reloaded': False,
        }
        data = json.dumps(reloadInfo)
        with open("config/databases/infos.json", 'w') as json_file:
            json_file.write(data)
            json_file.close()
    else:
        channel = bot.get_channel(875048651129507891)
        embed = discord.Embed(title=f"{bot.user.display_name} Started", colour=config.EMBED_COLOR)
        embed.set_thumbnail(url=bot.user.display_avatar.url)
        embed.add_field(name=f"Server Count: {guild_count}", value="The biggest Server is\n"
                                                                   f"**{biggest_server_name}** with **{biggest_server_users}** users",
                        inline=False)
        await channel.send(embed=embed)


@bot.event
async def on_guild_join(guild):
    print(guild.name)
    await register(guild)


async def register(guild):

    guild_to_settings[guild] = Settings(guild)
    guild_to_audiocontroller[guild] = AudioController(bot, guild)

    sett = guild_to_settings[guild]

    if config.GLOBAL_DISABLE_AUTOJOIN_VC == True:
        return

    vc_channels = guild.voice_channels

    if sett.get('vc_timeout') == False:
        if sett.get('start_voice_channel') == None:
            try:
                await guild_to_audiocontroller[guild].register_voice_channel(guild.voice_channels[0])
            except Exception as e:
                print(e)

        else:
            for vc in vc_channels:
                if vc.id == sett.get('start_voice_channel'):
                    try:
                        await guild_to_audiocontroller[guild].register_voice_channel(vc_channels[vc_channels.index(vc)])
                    except Exception as e:
                        print(e)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        rest = error.retry_after
        time = ""
        if rest / 3600 >= 1:
            time += f"{int(rest / 3600)}h "
            rest %= 3600
        if rest / 60 >= 1:
            time += f"{int(rest / 60)}min "
            rest %= 60
        time += f"{rest:.0f}sec"
        embed = discord.Embed(title=f"This command is currently on cooldown!", description=f"Try again in {time}.",
                              color=config.ERROR_EMBED_COLOR)
        await ctx.send(embed=embed)


#Check reminders
@tasks.loop(minutes=1)
async def reminderCheck():
    try:
        remembers = TimeManager.remind()
        for remember in remembers:
            user = await bot.fetch_user(int(remember[0]))
            embed = discord.Embed(title=remember[2], description=remember[1], colour=config.EMBED_COLOR)
            await user.send(embed=embed)

    except Exception as e:
        print(e)

reminderCheck.start()

if test == True:
    bot.run(config.TEST_BOT_TOKEN, reconnect=True)
else:
    bot.run(config.BOT_TOKEN, reconnect=True)
