import discord
from discord.ext import commands
from discord.ext.commands import BucketType
import asyncio
import shutil
import sys
from discord.utils import get
import random
import requests
import time
import sys
import math
from datetime import *
from discord.ext.commands import command
import ssl
import json
import os
from dateutil.tz import gettz
from datetime import date
from datetime import time
from datetime import datetime
from datetime import datetime, timedelta
from random import choice
from discord import Embed
import youtube_dl
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions
import typing as t
import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN
)

TOKEN = 'NzQxODEyNzY4MzYwODkwNDgx.Xy9A-g.KeTpgl8rpuvPhIi_Xkv7y7ppJhs'

def get_prefix(client, message):

	with open("prefixes.json", "r") as f:
		prefixes = json.load(f)

	return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)
client.remove_command('help')

		   
@client.event
async def on_guild_join(guild):
	with open("prefixes.json", "r") as f:
		prefixes = json.load(f)

	prefixes[str(guild.id)] = ","

	with open('prefixes.json', 'w') as f:
		json.dump(prefixes,f)

async def is_owner(ctx):
	return ctx.author.id in [429611688992702476]

@client.event
async def on_ready():
	print("The bot is running!")
	totalserv = str(len(client.guilds))
	await client.change_presence(activity=discord.Donot(name=f",help | Helping {totalserv} servers!", url="https://twitch.tv/denaticc"))

async def get_bank_data():
	with open("mainbank.json", "r") as f:
		users = json.load(f)

	return users

async def open_account(user):

	users = await get_bank_data()

	with open("mainbank.json", "r") as f:
		users = json.load(f)

	if str(user.id) in users:
		return False
	else:
		users[str(user.id)]["wallet"] = 0
		users[str(user.id)]["bank"] = 0

	with open("mainbank.json", "w") as f:
		json.dump(users,f)
	return True

@client.command()
@commands.check(is_owner)
async def load(ctx, ext:str=None):
	if ext == None:
		for filename in os.listdir('\cogs'):
			if filename.endswith('.py'):
				client.load_extension(f'cogs.{filename[:-3]}')
		await ctx.send("All extensions have been loaded")
		print("All extensions have been loaded")
	else:
		ext = ext.lower()
		client.load_extension(f'cogs.{ext}')
		await ctx.send(f"The extension `{ext}` have been loaded")
		
@client.command()
@commands.check(is_owner)
async def unload(ctx, ext:str=None):
	if ext == None:
		for filename in os.listdir('\cogs'):
			if filename.endswith('.py'):
				client.unload_extension(f'cogs.{filename[:-3]}')
		await ctx.send("All extensions have been unloaded")
		print("All extensions have been unloaded")
	else:
		ext = ext.lower()
		client.unload_extension(f'cogs.{ext}')
		await ctx.send(f"The extension `{ext}` have been unloaded")
		print(f"The extension `{ext}` have been unloaded")

@client.command()
@commands.check(is_owner)
async def reload(ctx, ext:str=None):
	if ext == None:
		for filename in os.listdir('\cogs'):
			if filename.endswith('.py'):
				client.reload_extension(f'cogs.{filename[:-3]}')
		await ctx.send("All extensions have been reloaded")
		print("All extensions have been reloaded")
	else:
		ext = ext.lower()
		client.reload_extension(f'cogs.{ext}')
		await ctx.send(f"The extension `{ext}` have been reloaded")
		print(f"The extension `{ext}` have been reloaded")

@client.command()
@commands.check(is_owner)
async def logout(ctx):
	await ctx.send('```Shutting down...```')
	print("Shutting down...")
	await client.logout()

@client.command(pass_context=True)
async def add(ctx, a: int, b:int):
	await ctx.send(a+b)
	
@client.command(pass_context=True)
async def minus(ctx, a: int, b:int):
	await ctx.send(a-b)

@client.command(pass_context=True)
async def multiply(ctx, a: int, b:int):
	await ctx.send(a*b)
	
@client.command(pass_context=True)
async def divide(ctx, a: int, b:int):
	await ctx.send(a/b)

@client.command()
async def guilds(ctx):
	await ctx.send(client.guilds)

