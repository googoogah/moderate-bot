#from webserver import keep_alive
import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

keep_alive()

intents = discord.Intents.default()
intents.reactions = True
intents.presences = True
intents.message_content = True
intents.members = True
intents.typing = True

bot = commands.Bot(command_prefix='!', intents=intents)

log_channel_id = 1133127805845114941  # Specify the log channel ID here

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_raw_reaction_add(payload):
    if payload.guild_id is None:  # Ignore reactions from direct messages
        return

    guild = bot.get_guild(payload.guild_id)
    channel = guild.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = bot.get_user(payload.user_id)
    emoji = payload.emoji

    log_embed = discord.Embed(title="Reaction Added",
                              description=f"Emoji: {emoji}\n"
                                          f"Author: {user.mention}\n"
                                          f"Channel: {channel.mention}\n"
                                          f"Message ID: {message.id}\n"
                                          f"Link to Message: [Jump to Message]({message.jump_url})",
                              color=discord.Color.green())
    log_embed.timestamp = discord.utils.utcnow()

    await send_log_message(log_embed)

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.guild_id is None:  # Ignore reactions from direct messages
        return

    guild = bot.get_guild(payload.guild_id)
    channel = guild.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = bot.get_user(payload.user_id)
    emoji = payload.emoji

    # Get the user who removed the reaction
    remover = bot.get_user(payload.user_id)

    log_embed = discord.Embed(title="Reaction Removed",
                              description=f"Emoji: {emoji}\n"
                                          f"Author: {user.mention}\n"
                                          f"Removed by: {remover.mention}\n"  # Mention the user who removed the reaction
                                          f"Channel: {channel.mention}\n"
                                          f"Message ID: {message.id}\n"
                                          f"Link to Message: [Jump to Message]({message.jump_url})",
                              color=discord.Color.red())
    log_embed.timestamp = discord.utils.utcnow()

    await send_log_message(log_embed)

@bot.event
async def on_message_delete(message):
    author = message.author
    channel = message.channel
    reactions = message.reactions

    log_embed = discord.Embed(title="Message Deleted",
                              description=f"Reactions on the Message: {', '.join(str(reaction) for reaction in reactions)}\n"
                                          f"Author of Reactions: {author.mention}\n"
                                          f"User who deleted the Message: {bot.user.mention}\n"
                                          f"Channel: {channel.mention}\n"
                                          f"Message ID: {message.id}\n"
                                          f"Link to Message: [Jump to Message]({message.jump_url})",
                              color=discord.Color.orange())
    log_embed.timestamp = discord.utils.utcnow()

    await send_log_message(log_embed)

async def send_log_message(embed):
    global log_channel_id

    log_channel = bot.get_channel(log_channel_id)
    if log_channel is not None:
        await log_channel.send(embed=embed)


keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))