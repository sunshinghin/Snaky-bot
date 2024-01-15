import nextcord
from nextcord.ext import commands
import json

def get_commandchannel(message):
  with open("commandchannel.json", "r") as f:
    commandchannel = json.load(f)
  if str(message.guild.id) in commandchannel:
    return commandchannel[str(message.guild.id)]
  else:
    return None
def read_highscore(user_id):
  with open("userscore.json", "r") as f:
    highscore = json.load(f)

  
  
  if str(user_id) in highscore:
    
    return highscore[str(user_id)]
  else:
    return "notfound"
def return_rank(score):
  if score < 25:
    return "Starter"
  elif score < 50:
    return "Beginner"
  elif score < 100:
    return "Snaker"
  elif score < 200:
    return "Real Snaker"
  elif score < 500:
    return "Snake Master"  
  elif score < 1000:
    return "Snake God"
  elif score < 2000:
    return "True Snake Man"

class rank(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("rank.py is ready!")


    @nextcord.slash_command(name="rank", description="Show your rank!")
  
    async def rank(self, interaction: nextcord.Interaction):
      set_command_channel_id = get_commandchannel(interaction)
      if set_command_channel_id == None:
        set_command_channel_id = str(interaction.channel.id)
      if set_command_channel_id == str(interaction.channel.id):
        result = read_highscore(interaction.user.id)
        if result == "notfound":
          await interaction.response.send_message("You have not played any games yet!")
        else:
          rank = return_rank(result)
          await interaction.response.send_message("Your rank is: " + rank)
      else:
        await interaction.response.send_message("This command is not allowed in this channel!")
def setup(client):
  client.add_cog(rank(client))