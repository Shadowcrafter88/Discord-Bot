import discord
from botCommands.gambling.economy import Economy
from config import config
from discord.ui import Button, View
import random

class FirstOptionsView(View):
    def __init__(self, reference, ctx, message, bet):
        super().__init__(timeout=90)

        self.reference = reference
        self.ctx = ctx
        self.message = message
        self.bet = bet

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.blurple)
    async def stay_button_callback(self, button, interaction):
        if interaction.user == self.ctx.author:
            # await interaction.response.send_message("Stay")
            await self.reference.blackjackRecursion(stay=True)

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.blurple)
    async def hit_button_callback(self, button, interaction):
        if interaction.user == self.ctx.author:
            #await interaction.response.send_message("Hit")
            await self.reference.blackjackRecursion()

    @discord.ui.button(label="Double", style=discord.ButtonStyle.blurple)
    async def double_button_callback(self, button, interaction):
        if interaction.user == self.ctx.author:
            # await interaction.response.send_message("Double")
            await self.reference.blackjackRecursion(lastTurn=True, doubleBet=True)

    async def on_timeout(self) -> None:
        if self.reference.end == False:
            embed = discord.Embed(title=f"{self.ctx.author.display_name} timed out!", description=f"You lost: {self.bet}", color=config.ERROR_EMBED_COLOR)
            await self.message.edit(embed=embed, view=None)

            profit = 0 - int(self.bet)
            Economy.ocAddCredits(self, self.ctx.author.id, profit)
        return await super().on_timeout()

class NextOptionsView(View):
    def __init__(self, reference, ctx, message, bet):
        super().__init__(timeout=90)

        self.reference = reference
        self.ctx = ctx
        self.message = message
        self.bet = bet

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.blurple)
    async def stay_button_callback(self, button, interaction):
        if interaction.user == self.ctx.author:
            # await interaction.response.send_message("Stay")
            await self.reference.blackjackRecursion(stay=True)

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.blurple)
    async def hit_button_callback(self, button, interaction):
        if interaction.user == self.ctx.author:
            #await interaction.response.send_message("Hit")
            await self.reference.blackjackRecursion()

    @discord.ui.button(label="Double", style=discord.ButtonStyle.blurple, disabled=True)
    async def double_button_callback(self, button, interaction):
        await interaction.response.send_message("")

    async def on_timeout(self) -> None:
        if self.reference.end == False:
            embed = discord.Embed(title=f"{self.ctx.author.display_name} timed out!", description=f"You lost: {self.bet}", color=config.ERROR_EMBED_COLOR)
            await self.message.edit(embed=embed, view=None)

            profit = 0 - self.bet
            Economy.ocAddCredits(self, self.ctx.author.id, profit)
        return await super().on_timeout()

class LastView(View):
    def __init__(self, reference, ctx, message, bet):
        super().__init__(timeout=90)

        self.reference = reference
        self.ctx = ctx
        self.message = message
        self.bet = bet

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.blurple, disabled=True)
    async def last_stay_button_callback(self, button, interaction):
        await interaction.response.send_message("")

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.blurple)
    async def last_hit_button_callback(self, button, interaction):
        if interaction.user == self.ctx.author:
            #await interaction.response.send_message("Hit")
            await self.reference.blackjackRecursion(stay=True, end=True)

    @discord.ui.button(label="Double", style=discord.ButtonStyle.blurple, disabled=True)
    async def last_double_button_callback(self, button, interaction):
        await interaction.response.send_message("")

    async def on_timeout(self) -> None:
        if self.reference.end == False:
            embed = discord.Embed(title=f"{self.ctx.author.display_name} timed out!", description=f"You lost: {self.bet}", color=config.ERROR_EMBED_COLOR)
            await self.message.edit(embed=embed, view=None)

            profit = 0 - self.bet
            Economy.ocAddCredits(self, self.ctx.author.id, profit)
        return await super().on_timeout()

