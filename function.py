
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

#SERVERDATASAVE FORMAT
#[CATEGORY_ID_SAVED]

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


    
def write_userdatasave(user_id,sectionname,writevalue):
  with open("userdatasave.json", "r") as f:
      data = json.load(f)

  if not str(user_id) in data:
      data[str(user_id)] = {}
  
  data[str(user_id)][sectionname] = writevalue
  
  with open("userdatasave.json", "w") as f:
      json.dump(data, f, indent=4)
  return

def read_userdatasave(user_id,sectionname):
  with open("userdatasave.json", "r") as f:
    data = json.load(f)

  if str(user_id) in data:
    if sectionname in data[str(user_id)]:
    
      return data[str(user_id)][sectionname]
    else:
      return None
  else:
    return None

def write_serverdatasave(guild_id,sectionname,writevalue):
  with open("serverdatasave.json", "r") as f:
      data = json.load(f)

  if not str(guild_id) in data:
      data[str(guild_id)] = {}
  
  data[str(guild_id)][sectionname] = writevalue
  
  with open("serverdatasave.json", "w") as f:
    
      json.dump(data, f, indent=4)
  return

def read_serverdatasave(guild_id,sectionname):
  with open("serverdatasave.json", "r") as f:
    data = json.load(f)

  if str(guild_id) in data:
    if sectionname in data[str(guild_id)]:
      
      return data[str(guild_id)][sectionname]
    else:
      return None  
  else:
    return None