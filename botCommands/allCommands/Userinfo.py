import discord
from discord.ext import commands
import pytz
from datetime import datetime
from config import config
import logging


class Userinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='userinfo')
    async def userinfo(self, ctx, member: discord.Member = None):
        try:
            if member is None:
                member = ctx.author

            date_format = "%a, %d %b %Y %I:%M %p"
            members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
            perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in member.guild_permissions if p[1]])

            embed = discord.Embed(color=member.color, description=member.mention)
            embed.set_author(name=str(member), icon_url=member.avatar.url)
            embed.set_thumbnail(url=member.avatar.url)

            embed.add_field(name="Joined", value=member.joined_at.strftime(date_format), inline=True)
            #embed.add_field(name="Join position", value=str(members.index(member) + 1))
            embed.add_field(name="Registered", value=member.created_at.strftime(date_format), inline=True)
            if len(member.roles) > 1:
                role_string = ' '.join([r.mention for r in member.roles][1:])
                embed.add_field(name=f"Roles [{len(member.roles) - 1}]", value=role_string, inline=False)
            embed.add_field(name="Guild permissions", value=perm_string, inline=False)
            embed.add_field(name='Booster', value=f'{"Yes" if member.premium_since else "No"}', inline=False)
            embed.set_footer(text='ID: ' + str(member.id))
            await ctx.send(embed=embed)

        except Exception as e:
            print(e)
            logging.exception("message")


def setup(bot):
    bot.add_cog(Userinfo(bot))