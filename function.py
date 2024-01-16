
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
permissionscheck = ["send_messages","manage_messages","manage_channels","manage_guild","embed_links","attach_files","add_reactions","external_emojis","external_stickers","read_message_history","use_slash_commands","read_messages"]
#Main function
async def send_permission_error(ctx):
  
  list_to_return = []
  perm_list = [perm[0] for perm in ctx.guild.me.guild_permissions if perm[1]]

  for checkperm in permissionscheck:
    perm_contain = False
    for perm in perm_list:
      if perm == checkperm:
        perm_contain = True
    if perm_contain == False:
      list_to_return.append(checkperm)
  
  
  iserror = False
  for i in list_to_return:
    iserror = True
  if iserror == True:
    error_embed = nextcord.Embed(title="Missing Permissions",description="Snaky is missing some required permission here: ")
    for missperm in list_to_return:
        error_embed.add_field(name=missperm,value="")

    await ctx.response.send_message(embed=error_embed)
  
    return "notok"

  else:
    return "ok"

def server_catelog(message):
  with open("catelog.json", "r") as f:
    channel = json.load(f)
  if str(message.guild.id) in channel:
    return channel[str(message.guild.id)]
  else:
    return None
def get_commandchannel(message):
  
  with open("commandchannel.json", "r") as f:
    commandchannel = json.load(f)
 
  if str(message.guild.id) in commandchannel:
    return commandchannel[str(message.guild.id)]
  else:
    return None