class BlackjackClass:
    def __init__(self, bet, credits, ctx, message):
        self.bet = bet
        self.credits = credits

        self.ctx = ctx
        self.message = message

        self.myCards = []
        self.myTypes = []
        self.dealerCards = []
        self.dealerTypes = []

        self.drawCard(my=True)
        self.drawCard(my=False)

        self.end = False
        self.round = 0
        self.lastTurn = False


    def getCardArray(self, cards, types):
        cardList = ""
        symbolArray = [":diamonds:", ":spades:", ":clubs:", ":hearts:"]
        i = 0
        for card in cards:
            if i == len(cards) - 1:
                cardList += f"{card} {symbolArray[types[i]]}"
            else:
                cardList += f"{card} {symbolArray[types[i]]}, "
            i += 1

        return cardList

    def drawCard(self, my=False):
        pointArray = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        symbolArray = [0, 1, 2, 3]
        if my == True:
            self.myCards.append(random.choice(pointArray))
            self.myTypes.append(random.choice(symbolArray))
        else:
            self.dealerCards.append(random.choice(pointArray))
            self.dealerTypes.append(random.choice(symbolArray))

    async def resultManager(self, won, draw=False, multiplier=1.0):
        mySum = self.sumCards(True)
        dealerSum = self.sumCards(False)

        if won == True:
            profit = round(self.bet * multiplier)
            embed = discord.Embed(title=f"{self.ctx.author.display_name} won!", description="Blackjack",
                                  color=0x000000)
        else:
            if draw == True:
                profit = 0
                embed = discord.Embed(title=f"{self.ctx.author.display_name} draw!", description="Blackjack",
                                      color=config.EMBED_COLOR)
            else:
                profit = 0 - int(self.bet)
                embed = discord.Embed(title=f"{self.ctx.author.display_name} lost!", description="Blackjack",
                                      color=0xff0000)
        self.credits += profit
        embed.add_field(name=f"{self.ctx.author.name}'s Hand", value=f"{self.getCardArray(self.myCards, self.myTypes)}\nTotal: **{mySum}**",
                        inline=True)
        embed.add_field(name="Dealers Hand", value=f"{self.getCardArray(self.dealerCards, self.dealerTypes)}\nTotal: **{dealerSum}**",
                        inline=True)
        embed.set_footer(text=f"Played by {self.ctx.author.name} {self.ctx.author.id}",
                         icon_url=f"{self.ctx.author.display_avatar.url}")

        embed.add_field(name="Profit", value=f"**{profit}** credits", inline=False)
        embed.add_field(name="Your Credits", value=f"{self.credits}", inline=True)

        await self.message.edit(embed=embed, view=None)
        self.end = True
        Economy.ocAddCredits(self, self.ctx.author.id, profit)

    def sumCards(self, my=False):
        sum = 0
        ace = 0
        if my == True:
            for card in self.myCards:
                try:
                    sum += int(card)
                except Exception as e:
                    if (card == 'J') or (card == 'Q') or (card == 'K'):
                        sum += 10
                    elif card == 'A':
                        ace += 1
        else:
            for card in self.dealerCards:
                try:
                    sum += int(card)
                except Exception as e:
                    if (card == 'J') or (card == 'Q') or (card == 'K'):
                        sum += 10
                    elif card == 'A':
                        ace += 1
        while ace > 0:
            if (sum + 11 + (ace - 1)) <= 21:
                sum += 11
            else:
                sum += 1
            ace -= 1
        return sum

    async def blackjackRecursion(self, stay=False, lastTurn=False, doubleBet=False, end=False):
        self.round += 1

        if doubleBet == True:
            self.bet *= 2

        mySum = self.sumCards(True)
        dealerSum = self.sumCards(False)

        if (stay == False) or (lastTurn == True):
            # Todo System that gives you the Cards
            if lastTurn == False:
                self.drawCard(my=True)

                mySum = self.sumCards(True)
                dealerSum = self.sumCards(False)

                if mySum == 21:
                    if self.round == 1:
                        await self.resultManager(True, multiplier=1.5)
                        return True
                    else:
                        await self.resultManager(True)
                        return True
                if mySum >= 21:
                    await self.resultManager(False)
                    return False

            embed = discord.Embed(title=f"{self.ctx.author.display_name}", description="Blackjack", color=config.EMBED_COLOR)
            embed.add_field(name="Your Hand", value=f"{self.getCardArray(self.myCards, self.myTypes)}\nTotal: **{mySum}**",
                            inline=True)
            embed.add_field(name="Dealers Hand",
                            value=f"{self.getCardArray(self.dealerCards, self.dealerTypes)}\nTotal: **{dealerSum}**",
                            inline=True)
            embed.set_footer(text=f"{self.ctx.author.name} You have 90 sec",
                             icon_url=f"{self.ctx.author.display_avatar.url}")

            reference = self
            if lastTurn == False:
                if self.round > 1:
                    view = NextOptionsView(reference, self.ctx, self.message, self.bet)
                else:
                    view = FirstOptionsView(reference, self.ctx, self.message, self.bet)
            else:
                view = LastView(reference, self.ctx, self.message, self.bet)

            await self.message.edit(embed=embed, view=view)

        else:
            if end == True:
                self.drawCard(my=True)
                mySum = self.sumCards(True)
                if mySum > 21:
                    await self.resultManager(False)
                    return False

            while dealerSum <= 16:
                self.drawCard(my=False)
                dealerSum = self.sumCards(False)

            if (mySum < dealerSum) and (dealerSum < 21):
                await self.resultManager(False)
                return False
            elif dealerSum < mySum and (mySum < 21):
                await self.resultManager(True)
                return True
            elif dealerSum == mySum:
                await self.resultManager(False, True)
                return False
            elif (mySum < 21) and (dealerSum > 21):
                await self.resultManager(True)
                return True
            elif (dealerSum < 21) and (mySum > 21):
                await self.resultManager(True)
                return False
            elif dealerSum == 21:
                await self.resultManager(False)
                return False
            elif mySum == 21:
                await self.resultManager(True)
                return True
            else:
                await self.resultManager(False, True)
                return False