@client.command()
async def google(ctx, *, arg):
	api_token = "API"
	url = f'http://newsapi.org/v2/everything?q={arg}&apiKey={api_token}'

	response = requests.get(url)

	if response.json()['status'] == 'ok' and response.json()['totalResults'] > 0:
		articlesTotal = response.json()['totalResults']
		if articlesTotal > 20:
			articlesTotal = 20
		articleId = random.randrange(articlesTotal)
		articleTitle = response.json()['articles'][articleId]["title"]
		articleUrl = response.json()['articles'][articleId]["url"]
		test_e = discord.Embed(colour = 0x33b4cc, title = f"Searching for {arg}...", description = f"{articlesTotal} things found!\nSelected searcg no: {articleId}\n\n[**{articleTitle}**]({articleUrl})")
	else:
		test_e = discord.Embed(colour = 0x33b4cc, description = f"**No search results :(**\n\nSearch for {arg}\nreturned no results.")
	await ctx.send(embed = test_e)

@client.command()
async def news(ctx):
	api_token = "API"
	url = f'https://newsapi.org/v2/top-headlines?country=gb&category=business&apiKey={api_token}'

	response = requests.get(url)

	if response.json()['status'] == 'ok' and response.json()['totalResults'] > 0:
		articlesTotal = response.json()['totalResults']
		if articlesTotal > 20:
			articlesTotal = 20
		articleId = random.randrange(articlesTotal)
		articleTitle = response.json()['articles'][articleId]["title"]
		articleUrl = response.json()['articles'][articleId]["url"]
		test_e = discord.Embed(colour = 0x33b4cc, title = f"News", description = f"{articlesTotal} articles found!\nSelected article no: {articleId}\n\n[**{articleTitle}**]({articleUrl})")
	else:
		test_e = discord.Embed(colour = 0x33b4cc, description = f"**No news for you :(**\n\nQuery for '**arg**'\nreturned no results.")
	await ctx.send(embed = test_e)

@client.command(aliases=["dev"])
async def developer(ctx):
	await ctx.send("The developer of this bot is 1Terry#9999")

@client.command()
async def sms(ctx, user: discord.Member, *, arg):

	await user.send(f"{ctx.author} sent you a SMS saying: {arg}")
	await ctx.send("Message successfully sent sir!")

@client.command()
async def embed(ctx):
	await ctx.send("what do you want the title to be")

	def check(x):
		return x.author == ctx.author

	msg1 = await client.wait_for('message', check=check, timeout=30)

	await ctx.send("what do you want the desc to be")

	def check(z):
		return z.author == ctx.author

	msg2 = await client.wait_for('message', check=check, timeout=30)

	await ctx.send("what do you want the field title to be")

	def check(z):
		return z.author == ctx.author

	msg3 = await client.wait_for('message', check=check, timeout=30)

	await ctx.send("what do you want the desc of the field to be")

	def check(z):
		return z.author == ctx.author

	msg4 = await client.wait_for('message', check=check, timeout=30)

	await ctx.send("what do you want the footer to have?")

	def check(z):
		return z.author == ctx.author

	msg5 = await client.wait_for('message', check=check, timeout=30)

	await ctx.send("what do you want the color to be? just make sure you replace the # of the hex code with a 0x like 0xff0000")
		
	def check(z):
		return z.author == ctx.author

	msg6 = await client.wait_for('message', check=check, timeout=30)
	em = discord.Embed(
		title=msg1.content, 
		description=msg2.content,
		color=int(msg6.content,16)
		)
	em.add_field(name=msg3.content, value=msg4.content)
	em.set_footer(text=msg5.content)
	await ctx.send(embed=em)

@client.command(aliases=['sslowmode','slowmode', 'ssm'])
@commands.has_permissions(view_audit_log=True)
async def setslowmode(ctx,tm):
	t = convert_time_to_seconds(tm)
	await ctx.channel.edit(slowmode_delay=t) 
	if tm.find('h')!=-1 or tm.find('s')!=-1 or tm.find('m')!=-1:
		await ctx.send(f"⌚ Set the slowmode delay in this channel to {tm}!", delete_after=10.5)
		return False
	else:
		await ctx.send(f"⌚ Set the slowmode delay in this channel to {tm}s!", delete_after=10.5)
