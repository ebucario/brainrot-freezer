from pathlib import Path
import discord
from discord import app_commands
from discord.ext.commands import Bot
from threading import Thread
from typing import cast

from . import sound
from . import queue
from .db import db

intents = discord.Intents.default()
intents.message_content = True

bot = Bot(command_prefix=(), description="""brainrot bot""", intents=intents)

if not isinstance(db.get("channels"), list):
	db["channels"] = []

@bot.event
async def on_ready():
	print(f'logged in as {bot.user}')

async def brainrot_error(inx: discord.Interaction, err: discord.app_commands.AppCommandError):
	await inx.response.send_message(f"⚠️ error: {err})")
bot.tree.on_error = brainrot_error

@bot.tree.command(description="register this channel for brainrot integration")
async def brainrot_register_channel(inx: discord.Interaction):
	channel = inx.channel.id # type: ignore
	if channel in db["channels"]:
		await inx.response.send_message("❌ this channel was already registered.", ephemeral=True)
	else:
		db["channels"].append(channel)
		db.save()
		print(f"registered to channel: {channel}")
		await inx.response.send_message("✅ registered this channel for brainrot.")

@bot.tree.command(description="remove this channel from brainrot integration")
async def brainrot_deregister_channel(inx: discord.Interaction):
	channel = inx.channel.id # type: ignore
	try:
		db["channels"].remove(channel)
		db.save()
		print(f"removed channel: {channel}")
		await inx.response.send_message("✅ deregistered this channel!")
	except ValueError:
		await inx.response.send_message("❌ this channel wasn't registered.")

@bot.tree.command(description="consume all the messages in a channel")
async def brainrot_consume(inx: discord.Interaction):
	if inx.channel.id not in db["channels"]:
		return await inx.response.send_message("❌ this won't work until you register this channel.")
	if not hasattr(inx.channel, 'history'):
		raise ValueError("no history in this channel")
	async for message in inx.channel.history(oldest_first=True):
		await on_message(message)
	await inx.response.send_message("✅ successfully consumed the channel!")

@bot.event
async def on_message(message: discord.Message):
	if message.author == bot.user:
		return
	if message.channel.id not in db["channels"]:
		return
	if len(message.attachments) == 0:
		return
	for attachment in message.attachments:
		if attachment.content_type.startswith('audio') and attachment.content_type != 'audio/ogg':
			return await message.reply("ℹ️ currently only brainrot in .ogg format works.")
		filename = attachment.filename
		print(f"found sound: {filename}")
		path = Path(sound.SOUND_PATH, filename)
		await attachment.save(path)
		print(f"saved to {path}")
		queue.enqueue(200, sound._load_sounds)
		await message.reply(f"✅ saved to \"{path}\".")
		sound.try_play_next(path.stem)

if not isinstance(db.get("token"), str):
	raise TypeError(f"discord token was not string (got {db.get('token')} instead)")

# async def setup_hook():
# 	print("attempting to sync tree...")
# 	print(bot.tree.copy_global_to(guild=discord.Object(id=1012522655460638730)))
# 	print(await bot.tree.sync(guild=discord.Object(id=1012522655460638730)))
# 	print("tree synced!")

# bot.setup_hook = setup_hook

def run_bot():
	bot.run(db["token"])

Thread(target=run_bot, daemon=True).start()