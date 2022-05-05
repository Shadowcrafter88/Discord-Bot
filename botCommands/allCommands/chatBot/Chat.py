import discord
from discord.ext import commands
from config import config

import aiml
import os
import re

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.aiml_kernel = aiml.Kernel()

        if os.path.isfile("config/bot_brain.brn"):
            self.aiml_kernel.bootstrap(brainFile="config/bot_brain.brn")
        else:
            self.aiml_kernel.bootstrap(learnFiles="config/std-startup.xml", commands="load aiml b")
            self.aiml_kernel.saveBrain("config/bot_brain.brn")


    @commands.command(
        aliases=["c"],
        name='chat')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def chat(self, ctx, *args):
        message = " ".join(args)
        if message == "":
            embed = discord.Embed(title="Empty message received.", colour=config.ERROR_EMBED_COLOR)
            embed.set_thumbnail(url=f"{self.bot.user.display_avatar.url}")
            await ctx.send(embed=embed)
            return

        #response = self.get_response(message)
        #if response == "":
        response = self.aiml_kernel.respond(message)
        if response == "":
            embed = discord.Embed(title="I don't have a response for that, sorry.", colour=config.ERROR_EMBED_COLOR)
            embed.set_thumbnail(url=f"{self.bot.user.display_avatar.url}")
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title=f"{response}", colour=config.EMBED_COLOR)
        embed.set_thumbnail(url=f"{self.bot.user.display_avatar.url}")
        await ctx.send(embed=embed)

    @commands.command(
        aliases=["cu"],
        name='chatUpdate')
    @commands.has_permissions(administrator=True)
    async def chatUpdate(self, ctx):
        if ctx.message.guild.id == config.OWNDER_SERVER:
            embed = discord.Embed(title="I am going to update my brain!", colour=config.EMBED_COLOR)
            embed.set_thumbnail(url=f"{self.bot.user.display_avatar.url}")
            message = await ctx.send(embed=embed)
            self.aiml_kernel.bootstrap(learnFiles="config/std-startup.xml", commands="load aiml b")
            self.aiml_kernel.saveBrain("config/bot_brain.brn")
            embed = discord.Embed(title="My brain has been updated!", colour=config.EMBED_COLOR)
            embed.set_thumbnail(url=f"{self.bot.user.display_avatar.url}")
            await message.edit(embed=embed)

    @commands.command(
        aliases=["ar"],
        name='addResponse')
    @commands.has_permissions(administrator=True)
    async def addResponse(self, ctx, message: str, response: str):
        if ctx.message.guild.id == config.OWNDER_SERVER:
            f = open("botCommands/allCommands/chatBot/helix/_helix/added.aml", "r")
            inside = f.read()
            f.close()

            if inside.find(message) != -1:
                embed = discord.Embed(title="Command already exists!",
                                      colour=config.ERROR_EMBED_COLOR)
                await ctx.send(embed=embed)
                return

            inside = inside[:inside.rfind("</aiml>")]

            add = "\n    <category>\n" \
                  f"        <pattern>{message}</pattern>\n" \
                  f"        <template>{response}</template>\n" \
                  "    </category>\n"

            inside += add + "</aiml>"
            f = open("botCommands/allCommands/chatBot/helix/_helix/added.aml", "w")
            f.write(inside)
            f.close()

            embed = discord.Embed(title="Adding new command to my database!", description=add, colour=config.EMBED_COLOR)
            await ctx.send(embed=embed)

    def message_probability(self, user_message, recognised_words, single_response=False, required_words=[]):
        message_certainty = 0
        has_required_words = True

        for word in user_message:
            if word in recognised_words:
                message_certainty += 1

        percentage = float(message_certainty) / float(len(required_words))

        for word in required_words:
            if word not in user_message:
                has_required_words = False
                break

        if has_required_words or single_response:
            return int(percentage*100)
        else:
            return 0

    def check_all_messages(self, message):
        highest_prob_list = {}

        def response(bot_response, list_of_words, single_response=False, required_words=[]):
            nonlocal highest_prob_list
            highest_prob_list[bot_response] = self.message_probability(message, list_of_words, single_response, required_words)

        # Responses ---------------------------------------------------------------------------------
        response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
        response('Thank you!', ['i', 'love', 'you'], required_words=['i'])

        best_match = max(highest_prob_list, key=highest_prob_list.get)


        return "" if highest_prob_list[best_match] < 200 else best_match

    def get_response(self, input):
        split_message = re.split(r'\s+|[,;?!.-]\s*', input.lower())
        response = self.check_all_messages(split_message)
        return response

def setup(bot):
    bot.add_cog(Chat(bot))