def convert_time_to_seconds(time):
	time_convert = {"s": 1, "m": 60, "h": 3600}

	try:
		return int(time[:-1]) * time_convert[time[-1]]
	except:
		return time

@client.command(aliases=['resetslowmode', 'rs'])
@commands.has_permissions(view_audit_log=True)
async def rslowmode(ctx):
	await ctx.channel.edit(slowmode_delay=0) 
	await ctx.send(f"⌚ Reset the slowmode delay in this channel!", delete_after=10.5)

@client.command()
async def weather(ctx, city="London"):

	apikey = "API"

	response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}")
	responsetext = response.text

	data = json.loads(responsetext)

	weather = data["weather"][0]["main"]
	description = data["weather"][0]["description"]
	temperature = str(round(float(data["main"]["temp"]) - 273.15)) + "°C"
	cloudpercent = str(data["clouds"]["all"]) + "%"

	test_e = discord.Embed(colour = 0xffa500, title = f"Weather in {city}.", description = f"**Temperature:** {temperature}.\n**Cloud Coverage:** {cloudpercent}\n**The sky:** {description}")
	test_e.set_footer(text = "You can check the weather for cities as well as towns")

	await ctx.send(embed=test_e)

@client.command (pass_context=True)
async def helpa(ctx):
	author = ctx.message.author
	test_e = discord.Embed(colour = 0x33b4cc, title = "Prim+ Command List", description = "We have some really [kick-ass](https://discord.gg/Rqn7Dk4) commands!")

	test_e.add_field(name="📷Image", value=f"`{get_prefix}help image`", inline=True)
	test_e.add_field(name="💰Currency", value=f"`{get_prefix}help currency`", inline=True)
	test_e.add_field(name="🛠️Utility", value=f"`{get_prefix}help utility`", inline=True)
	test_e.add_field(name="😄Fun", value=f'`{get_prefix}help fun`', inline=True)
	test_e.add_field(name="⚔️Moderation", value=f'`{get_prefix}help moderation`', inline=True)
	test_e.add_field(name="🎵Music", value=f'`{get_prefix}help music`', inline=True)
	test_e.set_footer(text = "© Developed by 1Terry#9999")

	await ctx.send(embed=test_e)

@client.command (pass_context=True)
async def vote(ctx):
	author = ctx.message.author
	test_e = discord.Embed(colour = 0x33b4cc, title = "Vote for Prim+", description = "We have some really [kick-ass](https://www.youtube.com/watch?v=dQw4w9WgXcQ) perks for voting!\n\nVote here at [**top.gg**](https://top.gg/bot/741812768360890481/vote)\n")
	test_e.set_footer(text = "Make sure to do the command ',voteclaim' to claim your voting perks.")
	
	await ctx.send(embed=test_e)

