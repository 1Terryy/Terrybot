import discord
from discord.ext import commands
from datetime import *
import asyncio
from datetime import timedelta
from discord.ext.commands import BucketType, cooldown
import json
import string
import random

seconds_in_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
def convertToSeconds(timeduration):
	return int(timeduration[:-1]) * seconds_in_unit[timeduration[-1]]


class Moderation(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	@commands.has_permissions(manage_roles=True)
	async def tempmute(self, ctx, user: discord.Member, timeduration, *, reason: str = "No reason specified"):
		server = ctx.channel.guild
		role = discord.utils.get(ctx.guild.roles, name="Muted")
		if not role in user.roles:
			userID = (user.id)
			embed = discord.Embed(title="Member muted", color = 0xFF0000)
			embed.add_field(name="Member", value="{} ".format(user) + "(<@{}>)".format(userID), inline=True)
			embed.add_field(name="Moderator", value="<@{}>".format(ctx.message.author.id), inline=True)
			embed.add_field(name="Duration", value=timeduration, inline=True)
			embed.add_field(name="Reason", value="{}".format(reason), inline=True)
			embed.set_thumbnail(url=user.avatar_url)
			embed.timestamp = datetime.utcnow()
			await user.add_roles(role)
			await ctx.send(embed=embed)
			await user.send(f"You were temporarily muted in {ctx.guild.name} for {timeduration} for: {reason}.")
			await ctx.message.delete()

			theTime = convertToSeconds("{}".format(timeduration))
			await asyncio.sleep(int(theTime))
			try:
				await user.remove_roles(role)
			except:
				pass
		else:
			await ctx.send("This member is already muted")

	@tempmute.error
	async def tempmute_error(self, ctx, error):
		if str(error) == 'Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions' or str(error) == 'Command raised an exception: Forbidden: 403 Forbidden (error code: 50001): Missing Access':
			await ctx.send("I don't have the permission to mute this member !")
		elif isinstance(error, commands.CheckFailure):
			await ctx.send("You don't have the permission to use this command.")
		elif isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send("There is one or more arguments missing : `,tempmute <member> <duration> [reason]`")
		elif isinstance(error, commands.errors.BadArgument):
			await ctx.send("One or more arguments are incorrect : `,tempmute <member> <duration> [reason]`")
		else:
			raise error

	@commands.command()
	@commands.has_permissions(manage_roles=True)
	async def mute(self, ctx, user: discord.Member, *, reason: str = "No reason specified"):
		role = discord.utils.get(ctx.guild.roles, name="Muted")
		if not role in user.roles:
			embed = discord.Embed(title="Member muted", color = 0xFF0000)
			embed.add_field(name="Member", value="{} ".format(user) + "(<@{}>)".format(user.id), inline=True)
			embed.add_field(name="Moderator", value="<@{}>".format(ctx.message.author.id), inline=True)
			embed.add_field(name="Reason", value="{}".format(reason), inline=True)
			embed.set_thumbnail(url=user.avatar_url)
			embed.timestamp = datetime.utcnow()
			await user.add_roles(role)
			await ctx.message.delete()
			await user.send(f"You were muted in {ctx.guild.name} for: {reason}.")
			await ctx.send(embed=embed)
		else:
			await ctx.send("This member is already muted !")

	@mute.error
	async def mute_error(self, ctx, error):
		if str(error) == 'Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions' or str(error) == 'Command raised an exception: Forbidden: 403 Forbidden (error code: 50001): Missing Access':
			await ctx.send("I don't have the permission to mute this member !")
		elif isinstance(error, commands.CheckFailure):
			await ctx.send("You don't have the permission to use this command.")
		elif isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send("There is one or more arguments missing : `,mute <member> [reason]`")
		elif isinstance(error, commands.errors.BadArgument):
			await ctx.send("One or more arguments are incorrect : `,mute <member> [reason]`")
		else:
			raise error

	@commands.command()
	@commands.has_permissions(manage_roles=True)
	async def unmute(self, ctx, user: discord.Member):
		role = discord.utils.get(ctx.guild.roles, name="Muted")
		if role in user.roles:
			embed = discord.Embed(title="Member unmuted", color = 0x0000FF)
			embed.add_field(name="Member", value="{} ".format(user) + "(<@{}>)".format(user.id), inline=True)
			embed.set_thumbnail(url=user.avatar_url)
			embed.timestamp = datetime.utcnow()
			await user.remove_roles(role)
			await ctx.message.delete()
			await ctx.send(embed=embed)
		else:
			await ctx.send("This member isn't muted")

	@unmute.error
	async def unmute_error(self, ctx, error):
		if str(error) == 'Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions' or str(error) == 'Command raised an exception: Forbidden: 403 Forbidden (error code: 50001): Missing Access':
			await ctx.send("I do not have the permission to unmute this member")
		elif isinstance(error, commands.CheckFailure):
			await ctx.send("You don't have the permission to use this command")
		elif isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send("The `member` argument is missing : `,unmute <member>`")
		elif isinstance(error, commands.errors.BadArgument):
			await ctx.send("The `member` argument is incorrect : `,unmute <member>`")
		else:
			raise error

	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, user: discord.Member, *, reason:str="No reason specified"):
		embed = discord.Embed(title="Member banned", color = 0xFF0000)
		embed.add_field(name="Member", value="{} ".format(user) + "(<@{}>)".format(user.id), inline=True)
		embed.add_field(name="Moderator", value="<@{}>".format(ctx.message.author.id), inline=True)
		embed.add_field(name="Reason", value="{}".format(reason), inline=True)
		await user.send(f"You were banned in {ctx.guild.name} for: {reason}.")
		await ctx.guild.ban(user, reason=reason, delete_message_days=7)
		await ctx.message.delete()
		await ctx.send(embed=embed)

	@ban.error
	async def ban_error(self, ctx, error):
		if str(error) == 'Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions' or str(error) == 'Command raised an exception: Forbidden: 403 Forbidden (error code: 50001): Missing Access':
			await ctx.send("I do not have the permission to ban this member.")
		elif isinstance(error, commands.CheckFailure):
			await ctx.send("You don't have the permission to use this command")
		elif isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send("There is one or more arguments that are missing : `,ban <member> [reason]`")
		elif isinstance(error, commands.errors.BadArgument):
			await ctx.send("One or more arguments are incorrect : `,ban <member> [reason]`")
		else:
			raise error

	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def unban(self, ctx, user: discord.User):
		embed = discord.Embed(title="Member unbanned", color = 0xFF0000)
		embed.add_field(name="Member", value="{} ".format(user) + "(<@{}>)".format(user.id), inline=True)
		embed.add_field(name="Moderator", value="<@{}>".format(ctx.message.author.id), inline=True)
		await ctx.guild.unban(user)
		await ctx.message.delete()
		await ctx.send(embed=embed)


	@unban.error
	async def unban_error(self, ctx, error):
		if str(error) == 'Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions' or str(error) == 'Command raised an exception: Forbidden: 403 Forbidden (error code: 50001): Missing Access':
			await ctx.send("I do not have the permission to unban this member")
		elif isinstance(error, commands.CheckFailure):
			await ctx.send("You don't have the permission to use this command.")
		elif isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send("There is one argument missing : `,unban <member>`")
		elif isinstance(error, commands.errors.BadArgument):
			await ctx.send("An argument is incorrect : `,unban <member>`")
		else:
			raise error

	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def tempban(self, ctx, user: discord.Member, timeduration, *, reason: str = "No reason specified"):
		server = ctx.channel.guild
		userID = (user.id)
		embed = discord.Embed(title="Member banned", color = 0xFF0000)
		embed.add_field(name="Member", value="{} ".format(user) + "(<@{}>)".format(userID), inline=True)
		embed.add_field(name="Moderator", value="<@{}>".format(ctx.message.author.id), inline=True)
		embed.add_field(name="Duration", value=timeduration, inline=True)
		embed.add_field(name="Reason", value="{}".format(reason), inline=True)
		embed.set_thumbnail(url=user.avatar_url)
		embed.timestamp = datetime.utcnow()
		await user.send(f"You were temporarily banned from {ctx.guild.name} for: {timeduration} for: {reason}.")
		await server.ban(user, reason=reason, delete_message_days=7)
		await ctx.send(embed=embed)
		await ctx.message.delete()
		theTime = convertToSeconds("{}".format(timeduration))
		await asyncio.sleep(int(theTime))
		try:
			await server.unban(user)
		except:
			pass

	@tempban.error
	async def tempban_error(self, ctx, error):
		if str(error) == 'Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions' or str(error) == 'Command raised an exception: Forbidden: 403 Forbidden (error code: 50001): Missing Access':
			await ctx.send("I do not have the permission to ban this member")
		elif isinstance(error, commands.CheckFailure):
			await ctx.send("You don't have the permission to use this command.")
		elif isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send("One or more arguments are missing : `,tempban <member> <duration> [reason]`")
		elif isinstance(error, commands.errors.BadArgument):
			await ctx.send("One or more arguments are incorrect : `,tempban <member> <duration> [reason]`")
		else:
			raise error

	@commands.command()
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, user: discord.Member, *, reason: str = "No reason specified"):
		embed = discord.Embed(title="Member kicked", color = 0xFF0000)
		embed.add_field(name="Member", value="{} ".format(user) + "(<@{}>)".format(user.id), inline=True)
		embed.add_field(name="Moderator", value="<@{}>".format(ctx.message.author.id), inline=True)
		embed.add_field(name="Reason", value="{}".format(reason), inline=True)
		await user.send(f"You were kicked in {ctx.guild.name} for: {reason}.")
		await ctx.guild.kick(user, reason=reason)
		await ctx.message.delete()
		await ctx.send(embed=embed)

	@kick.error
	async def kick_error(self, ctx, error):
		if str(error) == 'Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions' or str(error) == 'Command raised an exception: Forbidden: 403 Forbidden (error code: 50001): Missing Access':
			await ctx.send("I don't have the permission to kick this member")
		elif isinstance(error, commands.CheckFailure):
			await ctx.send("You don't have the permission to use this command")
		elif isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send("There is one or more arguments missing : `,kick <member> [reason]`")
		elif isinstance(error, commands.errors.BadArgument):
			await ctx.send("One or more arguments are incorrect : `,kick <member> [reason]`")
		else:
			raise error
		
	@commands.command()
	@commands.has_permissions(view_audit_log=True)
	async def warn(self, ctx, user:discord.Member, *, reason:str="No reason specified"):
		dt = datetime.utcnow()
		if len(reason) > 1000:
			raise ValueError("The given reason is too long ! (1000 characters maximum)")
		with open("warns.json", "r") as warns:
			dic = json.load(warns)
		idlist = list(string.ascii_letters + string.digits)
		id = ''
		for i in range(6):
			id += random.choice(idlist)
		if str(ctx.guild.id) in dic:
			if str(user.id) in dic[str(ctx.guild.id)]:
				dic[str(ctx.guild.id)][str(user.id)][id] = {"reason":reason, "date":dt.replace().timestamp()}
			else:
				dic[str(ctx.guild.id)][str(user.id)] = {}
				dic[str(ctx.guild.id)][str(user.id)][id] = {"reason":reason, "date":dt.replace().timestamp()}
		else:
			dic[str(ctx.guild.id)] = {}
			dic[str(ctx.guild.id)][str(user.id)] = {}
			dic[str(ctx.guild.id)][str(user.id)][id] = {"reason":reason, "date":dt.replace().timestamp()}
		with open("warns.json", "w") as warns:
			json.dump(dic, warns, indent=4)
		embed = discord.Embed(title="Member warned", color = 0xFF0000)
		embed.add_field(name="Member", value="{} ".format(user) + "(<@{}>)".format(user.id), inline=True)
		embed.add_field(name="Moderator", value="<@{}>".format(ctx.message.author.id), inline=True)
		embed.add_field(name="Reason", value="{}".format(reason), inline=True)
		await ctx.message.delete()
		await ctx.send(embed=embed)
		await user.send(f"You were warned in {ctx.guild.name} for: {reason}.")

	@warn.error
	async def warn_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError) and str(error) == "Command raised an exception: ValueError: The given reason is too long ! (1000 characters maximum)":
			await ctx.send("The given reason is too long ! (1000 characters maximum)")
		elif isinstance(error, commands.CheckFailure):
			await ctx.send("You don't have the permission to use this command")
		elif isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send("One or more arguments are missing : `,warn <member> [reason]`")
		elif isinstance(error, commands.errors.BadArgument):
			await ctx.send("One or more arguments are incorrect : `,warn <member> [reason]`")
		else:
			raise error

	@commands.command(aliases=["infractions", "warnings"])
	@commands.has_permissions(view_audit_log=True)
	async def warns(self, ctx, user:discord.Member):
		with open("warns.json", "r") as warns:
			dic = json.load(warns)
		if str(ctx.guild.id) in dic and str(user.id) in dic[str(ctx.guild.id)]:
			embed = discord.Embed(title=str(len(dic[str(ctx.guild.id)][str(user.id)])) + " warn(s)", color=0xff0000)
			embed.set_author(name="Warns of " + user.name + "#" + str(user.discriminator))
			embed.set_thumbnail(url=user.avatar_url)
			embed.timestamp = datetime.utcnow()
			for warn in dic[str(ctx.guild.id)][str(user.id)]:
				embed.add_field(name=datetime.fromtimestamp(dic[str(ctx.guild.id)][str(user.id)][warn]["date"]).strftime('The %d/%m/%Y, at %H:%M:%S'), value="Reason : " + dic[str(ctx.guild.id)][str(user.id)][warn]['reason'] + "\nID : " + warn, inline=False)
			await ctx.send(embed=embed)
		else:
			embed = discord.Embed(title = "This user does not have any warnings.", color=0xFF0000)
			await ctx.send(embed=embed)

	@warns.error
	async def warns_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send("You don't have the permission to use this command")
		elif isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send("The \"member\" argument is missing : `,warns <member>`")
		elif isinstance(error, commands.errors.BadArgument):
			await ctx.send("The given argument is incorrect : `,warns <member>`")
		elif isinstance(error, commands.errors.CommandInvokeError) and str(error) == "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\nIn embed: Embed size exceeds maximum size of 6000":
			await ctx.send("This person has too many warns, I can't show them all")
		else:
			raise error
		
	@commands.command(aliases=["reset-warns", "remwarn", "delwarn"])
	@commands.has_permissions(view_audit_log=True)
	async def reset_warns(self, ctx, user:discord.Member=None, count:str=None):
		if count == None:	
			if user == None:
				user = ctx.message.author
			with open("warns.json", "r") as warns:
				dic = json.load(warns)
			dic[str(ctx.guild.id)].pop(str(user.id))
			with open("warns.json", "w") as warns:
				json.dump(dic, warns, indent=4)
			await ctx.send("<@{}>'s warns has been resetted.".format(user.id))
		else:
			with open("warns.json", "r") as warns:
				dic = json.load(warns)
			dic[str(ctx.guild.id)][str(user.id)].pop(count)
			with open("warns.json", "w") as warns:
				json.dump(dic, warns, indent=4)
			embed = discord.Embed(title="Warn deleted for {}#{} with the ID: {}".format(user.name, user.discriminator, count), color=0x00FFE1)
			await ctx.send(embed=embed)
				
	@commands.Cog.listener()
	async def on_guild_channel_create(self, channel):
		role = discord.utils.get(channel.guild.roles, name="Muted")
		if str(channel.type) == "text":
			await channel.set_permissions(role, send_messages=False)

	@commands.command()
	@cooldown(1, 300, BucketType.user)
	@commands.has_permissions(administrator=True)
	async def nuke(self, ctx, channels : discord.TextChannel=None):
		if channels == None:
			await ctx.send('Give a channel')
			return
		if ctx.author != ctx.guild.owner:
			await ctx.send('Only **{}** Can use this Command'.format(ctx.guild.owner))
		else:
			verif = await ctx.send('Are you sure!')
			await ctx.send('Type in `yes`. To proceed')

			def check(m):
				user = ctx.author
				return m.author.id == user.id and m.content == 'yes'

			msg = await self.bot.wait_for('message', check=check)
			await ctx.channel.send('Theres no going back!\n**Are you sure.**')
			def check(m):
				user = ctx.author
				return m.author.id == user.id and m.content == 'yes'

			msg = await self.bot.wait_for('message', check=check)
			new = await channels.clone()
			await channels.delete()
			await new.send('https://media1.tenor.com/images/6c485efad8b910e5289fc7968ea1d22f/tenor.gif?itemid=5791468')
			await asyncio.sleep(2)
			await new.send('**Terry** has nuked this channel!')
			
	@commands.command()
	@commands.has_permissions(manage_channels=True)
	async def lock(self, ctx, channel: discord.TextChannel=None):
		channel = channel or ctx.channel

		if ctx.guild.default_role not in channel.overwrites:
			overwrites = {
			ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
			}
			await channel.edit(overwrites=overwrites)
			await ctx.send("**The channel `{}` has successfully been locked!**".format(ctx.channel.name))
		elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
			overwrites = channel.overwrites[ctx.guild.default_role]
			overwrites.send_messages = False
			await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
			await ctx.send("**The channel `{}` has successfully been locked!**".format(ctx.channel.name))
		else:
			overwrites = channel.overwrites[ctx.guild.default_role]
			overwrites.send_messages = True
			await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
			await ctx.send('**The channel `{}` has now been unlocked!**'.format(ctx.channel.name))
	
def setup(client):
	client.add_cog(Moderation(client))