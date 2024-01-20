import nextcord
from nextcord.ext import commands
import json
from function import *

def rank_define(score):
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


class profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("profile.py is ready!")

    
      
  
    @nextcord.slash_command(name="profile", description="Show your Snaky profile!")
  
    async def profile(self, interaction: nextcord.Interaction):
      checker = await send_permission_error(interaction)
      if checker == "notok":
        return
      set_command_channel_id = read_serverdatasave(interaction.guild.id, "commandchannel_id")
      if set_command_channel_id == None:
        set_command_channel_id = str(interaction.channel.id)
      if set_command_channel_id == str(interaction.channel.id):
        profile_array = read_userdatasave(interaction.user.id,"profile")

        user_score = read_userdatasave(interaction.user.id,"user_score")

        if user_score == None:
          user_score = 0
        
        description_txt = None
        profile_pic = None
        if profile_array == None:
          description_txt = "No description"
          profile_pic = interaction.user.avatar.url
        else:  
          if "description" in profile_array:
            description_txt = profile_array["description"]
          else: 
            description_txt = "No description"
  
        
        
          if "profile_pic" in profile_array:
            profile_pic = profile_array["profile_pic"]
          else:
            profile_pic = interaction.user.avatar.url
        
        rank = rank_define(user_score)

        rebirth = read_userdatasave(interaction.user.id,"rebirth")
        if rebirth == None:
          rebirth = 0
          
        
        profile_embed = nextcord.Embed(title=interaction.user.name + "'s profile", description="Description: " + description_txt,color=nextcord.Color.random(seed=None))    
        profile_embed.set_thumbnail(url=profile_pic)
        profile_embed.add_field(name="Total Score: ", value=str(user_score))

        profile_embed.add_field(name="Rebirth: ", value=str(rebirth))  
        profile_embed.add_field(name="Rank: ", value=rank)
        await interaction.response.send_message(embed=profile_embed)
        return
      else:
        await interaction.response.send_message("This command is not allowed in this channel!",ephemeral=True)
def setup(client):
  client.add_cog(profile(client))