@client.command()
async def help(ctx, sect=None):
	if sect == None:
		test_e = discord.Embed(colour = 0x33b4cc, title = "Prim+ Command List", description = "We have some really [kick-ass](https://discord.gg/Rqn7Dk4) commands!")

		test_e.add_field(name="📷Image", value=f"`,help image`", inline=True)
		test_e.add_field(name="💰Currency", value=f"`,help currency`", inline=True)
		test_e.add_field(name="🛠️Utility", value=f"`,help utility`", inline=True)
		test_e.add_field(name="😄Fun", value=f'`,help fun`', inline=True)
		test_e.add_field(name="⚔️Moderation", value=f'`,help moderation`', inline=True)
		test_e.add_field(name="🎵Music", value=f'`,help music`', inline=True)
		test_e.set_footer(text = "© Developed by 1Terry#9999")
		await ctx.send(embed=test_e)
	elif sect == 'utility':
		test_e = discord.Embed(colour = 0x33b4cc, title = "🛠️Utility", description = "\n`invite\nchange_prefix\nsetslowmode\nresetslowmode\nping\nserverinfo\nwhois\nsuggest\nselfharm\nstats`")
		test_e.set_footer(text = f"Make sure to add your prefix before the commands.")
		await ctx.send(embed=test_e)
	elif sect == 'currency':
		test_e = discord.Embed(colour = 0x33b4cc, title = "💰Currency commands", description = "\n`bal\nshop\nbuy\nbag\nsell\nleaderboard\nbeg\ndaily\nsearch\nwithdraw\ndep\ngive\nrob`")
		test_e.set_footer(text = f"Make sure to add your prefix before the commands.")
		await ctx.send(embed=test_e)
	elif sect == 'image':
		test_e = discord.Embed(colour = 0x33b4cc, title = "📷Image commands", description = "\n`slap\nmeme\nksi\nREDDIT\npepesign\ncat\ncancer\nrip\nweird\nclay\ndrawing\nchangemymind\nblackandwhite\nshush\nMore coming soon...`")
		test_e.set_footer(text = f"Make sure to add your prefix before the commands.")
		await ctx.send(embed=test_e)
	elif sect == 'moderation':
		test_e = discord.Embed(colour = 0x33b4cc, title = "⚔️Moderation commands", description = "\n`tempmute\nremoverole\naddrole\nlock\nnuke\nmute\nunmute\nban\nunban\ntempban\nkick\nwarn\nreset_warns\nwarns\ndelwarn\nnewchannel`")
		test_e.set_footer(text = f"Make sure to add your prefix before the commands.")
		await ctx.send(embed=test_e)
	elif sect == 'fun':
		test_e = discord.Embed(colour = 0x33b4cc, title = "😄Fun commands", description = "\n`,rps\nPP\nslots\nrps\nflip\nweather\ngoogle\nnews\njoke\ncoinflip\npoll\nconvert`")
		test_e.set_footer(text = f"Make sure to add your prefix before the commands.")
		await ctx.send(embed=test_e)
	elif sect == 'music':
		test_e = discord.Embed(colour = 0x33b4cc, title = "🎵Music commands", description = "\n`Music system for Python doesn't work.\nThe developers are working on a fix.\nPlease be patient.`")
		test_e.set_footer(text = f"Make sure to add your prefix before the commands.")
		await ctx.send(embed=test_e)
	else:
		test_e = discord.Embed(colour = 0x33b4cc, title = "Prim+ Command List", description = "We have some really [kick-ass](https://discord.gg/Rqn7Dk4) commands!")

		test_e.add_field(name="📷Image", value=f"`{get_prefix}help image`", inline=True)
		test_e.add_field(name="💰Currency", value=f"`{get_prefix}help currency`", inline=True)
		test_e.add_field(name="🛠️Utility", value=f"`{get_prefix}help utility`", inline=True)
		test_e.add_field(name="😄Fun", value=f'`{get_prefix}help fun`', inline=True)
		test_e.add_field(name="⚔️Moderation", value=f'`{get_prefix}help moderation`', inline=True)
		test_e.add_field(name="🎵Music", value=f'`{get_prefix}help music`', inline=True)
		test_e.set_footer(text = "© Developed by 1Terry#9999")
		await ctx.send(embed=test_e)

#Music-command
#"\n`play\nskip\nsonginfo\nremove\nqueue\npause\nresume`"

@client.command()
async def slap(ctx, user: discord.Member = None):
	if user == None:
		user = ctx.author

	slap = Image.open("superhero-meme.jpg")

	asset = user.avatar_url_as(size = 256)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)

	pfp = pfp.resize((333,333))
	slap.paste(pfp, (833,345))

	slap.save("profile.jpg")

	await ctx.send(file = discord.File("profile.jpg"))

@client.command(aliases=['changemymind'])
async def cmm(ctx, *, arg):

	cmm = Image.open("change-my-mind.jpg")
 
	fnt = ImageFont.truetype('Arial.ttf', 40)
	d = ImageDraw.Draw(cmm)
	d.text((283,582), f"{arg}", font=fnt, fill=(0, 0, 0))
 
	cmm.save('terry-is-cool.png')

	await ctx.send(file = discord.File("terry-is-cool.png"))

# 836 585

@client.command(aliases=['sign', 'pepesign'])
async def pepe(ctx, *, arg):

	cmm = Image.open("pepe.png")
	arg = arg.upper()
	fnt = ImageFont.truetype('the TOADFROG.ttf', 14)
	d = ImageDraw.Draw(cmm)
	d.text((11,8), f"{arg}", font=fnt, fill=(0, 0, 0))
 
	cmm.save('terry_le_bonka.png')

	await ctx.send(file = discord.File("terry_le_bonka.png"))

