import html

from urllib.request import urlopen
import json
from config import config
import discord
from botCommands.gambling.utils import random
from botCommands.gambling.utils.i18n import _, locale_doc
from discord.ui import Button, View
from botCommands.gambling.economy import Economy


class TriviaClass:
    def __init__(self, ctx, message, difficulty):
        self.ctx = ctx
        self.message = message
        self.difficulty = difficulty
        self.question = ""
        self.correct_answer = ""
        self.incorrect_answers = []
        self.allAnswers = []

    async def get_question(self):
        with urlopen(f"https://opentdb.com/api.php?amount=1&difficulty={self.difficulty}") as url:
            ret = json.loads(url.read().decode())
        if ret["response_code"] != 0:
            raise Exception("response error")
        ret = ret["results"][0]
        self.question = html.unescape(ret["question"])
        self.correct_answer = html.unescape(ret["correct_answer"])
        for i in ret["incorrect_answers"]:
            self.incorrect_answers.append(i)

    async def result(self, won=False):
        try:
            credits = Economy.ocGetCredits(self, self.ctx.author.id)
        except Exception as e:
            credits = 0
        if won == True:
            money = 10
            if self.difficulty == "medium":
                money = 20
            elif self.difficulty == "hard":
                money = 30
            multiplier = 1
            if len(self.allAnswers) == 3:
                multiplier = 1.2
            elif len(self.allAnswers) == 4:
                multiplier = 1.5
            profit = round(money * multiplier)
            credits += profit
            embed = discord.Embed(title="CORRECT Answer!", description=f"***{self.question}***", color=config.EMBED_COLOR)
        else:
            profit = 0
            embed = discord.Embed(title="WRONG Answer!", description=f"***{self.question}***", color=config.EMBED_COLOR)
        embed.add_field(name="Difficulty:", value=f"{self.difficulty}", inline=False)
        embed.add_field(name="Profit", value=f"**{profit}** credits", inline=False)
        embed.add_field(name="Your Credits", value=f"{credits}", inline=True)
        embed.set_footer(text=f"Question to {self.ctx.author.name} {self.ctx.author.id}",
                         icon_url=f"{self.ctx.author.display_avatar.url}")
        await self.message.edit(embed=embed)
        Economy.ocAddCredits(self, self.ctx.author.id, profit)

    async def formatButtons(self, button1, button2, button3=None, button4=None):
        view = View(timeout=10)

        if button1.label == self.correct_answer:
            button1.style = discord.ButtonStyle.green
        button1.disabled = True
        view.add_item(button1)

        if button2.label == self.correct_answer:
            button2.style = discord.ButtonStyle.green
        button2.disabled = True
        view.add_item(button2)
        if button3 is not None:
            if button3.label == self.correct_answer:
                button3.style = discord.ButtonStyle.green
            button3.disabled = True
            view.add_item(button3)
        if button4 is not None:
            if button4.label == self.correct_answer:
                button4.style = discord.ButtonStyle.green
            button4.disabled = True
            view.add_item(button4)

        await self.message.edit(view=view)

    async def trivia(self):
        try:
            await self.get_question()
        except Exception:
            return await self.ctx.send(_("Error generating question."))
        else:
            embed = discord.Embed(title=f"{self.question}", description="Trivia", color=config.EMBED_COLOR)
            embed.add_field(name="Difficulty:", value=f"{self.difficulty}", inline=False)
            embed.set_footer(text=f"Question to {self.ctx.author.name} {self.ctx.author.id}",
                             icon_url=f"{self.ctx.author.display_avatar.url}")
            allAnswers = self.incorrect_answers
            allAnswers.append(self.correct_answer)

            self.allAnswers = allAnswers
            allAnswers = random.shuffle(allAnswers)

            reference = self

            view = View(timeout=30)

            if len(allAnswers) >= 2:
                first = allAnswers[0]
                second = allAnswers[1]
                button1 = Button(label=f"{first}", style=discord.ButtonStyle.blurple)
                button2 = Button(label=f"{second}", style=discord.ButtonStyle.blurple)

                async def button_callback1(interaction):
                    if interaction.user == self.ctx.author:
                        if button1.label == reference.correct_answer:
                            await reference.result(True)
                        else:
                            await reference.result(False)
                            button1.style = discord.ButtonStyle.red
                        if len(allAnswers) == 2:
                            await self.formatButtons(button1, button2)
                        elif len(allAnswers) == 3:
                            await self.formatButtons(button1, button2, button3)
                        elif len(allAnswers) == 4:
                            await self.formatButtons(button1, button2, button3, button4)

                async def button_callback2(interaction):
                    if interaction.user == self.ctx.author:
                        if button2.label == reference.correct_answer:
                            await reference.result(True)
                        else:
                            await reference.result(False)
                            button2.style = discord.ButtonStyle.red
                        if len(allAnswers) == 2:
                            await self.formatButtons(button1, button2)
                        elif len(allAnswers) == 3:
                            await self.formatButtons(button1, button2, button3)
                        elif len(allAnswers) == 4:
                            await self.formatButtons(button1, button2, button3, button4)

                button1.callback = button_callback1
                button2.callback = button_callback2
                view.add_item(button1)
                view.add_item(button2)
            if len(allAnswers) >= 3:
                third = allAnswers[2]
                button3 = Button(label=f"{third}", style=discord.ButtonStyle.blurple)

                async def button_callback3(interaction):
                    if interaction.user == self.ctx.author:
                        if button3.label == reference.correct_answer:
                            await reference.result(True)
                        else:
                            await reference.result(False)
                            button3.style = discord.ButtonStyle.red
                        if len(allAnswers) == 2:
                            await self.formatButtons(button1, button2)
                        elif len(allAnswers) == 3:
                            await self.formatButtons(button1, button2, button3)
                        elif len(allAnswers) == 4:
                            await self.formatButtons(button1, button2, button3, button4)

                button3.callback = button_callback3
                view.add_item(button3)
            if len(allAnswers) >= 4:
                fourth = allAnswers[3]
                button4 = Button(label=f"{fourth}", style=discord.ButtonStyle.blurple)

                async def button_callback4(interaction):
                    if interaction.user == self.ctx.author:
                        if button4.label == reference.correct_answer:
                            await reference.result(True)
                        else:
                            await reference.result(False)
                            button4.style = discord.ButtonStyle.red
                        if len(allAnswers) == 2:
                            await self.formatButtons(button1, button2)
                        elif len(allAnswers) == 3:
                            await self.formatButtons(button1, button2, button3)
                        elif len(allAnswers) == 4:
                            await self.formatButtons(button1, button2, button3, button4)

                button4.callback = button_callback4
                view.add_item(button4)

            await self.message.edit(embed=embed, view=view)