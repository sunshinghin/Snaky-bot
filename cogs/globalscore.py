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
def get_topthree():
  list = []
  dict = None
  with open("userscore.json", "r") as f:
    dict = json.load(f)
  
  first = 0
  firstid = None
  second = 0
  secondid = None
  third = 0
  thirdid = None

  for score in dict:
    if dict[score] > first:
        third = second
        thirdid = secondid
        second = first
        secondid = firstid
        first = dict[score]
        firstid = score
    elif dict[score] > second:
        third = second
        thirdid = secondid
        second = dict[score]
        secondid = score
    elif dict[score] > third:
        third = dict[score]
        thirdid = score
  
  list.append([firstid,first])
  list.append([secondid,second])
  list.append([thirdid,third])
  return list

class globalscore(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("globalscore.py is ready!")


    @nextcord.slash_command(name="globalscore", description="Show top 3 highest score in the world!")
  
    async def globalscore(self, interaction: nextcord.Interaction):
      set_command_channel_id = get_commandchannel(interaction)
      if set_command_channel_id == None:
        set_command_channel_id = str(interaction.channel.id)
      if set_command_channel_id == str(interaction.channel.id):
        score_list = get_topthree()
        score_embed = nextcord.Embed(title="Top 3 highest score in the world!",description="Down below!", color=nextcord.Color.red())
        for i in score_list:
          if i[1] == 0:
            score_embed.add_field(name="No one", value="NO ONE")
          else:
            index = score_list.index(i)
            place = index + 1
            useridshow = i[0]
            user = await self.client.fetch_user(useridshow)
            score_embed.add_field(name=str(place) + " Place: " + user.name,value="Score: " + str(i[1]))
        await interaction.response.send_message(embed=score_embed)
      else:
        await interaction.response.send_message("This command is not allowed in this channel!")
def setup(client):
  client.add_cog(globalscore(client))