import nextcord
from nextcord.ext import commands
import json
from function import *

EXTRA_LIFE_PRICE = 87
DOUBLE_SCORE_PRICE = 121

def final_write_data(datas,userid):
  #write new var everytime you create a power-up
  inv = read_userdatasave(userid,"inventory")
  if inv == None:
    inv = {}
  power_up_cls = {"user_extralife": None,"user_doublescore": None}
 
    
  
  for key in datas:
    if key in power_up_cls:
      power_up_cls[key] = datas[key]
  
  for key in power_up_cls:
    if power_up_cls[key] == None:
      if key in inv:
        original_data = inv[key]
      else:
        original_data = 0
      power_up_cls[key] = original_data
      
  write_userdatasave(userid,"inventory",power_up_cls)
  return

async def buyprocess(interaction,self,currency,price,buyitem):
  inventory = read_userdatasave(interaction.user.id,"inventory")
  if inventory == None:
    inventory = {}
  usertotalscore = read_userdatasave(interaction.user.id,currency)

  error_embed = nextcord.Embed(title="Error!",description="You don't have enough scores to buy this item.",color=nextcord.Color.red())

  success_embed = nextcord.Embed(title="Success!",description="You have successfully bought this item.",color=nextcord.Color.green())
    
  if usertotalscore == None:
    usertotalscore = 0
  if usertotalscore >= price:
    save_totalscore = usertotalscore - price
    write_userdatasave(interaction.user.id,currency,save_totalscore)
    extralife = None
    if buyitem in inventory:
      extralife = inventory[buyitem]
    else:
      extralife = 0
    save_extralife = extralife + 1
      
    final_write_data({buyitem: save_extralife},interaction.user.id)
      
    await self.mainclass.sent_msg.edit(embed=success_embed,view=None)
      
      
  else:
      
    await self.mainclass.sent_msg.edit(embed=error_embed,view=None)
  return


class buybtn(nextcord.ui.View):
  
  def __init__(self,mainclass):
    super().__init__()
    self.mainclass = mainclass
  
  @nextcord.ui.button(label="Extra Life("+str(EXTRA_LIFE_PRICE)+"scores)",style=nextcord.ButtonStyle.danger)
  
  async def extralife(self,button:nextcord.ui.Button,interaction:Interaction):

    await buyprocess(interaction,self,"user_score",EXTRA_LIFE_PRICE,"user_extralife")
      
    self.stop()
  @nextcord.ui.button(label="Double score("+str(DOUBLE_SCORE_PRICE)+"scores)",style=nextcord.ButtonStyle.danger)
  
  async def doublescore(self,button:nextcord.ui.Button,interaction:Interaction):

    await buyprocess(interaction,self,"user_score",DOUBLE_SCORE_PRICE,"user_doublescore")
      
    self.stop()

class shop(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.sent_msg = None
    @commands.Cog.listener()
    async def on_ready(self):
        print("shop.py is ready!")


    @nextcord.slash_command(name="shop", description="Open the shop ui")
  
    async def shop(self, interaction: nextcord.Interaction):
      checker = await send_permission_error(interaction)
      if checker == "notok":
        return
      set_command_channel_id = read_serverdatasave(interaction.guild.id,"commandchannel_id")
      if set_command_channel_id == None:
        set_command_channel_id = str(interaction.channel.id)
      if set_command_channel_id == str(interaction.channel.id):
        view = buybtn(self)
        user_score = read_userdatasave(interaction.user.id,"user_score")
        shop_embed = nextcord.Embed(title="Shop",description="Welcome to the shop! Here you can buy items to help you in the game!The item you buy will save in your inventory.Click the button to buy an item!",color=nextcord.Color.red())
        shop_embed.add_field(name="Your scores:",value=str(user_score))
        sent = await interaction.response.send_message(embed=shop_embed,view=view,ephemeral=True)
        self.sent_msg = sent
      else:
        await interaction.response.send_message("This command is not allowed in this channel!",ephemeral=True)
def setup(client):
  client.add_cog(shop(client))