@client.command(aliases=['baw'])
async def blackandwhite(ctx, user: discord.Member = None):
	if user == None:
		user = ctx.author

	asset = user.avatar_url_as(size = 256)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)
	pfp.convert(mode='L').save('terry_the_god.png')

	await ctx.send(file = discord.File("terry_the_god.png"))

@client.command(aliases=['draw'])
async def drawing(ctx, user: discord.Member = None):
	if user == None:
		user = ctx.author

	asset = user.avatar_url_as(size = 256)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)
	img = pfp.filter(CONTOUR)
	img.save('terry_le_god.png')

	await ctx.send(file = discord.File("terry_le_god.png"))

@client.command(aliases=['cl'])
async def clay(ctx, user: discord.Member = None):
	if user == None:
		user = ctx.author

	asset = user.avatar_url_as(size = 256)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)
	img = pfp.filter(EMBOSS)
	img.save('terry_le_g.png')

	await ctx.send(file = discord.File("terry_le_g.png"))

@client.command()
async def smurf(ctx):
	embed = discord.Embed(title="Big smurf play by Terry <a:Smart:777115639088414720>", color=0xcc99cc )
	embed.set_image(url = "https://media.giphy.com/media/kfQSPf4u00qKhGsZ88/giphy.gif")
	await ctx.send(embed=embed)


@client.command()
async def love(ctx, user: discord.Member = None):
	if user == None:
		user = ctx.author

	member = ctx.author

	asset = user.avatar_url_as(size = 128)

	image1 = member.avatar_url_as(size = 128)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)

	image1 = image1.resize((426, 240))
	image1_size = image1.size
	image2_size = image2.size
	new_image = Image.new('RGB',(2*image1_size[0], image1_size[1]), (250,250,250))
	new_image.paste(image1,(0,0))
	new_image.paste(image2,(image1_size[0],0))
	new_image.save("yeahhh_babbbyy.png")

	await ctx.send(file = discord.File("terry_le_ga.png"))

@client.command(aliases=['scary'])
async def weird(ctx, user: discord.Member = None):
	if user == None:
		user = ctx.author

	asset = user.avatar_url_as(size = 128)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)
	img = pfp.filter(ImageFilter.MinFilter(3))
	img.save('terry_le_ga.png')

	await ctx.send(file = discord.File("terry_le_ga.png"))

@client.command()
async def shush(ctx, user: discord.Member = None):
	if user == None:
		user = ctx.author

	slap = Image.open("shush.jpg")

	asset = user.avatar_url_as(size = 128)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)

	pfp = pfp.resize((67,66))
	slap.paste(pfp, (545,164))

	slap.save("shush-get-shit-on-kid-by-the-god-terry.jpg")

	await ctx.send(file = discord.File("shush-get-shit-on-kid-by-the-god-terry.jpg"))

@client.command()
async def cancer(ctx, user: discord.Member = None):
	if user == None:
		user = ctx.author

	slap = Image.open("cancer.png")

	asset = user.avatar_url_as(size = 128)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)

	pfp = pfp.resize((89,80))
	slap.paste(pfp, (253,153))

	slap.save("profile.png")

	await ctx.send(file = discord.File("profile.png"))

@client.command()
async def rip(ctx, user: discord.Member = None):
	if user == None:
		user = ctx.author

	slap = Image.open("rip.png")

	asset = user.avatar_url_as(size = 128)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)

	pfp = pfp.resize((137,103))
	slap.paste(pfp, (108,139))

	slap.save("rip.png")

	await ctx.send(file = discord.File("rip.png"))

@client.command(aliases=["stats"])
async def statistics(ctx):
	embed = discord.Embed(title="Prim+ Statistics.", color=0xcc99cc)
	embed.add_field(name="\nTotal Guilds", value=len(client.guilds), inline=False)
	embed.add_field(name="Total Users", value=len(client.users), inline=False)
	await ctx.send(embed=embed)

@client.command(aliases = ["suggestion", "bug", 'sug'])
async def report(ctx):
	embed = discord.Embed(title="How to make a suggestion or report a bug.", color=0xcc99cc, description = "➤ Go to this [**server**](https://discord.gg/Rqn7Dk4)\n➤ Click on [**suggestions**](https://i.imgur.com/2IqckxH.png)\n➤ Use the [**,poll**](https://i.imgur.com/rUurqOr.png) command\n➤ Look at the [**example**](https://media.giphy.com/media/eo1bdgyHPHutNByTY3/giphy.gif)")
	embed.set_image(url = "https://media.giphy.com/media/eo1bdgyHPHutNByTY3/giphy.gif")
	await ctx.send(embed=embed)

