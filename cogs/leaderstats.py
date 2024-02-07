import nextcord
from nextcord.ext import commands
import json
from function import *

def get_topthree(leaderstat):
  setting = None
  if leaderstat == "Personal score leaderboard":
    setting = {
      "file": "userdatasave.json",
      "class": "user_score",
      "title": "Top 3 highest score in the world(Personal)",
      "showing": "Score:"
    }
  if leaderstat == "Server score leaderboard":
    setting = {
      "file": "serverdatasave.json",
               "class": "server_score",
               "title": "Top 3 highest score in the world(Server)",
      "showing": "Score:"
              }
  if leaderstat == "Rebirth leaderboard":
    setting = {
      "file": "userdatasave.json",
               "class": "rebirth",
               "title": "Top 3 highest rebirth in the world(Personal)",
      "showing": "Rebirth:"
    }
  list = []
  dict = None
  with open(setting["file"], "r") as f:
    dict = json.load(f)
  
  first = 0
  firstid = None
  second = 0
  secondid = None
  third = 0
  thirdid = None

  for score in dict:
    if setting["class"] not in dict[score]:
      continue
    
    if dict[score][setting["class"]] > first:
        third = second
        thirdid = secondid
        second = first
        secondid = firstid
        first = dict[score][setting["class"]]
        firstid = score
    elif dict[score][setting["class"]] > second:
        third = second
        thirdid = secondid
        second = dict[score][setting["class"]]
        secondid = score
    elif dict[score][setting["class"]] > third:
        third = dict[score][setting["class"]]
        thirdid = score
  
  list.append([firstid,first])
  list.append([secondid,second])
  list.append([thirdid,third])
  return [list,setting["title"],setting["showing"]]

class leaderstats(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("leaderstats.py is ready!")


    @nextcord.slash_command(name="leaderstats", description="Show Snaky's leaderboard")
  
    async def leaderstats(self, interaction: nextcord.Interaction,leaderboard: str = SlashOption(choices=["Personal score leaderboard","Server score leaderboard","Rebirth leaderboard"], required=True)):
      checker = await send_permission_error(interaction)
      if checker == "notok":
        return
      set_command_channel_id = read_serverdatasave(interaction.guild.id,"commandchannel_id")
      if set_command_channel_id == None:
        set_command_channel_id = str(interaction.channel.id)
      if set_command_channel_id == str(interaction.channel.id):
        
        returnlist = get_topthree(leaderboard)
        score_list = returnlist[0]
        titleembed = returnlist[1]
        showing = returnlist[2]
        score_embed = nextcord.Embed(title=titleembed,description="Down below!", color=nextcord.Color.red())

        place = None
        user = None
        
        for i in score_list:
          if i[1] == 0:
            score_embed.add_field(name="NO ONE", value="NO ONE")
          else:
            index = score_list.index(i)
            place = index + 1
            useridshow = i[0]
            score = i[1]
            if leaderboard == "Personal score leaderboard" or leaderboard == "Rebirth leaderboard":
              shearchuser = await self.client.fetch_user(useridshow)
              user = shearchuser.name
            else:
              
              
            
              channel = await self.client.fetch_guild(int(useridshow))
              if channel == None:
                user = "NO ONE"
                score = "NO ONE"
              else: 
                user = channel.name

              
            score_embed.add_field(name=str(place) + " Place: " + user,value=showing + str(score)) 
        await interaction.response.send_message(embed=score_embed)
      else:
        await interaction.response.send_message("This command is not allowed in this channel!",ephemeral=True)
def setup(client):
  client.add_cog(leaderstats(client))
