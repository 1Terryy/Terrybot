import random
import datetime
import time
import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
import os
import praw
import asyncio


class reddit(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.all_subs = []
		self.reddit = praw.Reddit(client_id="GuC_cDVmLSzwGg",
                 client_secret="EWrUwwrIupBG30FZsoguHXiRTvrTmQ", 
                 redirect_uri="https://localhost-8080",
                 user_agent='sdaa')

	@commands.command(aliases=['meme'])
	async def memes(self, ctx):

		random_sub = random.choice([i for i in self.reddit.subreddit('memes').hot(limit=200)])

		name = random_sub.title
		url = random_sub.url
		comments = random_sub.comments
		upvote = random_sub.upvote_ratio
		up = random_sub.score
		author = random_sub.author
		sub = random_sub.subreddit

		embed = discord.Embed(
			title= name,
			color=discord.colour.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
		)
		embed.description='Submission [URL]({}).'.format(random_sub.url)
		embed.set_author(name=f'Posted by {author} from r/{sub}')
		embed.set_image(url=url)
		embed.set_footer(text=f'\t💬 {len(comments)}	⇅ {upvote}	↑ {up}')
		await ctx.send(embed=embed)
		
	@commands.command(aliases=['breakingbad'])
	async def bb(self, ctx):
		subreddit = self.reddit.subreddit('breakingbad')
		top = subreddit.hot(limit=200)
		allsubs = []
		for sub in top:
			allsubs.append(sub)
		random_sub = random.choice(allsubs)
		
		if random_sub.subreddit.over18 == True:
			await ctx.send('Please navigate to a NSFW channel to use this. Most likey due to a meme containing 18+ content.')
			return
		
		name = random_sub.title
		url = random_sub.url
		comments = random_sub.comments
		upvote = random_sub.upvote_ratio
		up = random_sub.score
		author = random_sub.author
		sub = random_sub.subreddit

		embed = discord.Embed(
			title= name,
			color=discord.colour.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
		)
		embed.set_author(name=f'Posted by {author} from r/{sub}')
		embed.set_image(url=url)
		embed.set_footer(text=f'\t💬 {len(comments)}	⇅ {upvote}	↑ {up}')
		await ctx.send(embed=embed)

	@commands.command(aliases=['to'])
	async def theoffice(self, ctx):
		subreddit = self.reddit.subreddit('DunderMifflin')
		top = subreddit.hot(limit=200)
		allsubs = []
		for sub in top:
			allsubs.append(sub)
		random_sub = random.choice(allsubs)
		
		if random_sub.subreddit.over18 == True:
			await ctx.send('Please navigate to a NSFW channel to use this. Most likey due to a meme containing 18+ content.')
			return
		
		name = random_sub.title
		url = random_sub.url
		comments = random_sub.comments
		upvote = random_sub.upvote_ratio
		up = random_sub.score
		author = random_sub.author
		sub = random_sub.subreddit

		embed = discord.Embed(
			title= name,
			color=discord.colour.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
		)
		embed.set_author(name=f'Posted by {author} from r/{sub}')
		embed.set_image(url=url)
		embed.set_footer(text=f'\t💬 {len(comments)}	⇅ {upvote}	↑ {up}')
		await ctx.send(embed=embed)

	@commands.command(aliases=['ksi'])
	async def ksireddit(self, ctx):
		subreddit = self.reddit.subreddit('ksi')
		top = subreddit.hot(limit=200)
		allsubs = []
		for sub in top:
			allsubs.append(sub)
		random_sub = random.choice(allsubs)
		
		if random_sub.subreddit.over18 == True:
			await ctx.send('Please navigate to a NSFW channel to use this. Most likey due to a meme containing 18+ content.')
			return
		
		name = random_sub.title
		url = random_sub.url
		comments = random_sub.comments
		upvote = random_sub.upvote_ratio
		up = random_sub.score
		author = random_sub.author
		sub = random_sub.subreddit

		embed = discord.Embed(
			title= name,
			color=discord.colour.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
		)
		embed.set_author(name=f'Posted by {author} from r/{sub}')
		embed.set_image(url=url)
		embed.set_footer(text=f'\t💬 {len(comments)}	⇅ {upvote}	↑ {up}')
		await ctx.send(embed=embed)

	@commands.command()
	async def REDDIT(self, ctx, subname=None):
		if subname == None:
			await ctx.send('Give a subreddit name!')
			return
		global msg
		subreddit = self.reddit.subreddit('{}'.format(subname))
		if subreddit.over18 == True:
			msg = await ctx.send('Over 18 Content Detected!')
			if ctx.channel.is_nsfw() == True:
				all_subs = []
				top = subreddit.hot(limit=200)

				for submission in top:
					all_subs.append(submission)

				random_sub = random.choice(all_subs)

				name = random_sub.title
				url = random_sub.url
				comments = random_sub.comments
				upvote = random_sub.upvote_ratio
				up = random_sub.score
				author = random_sub.author
				sub = random_sub.subreddit

				embed = discord.Embed(
					title= name,
					color=discord.colour.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
				)
				embed.set_author(name=f'Posted by {author} from r/{sub}')
				embed.set_image(url=url)
				embed.set_footer(text=f'\t💬 {len(comments)}	⇅ {upvote}	↑ {up}')
				await ctx.send(embed=embed)
			else:
				embed = discord.Embed(
					title='❌ Error ❌',
					color=discord.Color.dark_red()
				)
				embed.set_thumbnail(url='https://rlv.zcache.com/return_to_sender_wrong_address_rubber_stamp-rabe45bc54d524b0ca9b150ee9d222490_6o1xx_540.jpg?rlvnet=1')
				embed.add_field(name='NOPE', value='This command must be used in a `NSFW` channel since this command is explicit!')
				await ctx.send(embed=embed)
		else:
			all_subs = []
			top = subreddit.hot(limit=50)

			for submission in top:
				all_subs.append(submission)

			random_sub = random.choice(all_subs)

			name = random_sub.title
			url = random_sub.url
			comments = random_sub.comments
			upvote = random_sub.upvote_ratio
			up = random_sub.score
			author = random_sub.author
			sub = random_sub.subreddit

			embed = discord.Embed(
				title= name,
				color=discord.colour.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
			)
			embed.set_author(name=f'Posted by {author} from r/{sub}')
			embed.set_image(url=url)
			embed.set_footer(text=f'\t💬 {len(comments)}	⇅ {upvote}	↑ {up}')
			await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(reddit(bot))