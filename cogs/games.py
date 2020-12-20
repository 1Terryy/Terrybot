import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import datetime
import random
import requests
import asyncio
import time
import os
import math

class games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Latency'])
    async def ping(self, ctx):
        msg = await ctx.send("`Bot Latency...`")
        times = []
        counter = 0
        embed = discord.Embed(title="More Information:", description="4 pings have been made and here are the results:", colour=random.randint(0x000000, 0xFFFFFF))
        for _ in range(3):
            counter += 1
            start = time.perf_counter()
            await msg.edit(content=f"Trying Ping... {counter}/3")
            end = time.perf_counter()
            speed = round((end - start) * 1000)
            times.append(speed)
            if speed < 160:
                embed.add_field(name=f"Ping {counter}:", value=f"🟢 | {speed}ms", inline=True)
            elif speed > 170:
                embed.add_field(name=f"Ping {counter}:", value=f"🟡 | {speed}ms", inline=True)
            else:
                embed.add_field(name=f"Ping {counter}:", value=f"🔴 | {speed}ms", inline=True)
        embed.set_author(name="🏓    PONG    🏓", icon_url="https://img.icons8.com/ultraviolet/40/000000/table-tennis.png")
        embed.add_field(name="Bot Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Normal Speed", value=f"{round((round(sum(times)) + round(self.bot.latency * 1000))/4)}ms")
        embed.set_footer(text=f"Total estimated elapsed time: {round(sum(times))}ms")
        await msg.edit(content=f":ping_pong: **{round((round(sum(times)) + round(self.bot.latency * 1000))/4)}ms**", embed=embed)

    @commands.command(aliases=['Penis', 'pp'])
    async def PP(self, ctx, user : discord.Member=None):
        if user == None:
            user = ctx.author
        else:
            pass
        pen = ['Inside out dick',
               '8D',
               '8=D',
               '8==D',
               '8===D',
               '8====D',
               '8=====D',
               '8======D',
               '8=======D',
               '8========D',
               '8=========D',
               '8==========D',
               '8===========D',
               '8============D',
               '8=============D',
               '8==============D',
               '8=================================D']
        e = discord.Embed(title="", colour=random.randint(0x000000, 0xFFFFFF), description="__**Prim+:**__", color=0x50C878)
        e.add_field(name='**PP machine 4356**',
                    value=f'{user.display_name} penis is:\n{random.choice(pen)}\n**Even my angel has a bigger one**', )
        await ctx.send(embed=e)

    @commands.command(aliases=['slots', 'bet'])
    async def slot(self, ctx):
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} : {b} : {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} Has gotten 3 out of 3, HE WINS!!! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 out of 3, HE WINS!!! 🎉")
        else:
            await ctx.send(f"{slotmachine} 0 out of 3, He looses 😢")

    @commands.command(aliases=['rps', 'rockpaperscissors'])
    async def RPS(self, ctx, choice=None):
        if choice == None:
            embed=discord.Embed(
                title='You gotta give a choice!',
                colour=random.randint(0x000000, 0xFFFFFF),
                description=f'{ctx.author.mention} you never gave a valid choice. the choice you gave was {choice}. The valid options are:\n`rock` `paper` `scissor`'
            )
            await ctx.send(embed=embed)
        else:
            x = choice.lower()
            option = ['rock', 'paper', 'scissor']
            op = random.choice(option)
            if x == 'rock':
                if op == 'rock':
                    await ctx.send(f'{ctx.author.name}: {choice}\nPrim+: rock\n\nWe both got rock! So its a tie. Good Game {ctx.author.name}!!!')
                elif op == 'paper':
                    await ctx.send(f'{ctx.author.name}: {choice}\nPrim+: paper\n\nYou chose paper. Paper wraps rock. So i win!')
                elif op == 'scissor':
                    await ctx.send(f'{ctx.author.name}: {choice}\nPrim+: scissors\n\nYou Won!!! Rock beats scissors. Good Game {ctx.author.name}!!!')
            elif x == 'scissor':
                if op == 'rock':
                    await ctx.send(f'{ctx.author.name}: {choice}\nPrim+: rock\n\nRock smashes scissors. You loose haha!')
                elif op == 'paper':
                    await ctx.send(f'{ctx.author.name}: {choice}\nPrim+: paper\n\nYou Win! Scissors cut paper. So you win {ctx.author}')
                elif op == 'scissor':
                    await ctx.send(f'{ctx.author.name}: {choice}\nPrim+: scissors\n\nIts a tie. Good Game {ctx.author.name}!!!')
            elif x == 'paper':
                if op == 'rock':
                    await ctx.send(f'{ctx.author.name}: {choice}\nPrim+: rock\n\nYou win as paper wraps rock!!!')
                elif op == 'paper':
                    await ctx.send(f'{ctx.author.name}: {choice}\nPrim+: paper\n\nIts a tie. We bot picked paper!')
                elif op == 'scissor':
                    await ctx.send(f'{ctx.author.name}: {choice}\Prim+: scissor\n\nYou Loose! Scissors cut paper.')
            else:
                embed=discord.Embed(
                    title='You gotta give a choice!',
                    colour=random.randint(0x000000, 0xFFFFFF),
                    description=f'{ctx.author.mention} you never gave a valid choice. the choice you gave was {choice}. The valid options are:\n`rock` `paper` `scissor`'
                )
                await ctx.send(embed=embed)

    @commands.command()
    async def flip(self, ctx, user_choice : str=None):
        choices = ('heads', 'head', 'tails', 'tail')
        if user_choice == None or user_choice.lower() not in choices:
            await ctx.send('Give a valid choice of **Heads** or **Tails**')
            return
        bot_choice = random.choice(choices)
        embed = discord.Embed(
                title='Heads and Tails',
                colour=random.randint(0x000000, 0xFFFFFF)
            )
        embed.add_field(name='{}'.format(ctx.author), value=user_choice)
        embed.add_field(name='{}'.format(self.bot.user), value=bot_choice)
        if user_choice.lower() == bot_choice or user_choice.lower() == bot_choice + 's':
            embed.description = 'You WIN!'
        else:
            embed.description = 'You lost.'
        await ctx.send(embed=embed)        
            
def setup(bot):
    bot.add_cog(games(bot))