@client.command(aliases=["killme", "suicide", "die", "hotline", "suicideprevention"])
async def selfharm(ctx):
	embed = discord.Embed(title = "Suicide and Self-Harm Prevention", color = 0xead65e, description = "\n**We want you to know you are never alone.**\n\n**__Suicide/Self-Harm Immediate 24/7 Hotlines:__**\n[USA Suicide Hotline](https://suicidepreventionlifeline.org/)\nPhone Number: 1-800-273-8255\n\n[International Suicide Hotlines](https://www.opencounseling.com/suicide-hotlines)\nThese hotlines are made available to those that do not reside in the United States currently. Look up the number on the list that correlates to your residency and call it. It will connect you to your country's suicide hotline.")
	embed.set_thumbnail(url='https://media.discordapp.net/attachments/713779513024184321/769617336558288916/HEART_2.gif?width=145&height=145')
	await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, role: discord.Role, user: discord.Member):
	if ctx.author.guild_permissions.administrator:
		await user.add_roles(role)
		embedVar = discord.Embed(title=" ", description=f"<:greenTICK:753289080044912852> Successfully given {role.name} to {user.name}.", color=0x43b581)
		await ctx.send(embed=embedVar)

@client.command(aliases = ["removerole"])
@commands.has_permissions(manage_roles=True)
async def remrole(ctx, role: discord.Role, user: discord.Member):
	if ctx.author.guild_permissions.administrator:
		await user.remove_roles(role)
		embedVar = discord.Embed(title=" ", description=f"<:greenTICK:753289080044912852> Successfully removed {role.name} from {user.name}.", color=0x43b581)
		await ctx.send(embed=embedVar)

@client.command (pass_context=True)
async def rules(ctx):
	author = ctx.message.author
	
	test_e = discord.Embed(colour = 0x33b4cc)
	
	test_e.set_author(name="How to scrim!")
	test_e.set_thumbnail(url='https://cdn.discordapp.com/attachments/704644736379650088/713093616477929593/2nd_zone_closed.png')
	test_e.add_field(name="__Rules__", value="**\nPlease remember to follow these rules. Failing to do so will result in a** ``BAN``\n\nDo not use Streamer Mode / Anonymous Mode\nTeaming is not allowed\n\nDo not Stream Snipe.\n\nYou may resume fighting once 2nd zone fully closes!\n\nIn event of a storm surge, you may kill where necessary\n\n\n\n\n\n\n\n\n\n", inline=True)
	test_e.set_footer(icon_url=client.user.avatar_url_as(),text="\nGood luck have fun!")
 
	
	await author.send(embed=test_e)

@client.command (pass_context=True)
async def support(ctx):
	author = ctx.message.author
	
	test_e = discord.Embed(colour = 0x33b4cc, timestamp=datetime.datetime.utcnow())

	test_e.set_thumbnail(url="https://media.discordapp.net/attachments/701407585722695691/752412497423761479/prim.png?width=481&height=481")
	test_e.set_author(icon_url=client.user.avatar_url_as(),name="Prim+")
	test_e.add_field(name="Need help with Prim+ or found a bug?", value="\n\n[Join our support server here!](https://discord.gg/jTxQfaz)", inline=False)
	test_e.set_footer(text='Prim+')

	await ctx.send(embed=test_e)

afkdict = {}
@client.command(name = "afk", brief = "Away From Keyboard",
				description = "I'll give you the afk status and if someone pings you before you come back, I'll tell "
							  "them that you are not available. You can add your own afk message!")
@commands.has_permissions(kick_members = True)
async def afk(ctx, message = "AFK"):
	global afkdict

	if ctx.message.author in afkdict:
		afkdict.pop(ctx.message.author)
		await ctx.send('Welcome back! You are no longer afk.')

	else:
		afkdict[ctx.message.author] = message
		await ctx.send(f"{ctx.author.mention} is now AFK: {message}")


