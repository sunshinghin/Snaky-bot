import nextcord
from nextcord.ext import commands
import json
from function import *
from nextcord import SlashOption

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

class checkprofile(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("checkprofile.py is ready!")
    @nextcord.slash_command(name="checkprofile", description="Check other user Snaky profile!")
    async def checkprofile(self, interaction: nextcord.Interaction,checkmember: nextcord.Member):
      checker = await send_permission_error(interaction)
      if checker == "notok":
        return
      set_command_channel_id = read_serverdatasave(interaction.guild.id,"commandchannel_id")
      
      if set_command_channel_id == None:
        set_command_channel_id = str(interaction.channel.id)
      if set_command_channel_id == str(interaction.channel.id):

        if checkmember.bot:
          await interaction.response.send_message("You cannot check bot profile!",ephemeral=True)
          return
        
        checkmember_id = checkmember.id
        checkmember_array = read_userdatasave(checkmember_id,"profile")

        profile_pic = None
        description_txt = None
        if checkmember_array == None:
          profile_pic = checkmember.avatar.url
          description_txt = "No description"
        else:
          
          if "profile_pic" in checkmember_array:
            profile_pic = checkmember_array["profile_pic"]
          else:
            profile_pic = checkmember.avater.url

          if "description" in checkmember_array:
            description_txt = checkmember_array["description"]
          else:
            description_txt = "No description"

        user_score = read_userdatasave(checkmember_id,"user_score")
        if user_score == None:
          user_score = 0
            
        rank = rank_define(user_score)

          
          

        rebirth = read_userdatasave(checkmember_id,"rebirth")
        if rebirth == None:
          rebirth = 0

        win = read_userdatasave(checkmember_id,"user_win")
        if win == None:
          win = 0
        
        profile_embed = nextcord.Embed(title=checkmember.name + "'s profile", description="Description: " + description_txt,color=nextcord.Color.random(seed=None))    
        profile_embed.set_thumbnail(url=profile_pic)
        profile_embed.add_field(name="Total Score: ", value=str(user_score))
        profile_embed.add_field(name="Rebirth: ", value=str(rebirth))
        profile_embed.add_field(name="Rank: ", value=rank)

        profile_embed.add_field(name="Win: ", value=str(win))
        
        await interaction.response.send_message(embed=profile_embed)
      else:
        await interaction.response.send_message("This command is not allowed in this channel!",ephemeral=True)
      
def setup(client):
  client.add_cog(checkprofile(client))