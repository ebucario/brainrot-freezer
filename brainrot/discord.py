from collections.abc import MutableMapping
from pathlib import Path
import discord
from discord import app_commands
from discord.ext.commands import Bot
from threading import Thread

from . import sound
from .db import db

intents = discord.Intents.default()
intents.message_content = True

bot = Bot(command_prefix='/', description="""brainrot bot""", intents=intents)

if not isinstance(db.get("channels"), MutableMapping):
	db["channels"] = {}

@bot.event
async def on_ready():
	print(f'logged in as {bot.user}')

@bot.command(description="register this channel for brainrot integration")
async def brainrot_register_channel(ctx):
	channel = ctx.channel.id
	if channel in db["channels"]:
		await ctx.send_response("❌ this channel was already registered.", ephemeral=True)
	else:
		db["channels"].append(channel)
		print(f"registered to channel: {channel}")
		await ctx.send_response("✅ registered this channel!", ephemeral=True)

@bot.command(description="remove this channel from brainrot integration")
async def brainrot_deregister_channel(ctx):
	channel = ctx.channel.id
	try:
		db["channels"].remove(channel)
		print(f"removed channel: {channel}")
		await ctx.send_response("✅ deregistered this channel!", ephemeral=True)
	except ValueError:
		await ctx.send_response("❌ this channel wasn't registered.", ephemeral=True)

@bot.command(description="consume all the messages in a channel")
async def brainrot_consume(ctx):
	async for message in reversed(list(ctx.channel.history())):
		await on_message(message)
	await ctx.send_response("✅ successfully consumed the channel!", ephemeral=True)

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	if message.channel.id not in db["channels"]:
		return
	if len(message.attachments) == 0:
		return
	for attachment in message.attachments:
		if attachment.content_type in ('video/ogg', 'audio/ogg', 'application/ogg'):
			filename = attachment.filename
			print(f"found sound: {filename}")
			path = Path(sound.SOUND_PATH, filename)
			attachment.save(path)
			print(f"saved to {path}")
			queue.enqueue(200, sound._load_sounds())

if not isinstance(db.get("token"), str):
	raise TypeError(f"discord token was not string (got {db.get('token')} instead)")

def run_bot():
	bot.run(db["token"])

Thread(target=run_bot, daemon=True).start()