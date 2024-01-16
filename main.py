

#PRE PART
import nextcord
import asyncio
import time
from nextcord.ext import commands, tasks
from itertools import cycle
import os
import json
import random
from nextcord.ext import application_checks
from nextcord.abc import GuildChannel
from nextcord import Interaction,SlashOption
from function import *

TOKEN="MTE5Mjg5MTYwODQ0NjgxNjQyNw.GxGaBU.upnQ5xYU0bWIaVCFJmsFN_Lz1FGi32Rpoa78vo"
bot_status = cycle(["Type /playsnake to play!","Snake bot with mutiplayer!","Type /setup to setup snaky!","Snaky is created by AnsonDev!"])

permissionscheck = ["view_channel","send_messages","manage_messages","manage_channels","manage_guild","embed_links","attach_files","add_reactions","use_external_emojis","use_external_stickers","read_message_history","use_slash_commands","read_messages"]


client = commands.Bot(command_prefix = '!', intents = nextcord.Intents.all())

directionemojis = ["⬆️", "⬇️", "⬅️", "➡","🛑"]

@tasks.loop(seconds=20)
async def change_status():
  await client.change_presence(activity=nextcord.Game(next(bot_status)))


@client.event
async def on_guild_remove(guild):
  with open("catelog.json", "r") as f:
    channel = json.load(f)

  channel.pop(str(guild.id))

  with open("catelog.json", "w") as f:
    json.dump(channel, f, indent=4)

  with open("commandchannel.json", "r") as f:
    commandchannel = json.load(f)

  commandchannel.pop(str(guild.id))

  with open("commandchannel.json", "w") as f:
    json.dump(commandchannel, f, indent=4)

@client.slash_command(name="help", description="Get the help panel!")

async def help(interaction: Interaction):
  checker = await send_permission_error(interaction)
  if checker == "notok":
    return
  help_embed = nextcord.Embed(title="Snaky Bot Help Menu", description="All the commands and setup with it!", color=nextcord.Color.blue())
  help_embed.set_image(url="https://cdn.discordapp.com/attachments/1193129827742515311/1194831279250747493/funnysnakeyer.png?ex=65b1c857&is=659f5357&hm=4332beae4b13a45c55ae72946c5b5e1aa9df96bc846787aa290de1722be5e378&")
  help_embed.add_field(name="Setup", value="To setup the bot.First,type /channel 'SELECT YOUR CHANNEL' to let Snaky know what channel can only use Snaky there.Next,type /setup 'SELECT YOUR CATEGORY' to select the category that store Snaky's game.")
  help_embed.add_field(name="Play", value="To play the game, use /playsnake 'OPTIONS' to start the game")
  help_embed.add_field(name="Clear", value="Type /clear_all (ONLY FOR ADMIN IN SERVER) to delete all in playing snake game.")
  help_embed.add_field(name="Score", value="Type /score to get your own highscore.")

  help_embed.add_field(name="Global score", value="Type /globalscore to get the top 3 highest score.")
  help_embed.add_field(name="Rank", value="Type /rank to see your rank!")
  help_embed.add_field(name="Server highest score", value="Type /serverscore to see the highest score in the server.")
  await interaction.user.send(embed=help_embed)
  await interaction.response.send_message("Check your DM!")


@client.event
async def on_raw_reaction_add(payload):

  channel = await client.fetch_channel(payload.channel_id)
  message = await channel.fetch_message(payload.message_id)

  # Get the member object
  guild = message.guild
  member = await guild.fetch_member(payload.user_id)
  category_id = server_catelog(message)
  if category_id == None:
    await channel.send("This server has not set up Snaky yet!")
    return
  category = nextcord.utils.get(guild.categories, id=int(category_id))
  
  channelcheck = nextcord.utils.get(category.text_channels, id=message.channel.id)
  
  if channelcheck == None:
    return
  
  if payload.member.bot:
    return
  
  if payload.emoji.name not in directionemojis:
    # Remove reaction


    
    await message.remove_reaction(payload.emoji.name, member)
    return

  
  user_reaction_count = 0
  for r in message.reactions:
      async for u in r.users():
          if u.id == payload.user_id:
              user_reaction_count+=1
              if user_reaction_count>1:
                  
                  await message.remove_reaction(payload.emoji.name, member)
                  break
@client.event
async def on_message(message):
  if not message.author.bot:
    if isinstance(message.channel, nextcord.channel.DMChannel):
      await message.channel.send("Sorry! You cannot use Snaky in dm! You can use this link to invite me to your server: https://discord.com/api/oauth2/authorize?client_id=1191767048401997864&permissions=8&scope=bot")
  else:
    return


@client.slash_command(name="setup", description="Setup the playing category!")
@application_checks.has_permissions(administrator=True)

async def setup(interaction: Interaction,setcategory: GuildChannel = SlashOption(channel_types=[nextcord.ChannelType.category],required=True)):
  checker = await send_permission_error(interaction)
  if checker == "notok":
    return
  
  set_command_channel_id = get_commandchannel(interaction)
  if set_command_channel_id == None:
    set_command_channel_id = str(interaction.channel.id)
  if set_command_channel_id == str(interaction.channel.id):
    
    savecatelog_id = str(setcategory.id)
  
    with open("catelog.json", "r") as f:
      catelog = json.load(f)
  
    catelog[str(interaction.guild.id)] = savecatelog_id
  
    with open("catelog.json", "w") as f:
      json.dump(catelog, f, indent=4)

    
    
  
    await interaction.response.send_message("Catelogory has been set to " + setcategory.name)
    
  else:
    await interaction.response.send_message("You cannot use snaky command here!",ephemeral=True)


@client.slash_command(name="channel", description="Set the channel that only can use snaky!")
@application_checks.has_permissions(administrator=True)

async def channel(interaction: Interaction,setchannel: GuildChannel = SlashOption(channel_types=[nextcord.ChannelType.text],required=True)):

  checker = await send_permission_error(interaction)
  if checker == "notok":
    return
  
  commandchannel = str(setchannel.id)
  
  with open("commandchannel.json", "r") as f:
    channel = json.load(f)
  
  channel[str(interaction.guild.id)] = commandchannel
  
  with open("commandchannel.json", "w") as f:
    json.dump(channel, f, indent=4)
  
  await interaction.response.send_message(f"Command channel has been set to {setchannel.name}")


@client.slash_command(name="clearall", description="End all in-process game!")
@application_checks.has_permissions(administrator=True)

async def clear_all(interaction: Interaction):
  checker = await send_permission_error(interaction)
  if checker == "notok":
    return
  catid = server_catelog(interaction)
  if catid == None:
    await interaction.response.send_message("This server has not set up Snaky yet!",ephemeral=True)
    return
  cat = client.get_channel(int(catid))
  
  for channel in cat.text_channels:
    await channel.delete()
  await interaction.response.send_message("All in-process game has been ended!")

@client.event
async def on_command_error(ctx, error):
  
  
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("You don't have permission to use this command!")


@client.event
async def on_ready():
  print("Snaky is ready!")
  change_status.start()

initial_extensions = []
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    initial_extensions.append("cogs." + filename[:-3])

if __name__ == '__main__':
  for extension in initial_extensions:
    client.load_extension(extension)

client.run(TOKEN)