import nextcord
from nextcord.ext import commands
import json
from function import *

def read_highscore(user_id):
  with open("userscore.json", "r") as f:
    highscore = json.load(f)

  
  
  if str(user_id) in highscore:
    
    return highscore[str(user_id)]
  else:
    return "notfound"


class score(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("score.py is ready!")


    @nextcord.slash_command(name="score", description="Show your total score!")
  
    async def score(self, interaction: nextcord.Interaction):
      checker = await send_permission_error(interaction)
      if checker == "notok":
        return
      set_command_channel_id = get_commandchannel(interaction)
      if set_command_channel_id == None:
        set_command_channel_id = str(interaction.channel.id)
      if set_command_channel_id == str(interaction.channel.id):
        result = read_highscore(interaction.user.id)
        if result == "notfound":
          await interaction.response.send_message("You have not played any games yet!",ephemeral=True)
        else:
          await interaction.response.send_message("Your score is: " + str(result))
      else:
        await interaction.response.send_message("This command is not allowed in this channel!",ephemeral=True)
def setup(client):
  client.add_cog(score(client))