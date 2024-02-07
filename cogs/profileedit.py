import nextcord
from nextcord.ext import commands
import json
from function import *
from nextcord import SlashOption
import validators

class profileedit(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("profileedit.py is ready!")
    @nextcord.slash_command(name="profileedit", description="Edit your Snaky profile!")
    async def profileedit(self, interaction: nextcord.Interaction,profilepictureurl: str = SlashOption(required=False,default=None), description: str = SlashOption(required=False,default=None)):
      checker = await send_permission_error(interaction)
      if checker == "notok":
        return
      set_command_channel_id = read_serverdatasave(interaction.guild.id,"commandchannel_id")
      
      if set_command_channel_id == None:
        set_command_channel_id = str(interaction.channel.id)
      if set_command_channel_id == str(interaction.channel.id):
        user_profile_pic = None
        description_txt = None

        array = read_userdatasave(interaction.user.id,"profile")
        
        if profilepictureurl == None:

          if array == None:
            user_profile_pic = interaction.user.avatar.url
          else:
            if "profile_pic" in array:
              
              user_profile_pic = array["profile_pic"]
            else:
              user_profile_pic = interaction.user.avatar.url
        else:
          if profilepictureurl == ":defaultprofile:":
            user_profile_pic = interaction.user.avatar.url
          else:
            valid = validators.url(profilepictureurl)
            if valid:
              user_profile_pic = profilepictureurl
            else:
              await interaction.response.send_message("The profile picture url is not valid!",ephemeral=True)
              return
          
        if description == None:
          if array == None:
            description_txt = "No description set!"
          else:
            if "description" in array:
              description_txt = array["description"]
            else:
              description_txt = "No description"
        else:
          
          description_txt = description    
        write_userdatasave(interaction.user.id,"profile",{"profile_pic": user_profile_pic,"description": description_txt})

        await interaction.response.send_message("Your profile has been edited!",ephemeral=True)
      
      else:
        await interaction.response.send_message("This command is not allowed in this channel!",ephemeral=True)
      
def setup(client):
  client.add_cog(profileedit(client))