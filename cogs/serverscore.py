import nextcord
from nextcord.ext import commands
import json
from function import *
def get_commandchannel(message):
  with open("commandchannel.json", "r") as f:
    commandchannel = json.load(f)
  if str(message.guild.id) in commandchannel:
    return commandchannel[str(message.guild.id)]
  else:
    return None
    
def read_highscore(user_id):
  with open("serverscore.json", "r") as f:
    highscore = json.load(f)

  
  
  if str(user_id) in highscore:
    
    return highscore[str(user_id)]
  else:
    return "notfound"


class serverscore(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("serverscore.py is ready!")


    @nextcord.slash_command(name="serverscore", description="Show the server highest total score!")
  
    async def serverscore(self, interaction: nextcord.Interaction):
      checker = await send_permission_error(interaction)
      if checker == "notok":
        return
      set_command_channel_id = get_commandchannel(interaction)
      
      if set_command_channel_id == None:
        set_command_channel_id = str(interaction.channel.id)
      if set_command_channel_id == str(interaction.channel.id):
        result = read_highscore(interaction.guild.id)
        if result == "notfound":
          await interaction.response.send_message("This server hasn't play any game yet!",ephemeral=True)
        else:
          await interaction.response.send_message("The server highest score is: " + str(result))
      else:
        await interaction.response.send_message("This command is not allowed in this channel!",ephemeral=True)
def setup(client):
  client.add_cog(serverscore(client))