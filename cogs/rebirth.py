import nextcord
from nextcord.ext import commands
import json
from function import *

class rebirthbtn(nextcord.ui.View):
  
  def __init__(self,cost,mainclass):
    super().__init__()
    self.cost = cost
    self.mainclass = mainclass
  @nextcord.ui.button(label="Rebirth!",style=nextcord.ButtonStyle.danger)
  
  async def confirmrebirth(self,button:nextcord.ui.Button,interaction:Interaction):

    total_score = read_userdatasave(interaction.user.id,"user_score")
    save_rebirth = None
    if total_score == None:
      total_score = 0

    if total_score >= self.cost:
      prev_rebirth = read_serverdatasave(interaction.guild.id,"rebirth")
      if prev_rebirth == None:
        prev_rebirth = 0

      save_rebirth = prev_rebirth + 1
      write_userdatasave(interaction.user.id,"rebirth",save_rebirth)
      write_userdatasave(interaction.user.id,"rebirth_cost",self.cost * 1.2)

      write_userdatasave(interaction.user.id,"user_score",0)
      user_tag = "<@"+str(interaction.user.id)+">"
    
      await interaction.channel.send(user_tag+" JUST REBIRTHED!("+str(save_rebirth)+" REBIRTH)"+" CONGRATE!!")
      success_msg = nextcord.Embed(title="Success!",description="You have successfully rebirthed! Congrate!",color=nextcord.Color.green())
      await self.mainclass.sent_msg.edit(embed=success_msg,view=None)

    
    else:

      error_msg = nextcord.Embed(title="Error!",description="You don't have enough score to rebirth!",color=nextcord.Color.red())
      
      await self.mainclass.sent_msg.edit(embed=error_msg,view=None)
    self.stop()


class rebirth(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.sent_msg = None
    @commands.Cog.listener()
    async def on_ready(self):
        print("rebirth.py is ready!")


    @nextcord.slash_command(name="rebirth", description="Rebirth?")
  
    async def rebirth(self, interaction: nextcord.Interaction):
      checker = await send_permission_error(interaction)
      if checker == "notok":
        return
      set_command_channel_id = read_serverdatasave(interaction.guild.id,"commandchannel_id")
      if set_command_channel_id == None:
        set_command_channel_id = str(interaction.channel.id)
      if set_command_channel_id == str(interaction.channel.id):
        
        confirm_embed = nextcord.Embed(title="Rebirth?",description="Are you sure you want to rebirth? This will reset your total score and rank but you will have one rebirth score.", color=nextcord.Color.red())
        user_cost = read_userdatasave(interaction.user.id,"rebirth_cost")
        if user_cost == None:
          user_cost = 450
        view = rebirthbtn(user_cost,self)

        confirm_embed.add_field(name="Rebirth Requirement:",value=str(user_cost) + " scores")
        confirm_embed.add_field(name="Click the button below to confirm" ,value=" ")
        self.sent_msg = await interaction.response.send_message(embed=confirm_embed,view=view,ephemeral=True)
      else:
        await interaction.response.send_message("This command is not allowed in this channel!",ephemeral=True)
def setup(client):
  client.add_cog(rebirth(client))