@client.event
async def on_message(message):
	global afkdict

	for member in message.mentions:  
		if member != message.author:  
			if member in afkdict:  
				afkmsg = afkdict[member]  
				await message.channel.send(f"{member} is AFK: {afkmsg}")
	await client.process_commands(message)

@client.command(aliases=["inv"])
async def invite(ctx):
	author = ctx.message.author
	
	test_e = discord.Embed(colour = 0x33b4cc, timestamp=datetime.datetime.utcnow())

	test_e.set_thumbnail(url="https://media.discordapp.net/attachments/707725076275003452/754459715928457276/prim.png?width=481&height=481")
	test_e.set_author(icon_url=client.user.avatar_url_as(),name="Prim+")
	test_e.add_field(name="Want to use Prim+ in your own server?", value="\n\n[Invite me!](https://discord.com/oauth2/authorize?client_id=741812768360890481&scope=bot&permissions=2147483647)", inline=False)
	test_e.set_footer(text=f'Prim+')

	await ctx.send(embed=test_e)

@client.command(aliases=['userinfo','info'])
async def whois(ctx, member: discord.Member):
	member = ctx.author if not member else member 
	roles = [role for role in member.roles]
	embed = discord.Embed(
		title = f"{member}", 
		description = f"{member.mention}", 
		colour=random.randint(0x000000, 0xFFFFFF),
		timestamp = datetime.datetime.utcnow()
	)
	embed.add_field(name = "ID", value = f"{member.id}", inline = True)
	embed.set_thumbnail(url = member.avatar_url)
	embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
	embed.add_field(name = "Created at:", value = member.created_at.strftime("%a, %#d %B %Y, %I:%M %p"))
	embed.add_field(name = "Joined at:", value = member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p"))
	embed.add_field(name = f"Roles ({len(roles)})", value="ㅤ", inline=False)
	embed.add_field(name = "Top Role:", value = member.top_role.mention)
	embed.add_field(name = "Bot?", value = member.bot)
	await ctx.send(embed=embed)

@client.command(aliases=['aboutserver'])
@commands.has_permissions(view_audit_log=True)
async def serverinfo(ctx):
	roles = [role for role in ctx.guild.roles]
	members = [member for member in ctx.guild.members]

	embed = discord.Embed(colour=random.randint(0x000000, 0xFFFFFF), timestamp=ctx.message.created_at)
	embed.set_author(name=f"Server Info - {ctx.guild.name}")
	embed.set_thumbnail(url=ctx.guild.icon_url)
	embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
	embed.add_field(name="ID:", value=ctx.guild.id)
	embed.add_field(name="Members:", value=f"{len(members)}")
	embed.add_field(name="Owner:", value=ctx.guild.owner)	
	embed.add_field(name="Created at:", value=ctx.guild.created_at.strftime("%a %#d %B %Y, %I:%M %p"))
	embed.add_field(name=f"Roles ({len(roles)})", value="ㅤ", inline=False)
		
	await ctx.send(embed=embed)

@client.command(aliases = ["newch"])
async def newchannel(ctx, name=None):
	guild = ctx.message.guild
	ch = await guild.create_text_channel(f'{name}')
	await ctx.send(f"I created {ch.mention}")
	await ch.set_permissions(ctx.guild.default_role, read_messages=True, send_messages=True)

@client.command(help='Countsdown from desired time')
async def countdown(ctx, seconds: int=1):
	embed=discord.Embed(title="Countdown", description=str(seconds)+" seconds remaining...")
	msg = await ctx.send(embed=embed)
	i=0
	while i < seconds:
		seconds=seconds-1
	embed.description=str(seconds)+" seconds remaining..."
	await msg.edit(embed=embed)
	await asyncio.sleep(1)
	embed.description="Countdown Complete!"
	await msg.edit(embed=embed)

@client.command(aliases=['speak'])
async def say(ctx,*,msg= " what do you wna say my brudda? "):
	embed=discord.Embed(description=f'{msg}',color=discord.Color.blue())
	
	await ctx.send(embed = embed)

@client.command (pass_context=True)
async def scrimsolo(ctx, *, arg):
	author = ctx.message.author
	
	test_e = discord.Embed(colour = 0x00f9a7)
	test_e = discord.Embed(title='Solo Custom Scrim', url='https://twitch.tv/arbzy')
	
	test_e.add_field(name="Custom Key", value=f"``{arg}``", inline=False)
	test_e.set_thumbnail(url='https://cdn.discordapp.com/attachments/704644736379650088/713093616477929593/2nd_zone_closed.png')
	test_e.add_field(name="Rules", value="Read the rules!", inline=False)
	test_e.set_footer(text = "Thanks for playing our Customs!")
	await ctx.message.delete()
	await ctx.send(embed=test_e)

@client.command (pass_context=True)
async def scrimtrio(ctx, *, arg):
	author = ctx.message.author
	
	test_e = discord.Embed(colour = 0x00f9a7)
	
	test_e.set_author(name="Trio Custom Scrim")
	test_e.add_field(name="Custom Key", value=f"``{arg}``", inline=False)
	test_e.set_thumbnail(url='https://cdn.discordapp.com/attachments/704644736379650088/713093616477929593/2nd_zone_closed.png')
	test_e.add_field(name="Rules", value="Read the rules", inline=False)
	test_e.set_footer(text = "Thanks for playing our Customs!")
	await ctx.message.delete()
	await ctx.send(embed=test_e)
	
@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=10):
	await ctx.message.delete()
	await ctx.channel.purge(limit=amount)
	await ctx.send(f"I have purged `{amount}` messages.", delete_after=5.0)
		
