import sqlite3
import discord
from config import config

class Economy:
    def __init__(self):
        self.openDB()

    def createDB(self):
        self.db = sqlite3.connect("config/databases/users.db")
        self.c = self.db.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS users (
                            id integer, 
                            credits integer,
                            last_daily integer
                        )""")
        self.db.commit()
        self.db.close()

    def setStartingCredits(self, id):
        self.c.execute(f"INSERT INTO users VALUES ({id}, {config.STARTING_MONEY}, {0})")

    def setCredits(self, id, credits):
        self.c.execute(f"UPDATE users SET credits = {credits} WHERE id = {id}")

    def openDB(self):
        self.db = sqlite3.connect("config/databases/users.db")
        self.c = self.db.cursor()

    def ocAddCredits(self, id, profit):
        self.db = sqlite3.connect("config/databases/users.db")
        self.c = self.db.cursor()
        self.c.execute(f"SELECT * FROM users WHERE id = {id}")
        selected = self.c.fetchone()
        credits = selected[1] + profit
        self.c.execute(f"UPDATE users SET credits = {credits} WHERE id = {id}")
        self.db.commit()
        self.db.close()
        return int(credits)

    def ocGetCredits(self, id):
        self.db = sqlite3.connect("config/databases/users.db")
        self.c = self.db.cursor()
        self.c.execute(f"SELECT * FROM users WHERE id = {id}")
        selected = self.c.fetchone()
        self.db.commit()
        self.db.close()
        return int(selected[1])

    def closeDB(self):
        self.db.commit()
        self.db.close()

    def getFromId(self, id):
        try:
            self.c.execute(f"SELECT * FROM users WHERE id = {id}")
            selected = self.c.fetchone()
            return selected
        except Exception as e:
            print(e)
            return False

    def sendNotEnoughCredits(self, betAmount: int, credits):
        embed = discord.Embed(title="You don't have enough credits!", color=config.ERROR_EMBED_COLOR)
        embed.add_field(name="Your credits:", value=f"{credits}", inline=False)
        embed.add_field(name="Your bet:", value=f"{betAmount}", inline=False)
        return embed

    def sendNotRegistred(self, you = True):
        if you:
            embed = discord.Embed(title=f"You are not registred!",
                                  description=f"Do `{config.BOT_PREFIX}register` to do so.",
                                  color=config.ERROR_EMBED_COLOR)
        else:
            embed = discord.Embed(title=f"This user is not registred!",
                                  color=config.ERROR_EMBED_COLOR)
        return embed


