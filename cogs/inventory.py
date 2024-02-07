import nextcord
from nextcord.ext import commands
import json
from function import *


class inventory(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("inventory.py is ready!")


    @nextcord.slash_command(name="inventory", description="Show your inventory!")
  
    async def inventory(self, interaction: nextcord.Interaction):
      checker = await send_permission_error(interaction)
      if checker == "notok":
        return
      set_command_channel_id = read_serverdatasave(interaction.guild.id,"commandchannel_id")
      if set_command_channel_id == None:
        set_command_channel_id = str(interaction.channel.id)
      if set_command_channel_id == str(interaction.channel.id):
        inv_embed = nextcord.Embed(title="Inventory", description="Check your stuffs!",color=nextcord.Color.red())
        inv = read_userdatasave(interaction.user.id,"inventory")
        if inv == None:
          inv = {}
        user_extra_life = None
        if "user_extralife" in inv:
          user_extra_life = inv["user_extralife"]
        else:
          user_extra_life = 0
        user_doublescore = None
        if "user_doublescore" in inv:
          user_doublescore = inv["user_doublescore"]
        else:
          user_doublescore = 0
        inv_embed.add_field(name="Extra life:", value=str(user_extra_life))

        inv_embed.add_field(name="Double score:", value=str(user_doublescore))
        await interaction.response.send_message(embed=inv_embed,ephemeral=True)
      
      else:
        await interaction.response.send_message("This command is not allowed in this channel!",ephemeral=True)
def setup(client):
  client.add_cog(inventory(client))