@client.command()
async def coinflip(ctx) :
		choices = ("I choose **HEADS!**",  "I choose tails :/")
		remcoin = random.choice(choices)
		await ctx.send(remcoin)

@client.command(pass_context = True)
async def poll(ctx, question, *options: str):
	author = ctx.message.author
	guild = ctx.message.guild

	if not author.guild_permissions.manage_messages: return await ctx.send(DISCORD_GUILD_ERROR_MSG)

	if len(options) <= 1:
		await ctx.send('```Error! You must format the command like: ,poll "question" yes no```')
		return
	if len(options) > 2:
		await ctx.send('```Error! You must format the command like: ,poll "question" yes no```')
		return

	if len(options) == 2 and options[0] == "no" and options[1] == "yes":
			reactions = ['👎', '👍']
	else:
			reactions = ['👍', '👎']

	description = []
	for x, option in enumerate(options):
		description += '\n\n {} {}'.format(reactions[x], option)

	embed = discord.Embed(title = question, colour=random.randint(0x000000, 0xFFFFFF), description = ''.join(description))

	message = await ctx.send(embed = embed)

	for reaction in reactions[:len(options)]:
		await message.add_reaction(reaction)

	embed.set_footer(icon_url = str(ctx.author.avatar_url), text=f'Created by {ctx.author}')

	await message.edit(embed=embed)

@client.command()
async def convert(ctx, number=0):
	def convert1(seconds):
		seconds = seconds % (24 * 3600)
		hour = seconds // 3600
		seconds %= 3600
		minutes = seconds // 60
		seconds %= 60
		return "%d:%02d:%02d" % (hour, minutes, seconds)
	await ctx.send(f'{number} seconds in Seconds, Minutes and Hours is:')
	await ctx.send(f'`{convert1(number)}`')

@client.command()
async def roll(ctx) :
		choices = ("You rolled 6 **WOW LUCKY**",  "You rolled a 1 **yikes**",  "You rolled a 4 `decent.`",  "You rolled a 2 *oof*",  "You rolled a 3 **meh** average.",  "You rolled a 5 **NICE!**")
		remcoin = random.choice(choices)
		await ctx.send(remcoin)

@client.command(aliases=['av'])
async def avatar(ctx, *, user: discord.Member = None):
	if not user:
		user = ctx.author
	eA = discord.Embed(title='Avatar', color=0xab455a)
	eA.set_author(name=user, icon_url=user.avatar_url)
	if str(user.avatar_url).endswith(".gif?size=1024"):
		eA.set_image(url=user.avatar_url_as(format="gif", size=1024))
	else:
		eA.set_image(url=user.avatar_url_as(format="png", size=1024))
	await ctx.send(embed=eA)

@client.command()
async def fspam(ctx, message):
	for i in range(1, 50):
		await ctx.send(message)
		
for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)
