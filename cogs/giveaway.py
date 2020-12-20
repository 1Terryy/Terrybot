import discord
import time
import asyncio
import random
import datetime
from discord.ext import commands
from utils.util import GetMessage

class giveaways(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="/giveaway [mins] [prize], a very simple giveaway command")
    async def giveaway(self, ctx, mins: int, *, prize: str):
        embed = discord.Embed(title=f"{prize}", description=f"**Hosted by:** {ctx.author.mention}", color=0x4994FF)
        embed.add_field(name=" ", value=f"react with the 🎉 to participate")
        embed.set_footer(text=f"Ends in {mins} minutes!")
        await ctx.send("🎉**__Giveaway__**🎉")
        my_msg = await ctx.send(embed=embed)
        await my_msg.add_reaction("🎉")
        await asyncio.sleep(mins*60)
        new_msg = await ctx.channel.fetch_message(my_msg.id)
        people = await new_msg.reactions[0].users().flatten()
        people.pop(people.index(ctx.guild.me))
        winner = random.choice(people)
        await ctx.send(f"🥳 **Congratulations!** {winner.mention} won **{prize}**.")


    @commands.command()
    async def reroll(self, ctx):

        new_msg = await ctx.channel.fetch_message(769945256980250654)
        people = await new_msg.reactions[0].users().flatten()
        people.pop(people.index(ctx.guild.me))
        winner = random.choice(people)
        await ctx.send(f"🥳 **Congratulations!** {winner.mention} won **$5 Discord Nitro**.")


def setup(bot):
    bot.add_cog(giveaways(bot))