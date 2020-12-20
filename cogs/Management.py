import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
import json
import os

cogsx = ['checks', 'fun', 'games', 'image', 'moderation', 'motivation', 'nsfw', 'reddit']
cogsy = ['Checks', 'Fun', 'Games', 'Image', 'Moderation', 'Motivation', 'NSFW', 'Reddit']
description = {
    'Checks' : 'Holds the commands such as Whois, Server, Avatar.',
    'Fun' : 'Holds all the commands found in the Fun Category.',
    'Games' : 'Holds all the commads found in the Games Category',
    'Image' : 'Holds all the Image Manipulation commands.',
    'Moderation' : 'Holds most commands in the Moderation Category.',
    'Motivation' : 'Holds all the commands in the Motivation Category.',
    'NSFW' : 'Holds all the commands in the NSFW category.',
    'Reddit' : 'Holds the Breaking Bad, Memes and Reddit commands.'
}

disabled_cogs = []

class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.disabled = ['remove', 'allow', 'help', 'prefix', 'change_prefix', 'cp', 'suggest', 'report', 'stats', 'uptime', 'refresh', 'sync', 'enable', 'disable']

    @commands.command(aliases=['cp'])
    @commands.has_permissions(administrator = True)
    async def change_prefix(self, ctx, *, prefix=None):
        global x
        try:
            x = list(prefix)
        except TypeError:
            pass
        if prefix == None:
            await ctx.send('You cannot set the prefix as nothing!')
        elif len(list(prefix)) > 20:
            await ctx.send("The server's prefix cannot be bigger than `20` Letters!")
        elif '[' in x[0] and ']' in x[-1]:
            x = list(prefix)
            x.pop(0)
            x.pop(-1)
            with open('prefixes.json', 'r') as f:
                prefixes = json.load(f)

            try:
                if ' ' not in x:
                    pass
                else:
                    x = x.split(" ")
                x = ''.join(map(str, x))
                x = x.split(',')
                x = ''.join(map(str, x))
                x = x.split("'")
                x = ''.join(map(str, x))
                prefixes[str(ctx.guild.id)] = x

                with open('prefixes.json', 'w') as f:
                    json.dump(prefixes, f, indent=4)
                await ctx.send('The new prefix for Prim+ is **`{}`**'.format(prefix))
            except Exception:
                await ctx.send('You gave an invalid list!')
        else:
            with open('prefixes.json', 'r') as f:
                prefixes = json.load(f)

            prefixes[str(ctx.guild.id)] = prefix

            with open('prefixes.json', 'w') as f:
                json.dump(prefixes, f, indent=4)
            await ctx.send('The new prefix for Prim+ is **`{}`**'.format(prefix))

    @commands.command()
    async def prefix(self, ctx):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefix = prefixes[str(ctx.guild.id)]
        await ctx.send('The prefix for the server **`{}`** is **`{}`**'.format(ctx.guild.name, prefix))

    @commands.command(aliases=['sw', 'set_wel', 'set_w'])
    async def set_welcome(self, ctx, channel : discord.TextChannel=None):
        if channel == None:
            await ctx.send('You havent provided a valid channel!')
        else:
            with open('welcome.json', 'r') as f:
                welcome_id = json.load(f)
            welcome_id[str(ctx.guild.id)] = f'{channel.id}'
            with open('welcome.json', 'w') as f:
                json.dump(welcome_id, f, indent=4)
            await ctx.send(f'The welcomes channel has been set as `{channel.name}`.')

    @commands.command(aliases=['rw', 'remove_w', 'r_welcome'])
    async def remove_welcome(self, ctx):
        with open('welcome.json', 'r') as f:
            welcome_id = json.load(f)
        welcome_id[str(ctx.guild.id)] = f'Not Set'
        with open('welcome.json', 'w') as f:
            json.dump(welcome_id, f, indent=4)
        await ctx.send(f'You have removed the welcome messages!')


    @commands.command()
    @commands.cooldown(1, 50000, BucketType.user)
    async def suggest(self, ctx, *args):
        if args == []:
            await ctx.send('Please give me a suggestion. This has been flagged.')
            return
        if ctx.author.id == 300074149878038539:
            await ctx.send('You have been banned from sending requests!')
        elif ctx.author.id == 708548079196045363:
            await ctx.send('You have been banned from sending requests!')
        else:
            channel = self.bot.get_channel(753704717254918214)
            x = ' '.join(map(str, args))
            embed = discord.Embed(
                title=f"{ctx.author}'s Suggestion!",
                color=discord.Color.red(),
                description=f'The user **`{ctx.author}`** is from **`{ctx.guild}`**.'
            )
            embed.add_field(name=f'Description!', value=f'{x}')
            embed.set_footer(text=f'User ID: {ctx.author.id}\nGuild ID: {ctx.guild.id}')
            msg = await channel.send(embed=embed)
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')
            await ctx.send('You suggestion has been sent')

def setup(bot):
    bot.add_cog(Management(bot))
