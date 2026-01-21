from pathlib import Path
import discord
from discord import app_commands
from discord.ext.commands import Bot
from threading import Thread

from brainrot import sound
from brainrot.db.models import DiscordToken, DiscordChannel, QueuedSound, Sound

intents = discord.Intents.default()
intents.message_content = True

bot = Bot(command_prefix=(), description="""brainrot bot""", intents=intents)

@bot.event
async def on_ready():
	print(f'logged in as {bot.user}')

async def brainrot_error(inx: discord.Interaction, err: discord.app_commands.AppCommandError):
	await inx.response.send_message(f"⚠️ error: {err})")
bot.tree.on_error = brainrot_error

@bot.tree.command(description="register this channel for brainrot integration")
async def brainrot_register_channel(inx: discord.Interaction):
	channel_id = inx.channel.id # type: ignore
	channel = DiscordChannel.get_or_none(DiscordChannel.id == channel_id)
	if channel is None:
		channel = DiscordChannel.create(discord_id=channel_id)
		print(f"registered to channel: {channel_id}")
		await inx.response.send_message("✅ registered this channel for brainrot.")
	else:
		await inx.response.send_message("❌ this channel was already registered.", ephemeral=True)

@bot.tree.command(description="remove this channel from brainrot integration")
async def brainrot_deregister_channel(inx: discord.Interaction):
	channel_id = inx.channel.id # type: ignore
	channel = DiscordChannel.get_or_none(DiscordChannel.id == channel_id)
	if channel is not None:
		channel.delete_instance()
		await inx.response.send_message("✅ deregistered this channel!")
	else:
		await inx.response.send_message("❌ this channel wasn't registered.")

@bot.tree.command(description="consume all the messages in a channel")
async def brainrot_consume(inx: discord.Interaction):
	channel_id = inx.channel.id # type: ignore
	if DiscordChannel.get_or_none(DiscordChannel.id == channel_id) is None:
		return await inx.response.send_message("❌ this won't work until you register this channel.")
	if not hasattr(inx.channel, 'history'):
		raise ValueError("no history in this channel")
	async for message in inx.channel.history(oldest_first=True): # type: ignore
		await on_message(message)
	await inx.response.send_message("✅ successfully consumed the channel!")

@bot.event
async def on_message(message: discord.Message):
	if message.author == bot.user:
		return
	if DiscordChannel.get_or_none(DiscordChannel.id == message.channel.id) is None:
		return
	if len(message.attachments) == 0:
		return
	for attachment in message.attachments:
		if attachment.content_type.startswith('audio') and attachment.content_type != 'audio/ogg': # type: ignore
			return await message.reply("ℹ️ currently only brainrot in .ogg format works.")
		if attachment.content_type != 'audio/ogg':
			return
		filename = attachment.filename
		print(f"found sound: {filename}")
		path = Path(sound.SOUND_PATH, filename)
		if path.is_file():
			return await message.reply(f"❌ there's already a sound file at \"{path}\"!")
		await attachment.save(path)
		sound_ = Sound.create(path=path)
		print(f"saved to {path}")
		qs = QueuedSound.create(sound=sound_)
		await message.reply(f"✅ saved to \"{path}\".")

token = DiscordToken.get_or_none()

if token is None:
	raise TypeError(f"discord token missing! is it in the database?")

# async def setup_hook():
# 	print("attempting to sync tree...")
# 	print(bot.tree.copy_global_to(guild=discord.Object(id=1262554097723117568)))
# 	print(await bot.tree.sync(guild=discord.Object(id=1262554097723117568)))
# 	print("tree synced!")

# bot.setup_hook = setup_hook

def run_bot():
	bot.run(token.token)

Thread(target=run_bot, daemon=True).start()