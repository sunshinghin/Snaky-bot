import nextcord
import asyncio
import re
from nextcord.ext import commands, tasks
from nextcord import Embed,SlashOption,Interaction
from itertools import cycle
import os
import json
import random
from function import *
DELETE_CHANNEL_TIME = 15
CHANCE_WEAK_SNAKE = 4 #/1


public_id = 0

directionemojis = ["⬆️", "⬇️", "⬅️", "➡"] 

public_ingame_userid = []
invite_userid = []

class deletechannel(nextcord.ui.View):
  
  def __init__(self,snake):
    super().__init__()
    self.snake = snake
    self.wantdelete = False
  @nextcord.ui.button(label="Delete Channel",style=nextcord.ButtonStyle.danger)
  
  async def deletechannel(self,button:nextcord.ui.Button,interaction:Interaction):
    if str(interaction.user.id) == self.snake.create_message_author:
      self.wantdelete = True
    else:
      await interaction.response.send_message("You are not allow to delete this channel.Only the creater of this round can delete this channel!",ephemeral=True)
    self.stop()

class requestbtn(nextcord.ui.View):

  def __init__(self):
    super().__init__()
    self.accept = False
    self.stoptime = False
  @nextcord.ui.button(label="Accept",style=nextcord.ButtonStyle.green)
  
  async def accept(self,button:nextcord.ui.Button,interaction:Interaction):
    self.accept = True
    self.stop()

  @nextcord.ui.button(label="Decline",style=nextcord.ButtonStyle.danger)
  
  async def decline(self,button:nextcord.ui.Button,interaction:Interaction):
    self.accept = False
    self.stoptime = True
    self.stop()

async def countdown(channel,WAIT_TIME,sent_time_embed,snake,hardcore,roundplayerid):

  

  counter = WAIT_TIME

 
  loop = WAIT_TIME + 1
  #while counter > 0:
  for i in range(loop):

    minutesa, secondsa = divmod(counter, 60)
    
    aftimembed = nextcord.Embed(title="State", description=" ", color=nextcord.Color.red())
    aftimembed.add_field(name="⏰Times Left:", value=str(minutesa) + "m " + str(secondsa) + "s")

    aftimembed.add_field(name="Round:",value="<@"+str(roundplayerid)+">")
    
    if hardcore == "y":
      aftimembed.add_field(name="😈Hardcore Mode", value=" ")

    
    
    if snake.lose == False:
    
      new_sent = await sent_time_embed.edit(embed=aftimembed)
    
      sent_time_embed = new_sent

    counter -= 1
    await asyncio.sleep(1)
  
  return


async def sendingembed(map,interaction,first,snake,score,moveemoji,WAIT_TIME,channel,author,hardmode,roundplayerid):
  
  
  if first == True:
    
    send_instr = "<@"+str(snake.firstplayer)+"> :"+snake.firstsnake_char+" \n<@"+str(snake.secondplayer)+"> :"+snake.secondsnake_char
    
    defineembed = nextcord.Embed(title="Instruction", description=send_instr, color=nextcord.Color.red())

    await channel.send(embed=defineembed)
    
    embed_message = nextcord.Embed(title="Snake Game", description="React below to decide where the snake goes!", color=nextcord.Color.red()) 
    embed_message.add_field(name=" ", value=map)
    
    embed_message.add_field(name="Last Move:", value=moveemoji)
    embed_message.add_field(name="Score:", value="Score: "+str(score))
    mention = '<@'+str(author)+'>'
    embed_message.add_field(name="Created by:", value=mention)
    
    minutesb, secondsb = divmod(WAIT_TIME, 60)
    bftimembed = nextcord.Embed(title="State", description=" ", color=nextcord.Color.red())
    bftimembed.add_field(name="⏰Times Left:", value=str(minutesb) + "m " + str(secondsb) + "s")

    bftimembed.add_field(name="Round:", value="<@"+str(roundplayerid)+">")
    
    if hardmode == "y":
      bftimembed.add_field(name="😈Hardcore Mode", value=" ")

    
    sent_time_embed = await channel.send(embed=bftimembed)
   
    sentembed = await channel.send(embed=embed_message)
    
    intermissioncounter = 10

    for i in range(10):
      await asyncio.sleep(1)
      intermissioncounter -= 1
      intermissionembed = nextcord.Embed(title="Intermission:"
,description=str(intermissioncounter) + "s", color=nextcord.Color.red())

      await sent_time_embed.edit(embed=intermissionembed)
      
      

    
    snake.embed_message = sentembed
    
    snake.timer_embed = sent_time_embed

  
  
    for i in directionemojis:
  
      await sentembed.add_reaction(i)
  
    
    await snake.console_game(channel,interaction,WAIT_TIME,sent_time_embed,author,hardmode)

      
  
  elif snake.lose == False:

    
    
    prev_message = snake.embed_message

    if prev_message == None:
      return
    
    newembed = nextcord.Embed(title="Snake Game", description="React below to decide where the snake go!",color=nextcord.Color.red()) 

    
    newembed.add_field(name=" ", value=map)

    newembed.add_field(name="Last Move:", value=moveemoji)
    newembed.add_field(name="Score:", value="Score: "+str(score))
    mention = '<@'+str(author)+'>'
    newembed.add_field(name="Created by:", value=mention)
    
    update = await prev_message.edit(embed=newembed)

      
    for i in directionemojis:

      await update.add_reaction(i)

  


async def getreact(channel,snake,round):


  
  directiontoreturn = None
  await asyncio.sleep(0.2)
  

  msg = None
  if snake.lose == False:
    msg = snake.embed_message
  else:
    return
  
  detectuserid = None
  if round == "first":
    detectuserid = snake.firstplayer
  else:
    detectuserid = snake.secondplayer
    
    
# create variables to save the highest reactions
  func_highest_reaction = ""
  func_highest_reaction_number = 0
  func_highest_reaction_count = 0


  for reaction in msg.reactions: # iterate through every reaction in the message
    detectreaction = reaction.count - 1
    async for user in reaction.users():
      
      if str(user.id) != str(detectuserid):
        if not user.bot:
          print("minus")
          detectreaction -= 1
    
    if detectreaction > func_highest_reaction_number:
    # (reaction.count-1) discounts the bot's reaction
      func_highest_reaction = reaction.emoji
      func_highest_reaction_count = reaction.count-1
  
  selected = False
    
  if func_highest_reaction == "⬆️":
    
    directiontoreturn = "up"

    if round == "first":
      snake.firstplayerevermove = True
    else:
      snake.secondplayerevermove = True
    selected = True
  if func_highest_reaction == "⬇️":
    
    directiontoreturn = "down"

    if round == "first":
      snake.firstplayerevermove = True
    else:
      snake.secondplayerevermove = True
    
    selected = True
  if func_highest_reaction == "⬅️":
    
    directiontoreturn = "left"
    if round == "first":
      snake.firstplayerevermove = True
    else:
      snake.secondplayerevermove = True
    selected = True
  if func_highest_reaction == "➡️":
    
    directiontoreturn = "right"
    if round == "first":
      snake.firstplayerevermove = True
    else:
      snake.secondplayerevermove = True
    selected = True
  
    
  if selected == False:
    
    directiontoreturn = "right"
    
    selected = True
  

  return directiontoreturn





async def lose(snake,channel,winnerid):
  snake.lose = True
  global public_ingame_userid
  global DELETE_CHANNEL_TIME

  evermove = False
  if snake.firstplayerevermove == True and snake.secondplayerevermove == True:
    evermove = True
  
  score = snake.score
  prev_message = snake.timer_embed
  prev_embed = snake.embed_message
  prev_highscore = read_userdatasave(winnerid,"user_score")
  if prev_highscore == None:
    prev_highscore = 0
  write_record = prev_highscore + score
  write_userdatasave(winnerid,"user_score",write_record)
  
  counter = DELETE_CHANNEL_TIME

  server_score = read_serverdatasave(channel.guild.id,"server_score")
  
  if server_score == None:
    server_score = 0

  save_server_score = server_score + score
  write_serverdatasave(channel.guild.id,"server_score",save_server_score)

  win = read_userdatasave(winnerid,"user_win")
  if win == None:
    win = 0
    
  write_win_record = win + 1
  if evermove == True:
    write_userdatasave(winnerid,"user_win",write_win_record)
  
  await prev_embed.clear_reactions()
  view = deletechannel(snake)
  await channel.send(view=view)

  for i in range(DELETE_CHANNEL_TIME):

    await asyncio.sleep(1)
    counter -= 1
    editembed = nextcord.Embed(title="Game Over", description="🏆WINNER: "+"<@"+str(winnerid)+">", color=nextcord.Color.red())

    if evermove == False:
      editembed.add_field(name="You opponent doesn't do a move", value="This game is not counted as a win")

    editembed.add_field(name="Delete channel after: ", value=str(counter)+"s")
    if view.wantdelete == False:
      await prev_message.edit(embed=editembed)
    else:
      public_ingame_userid.remove(str(snake.create_message_author))
      await channel.delete()
      return
  public_ingame_userid.remove(str(snake.create_message_author))

  await channel.delete()
  return

  
class Snake:
  score = 0
  channelforlose = None
  create_message_author = None
  appleingrid = 0
  embed_message_id = None
  timer_embed_id = None
  bombingrid = 0
  lose = False
  point_add = 1
  firstplayer = None
  secondplayer = None
  firstplayerevermove = False
  secondplayerevermove = False
  def __init__(self, grid_size, empty_char='⬜', snake_char='🫥', tail_char='🟨'):
      
      self.running = None  # for console running
      self.grid = [[empty_char for y in range(grid_size)] for i in range(grid_size)]  # snake grid
      self.grid_size = grid_size
      self.firstsnake_char = "😈"
      self.secondsnake_char = "😡"
      self.firsttail_char = "🟪"
      self.secondtail_char = "🟥"
      self.empty_char = empty_char
      self.firstturns = 0
      self.secondturns = 0
      self.maxbomb = random.randint(5,10)
      row = int(len(self.grid) / 2)
      self.firstsnake_pos = [row, row]
      self.secondsnake_pos = [row-1, row]
      self.apples = 0
      self.firsttail_positions = []
      self.secondtail_positions = []
      self.firstlast_move = (0, 0)
      self.secondlast_move = (0, 0)
  
  
  async def load_grid(self,channel,input,WAIT_TIME,round):
      """
      Function to load the grid in the console via print
      """
      
      
    
      map = None
      maparray = []
      for x in self.grid:
          print_list = []
          for y in x:
              print_list.append(y)
          
  
  
          map = "".join(print_list)
          maparray.append(map)
  
      if channel != None:
       

        send_emoji = None
        if input == "up":
          send_emoji = "⬆️"
        elif input == "down":
          send_emoji = "⬇️"
        elif input == "left":
          send_emoji = "⬅️"
        elif input == "right":
          send_emoji = "➡"

        send_id = None
        if round == "first":
          send_id = self.firstplayer
        else:
          send_id = self.secondplayer
        
        await sendingembed("\n".join(maparray),channel,False,self,self.score,send_emoji,WAIT_TIME,channel,self.create_message_author,None,send_id)       
  
  
  
  
  
  
  def return_grid(self) -> str:
      """
      Function to return the grid in a format that's readable
      """
      end_return = []
      for x in self.grid:
          row_list = []
          for y in x:
              row_list.append(y)
          end_return.append("".join(row_list))
      return "\n".join(end_return)
  
  def start(self):
      """
      Start the snake game by creating the snake
      """
      
      self.grid[self.firstsnake_pos[0]][self.firstsnake_pos[1]] = self.firstsnake_char

      self.grid[self.secondsnake_pos[0]][self.secondsnake_pos[1]] = self.secondsnake_char
  
  async def console_game(self,channel,interaction,WAIT_TIME,sent_time_embed,author,hardmode):

      
      self.create_message_author = author
    
      self.channelforlose = channel
      self.running = True
      controls = {
          'up': self.move_up,
          'down': self.move_down,
          'left': self.move_left,
          'right': self.move_right,
          'exit': lambda: 'stop',
      }
     
      round = "first"
      
      while self.running:
          send_id = None
          if round == "first":
            send_id = self.firstplayer
          else:
            send_id = self.secondplayer
        
          await countdown(channel,WAIT_TIME,sent_time_embed,self,hardmode,send_id)
          
          user_input = await getreact(channel,self,round)
          if user_input in controls.keys():
              
              controls_output = await controls[user_input](round)
                               
              if controls_output == 'stop':
                return
              
              if self.appleingrid < 7:
                self.spawn_apple()
              
              
              self.tail_handle(round)
              if round == "first":
                round = "second"
              else:
                round = "first"
              await self.load_grid(channel,user_input,WAIT_TIME,round)
              
          else:
              return
  # --- Snake Movements ---
  
  async def check_move(self, x_off, y_off,round) -> True | False:
      if round == "first":
        x = self.firstsnake_pos[1] + x_off 
    
        y = self.firstsnake_pos[0] + y_off
        if x >= self.grid_size or x < 0:
          
          await lose(self,self.channelforlose,self.secondplayer)
          
          return True
          
            # snake died GG ez
        if y >= self.grid_size or y < 0:
            
          await lose(self, self.channelforlose,self.secondplayer)
          return True
            
            # snake died GG ez
      
  
        if self.grid[y][x] == '🍎':
            
            self.apples += 1
            self.score += self.point_add
            self.appleingrid -= 1
        if self.grid[y][x] == '💣':
          
            await lose(self, self.channelforlose,self.secondplayer)
            return True
          
        if self.grid[y][x] == self.firsttail_char:
          
            
          await lose(self,self.channelforlose,self.secondplayer)
        
          return True

        if self.grid[y][x] == self.secondtail_char:
          
            
          await lose(self,self.channelforlose,self.secondplayer)
        
          return True

        if self.grid[y][x] == self.secondsnake_char:
          
            
          await lose(self,self.channelforlose,self.secondplayer)
        
          return True
        
        self.firstturns += 1
        return False
      else:
        x = self.secondsnake_pos[1] + x_off 
    
        y = self.secondsnake_pos[0] + y_off
        if x >= self.grid_size or x < 0:
          
          await lose(self,self.channelforlose,self.firstplayer)
          
          return True
          
            # snake died GG ez
        if y >= self.grid_size or y < 0:
            
            await lose(self, self.channelforlose,self.firstplayer)
            return True
            
            # snake died GG ez
      
  
        if self.grid[y][x] == '🍎':
            
            self.apples += 1
            self.score += self.point_add
            self.appleingrid -= 1
        if self.grid[y][x] == '💣':
          
            await lose(self, self.channelforlose,self.firstplayer)
            return True
          
        if self.grid[y][x] == self.secondtail_char:
          
            await lose(self,self.channelforlose,self.firstplayer)
        
            return True

        if self.grid[y][x] == self.firsttail_char:
          
            await lose(self,self.channelforlose,self.firstplayer)
        
            return True

        if self.grid[y][x] == self.firstsnake_char:
          
            await lose(self,self.channelforlose,self.firstplayer)
        
            return True
        
        self.secondturns += 1
        return False

  
  async def move_right(self,round):  # move snake right
      result = await self.check_move(1, 0,round)
      print(result)
      if round == "first":
        if result == True:
            self.running = False
            return
        
        self.grid[self.firstsnake_pos[0]][self.firstsnake_pos[1]] = self.empty_char  # remove snake from grid
        self.grid[self.firstsnake_pos[0]][self.firstsnake_pos[1] + 1] = self.firstsnake_char  # re-add snake in new position
        self.firstsnake_pos = [self.firstsnake_pos[0], self.firstsnake_pos[1] + 1]
        
        return 0, 1
      else:
        
        if result == True:
            self.running = False
            return
        
        
        self.grid[self.secondsnake_pos[0]][self.secondsnake_pos[1]] = self.empty_char  # remove snake from grid
        
        self.grid[self.secondsnake_pos[0]][self.secondsnake_pos[1] + 1] = self.secondsnake_char  # re-add snake in new position
        self.secondsnake_pos = [self.secondsnake_pos[0], self.secondsnake_pos[1] + 1]
        return 0, 1
                  
  async def move_left(self,round):  # move snake left
      result = await self.check_move(-1,0,round)
      if round == "first":
        if result == True:
            self.running = False
            return
        
        self.grid[self.firstsnake_pos[0]][self.firstsnake_pos[1]] = self.empty_char  # remove snake from grid
        self.grid[self.firstsnake_pos[0]][self.firstsnake_pos[1] - 1] = self.firstsnake_char  # re-add snake in new position
        self.firstsnake_pos = [self.firstsnake_pos[0], self.firstsnake_pos[1] - 1]
        return 0, -1
      else:
        if result == True:
            self.running = False
            return
        
        self.grid[self.secondsnake_pos[0]][self.secondsnake_pos[1]] = self.empty_char  # remove snake from grid
        self.grid[self.secondsnake_pos[0]][self.secondsnake_pos[1] - 1] = self.secondsnake_char  # re-add snake in new position
        self.secondsnake_pos = [self.secondsnake_pos[0], self.secondsnake_pos[1] - 1]
        return 0, -1
        
  async def move_down(self,round):  # move snake down
      result = await self.check_move(0, 1,round)
      if round == "first":
        if result == True:
            self.running = False
            return
        
        self.grid[self.firstsnake_pos[0]][self.firstsnake_pos[1]] = self.empty_char  # remove snake from grid
        self.grid[self.firstsnake_pos[0] + 1][self.firstsnake_pos[1]] = self.firstsnake_char  # re-add snake in new position
        self.firstsnake_pos = [self.firstsnake_pos[0] + 1, self.firstsnake_pos[1]]
        return 1, 0
      else:
        if result == True:
            self.running = False
            return
        
        self.grid[self.secondsnake_pos[0]][self.secondsnake_pos[1]] = self.empty_char  # remove snake from grid
        self.grid[self.secondsnake_pos[0] + 1][self.secondsnake_pos[1]] = self.secondsnake_char  # re-add snake in new position
        self.secondsnake_pos = [self.secondsnake_pos[0] + 1, self.secondsnake_pos[1]]
        return 1, 0
  
  async def move_up(self,round):  # move snake up
      result = await self.check_move(0, -1,round)
      if round == "first":
        if result == True:
            self.running = False
            return
        
        self.grid[self.firstsnake_pos[0]][self.firstsnake_pos[1]] = self.empty_char  # remove snake from grid
        self.grid[self.firstsnake_pos[0] - 1][self.firstsnake_pos[1]] = self.firstsnake_char  # re-add snake in new position
        self.firstsnake_pos = [self.firstsnake_pos[0] - 1, self.firstsnake_pos[1]]
        return -1,0
      else:
        if result == True:
            self.running = False
            return
        
        self.grid[self.secondsnake_pos[0]][self.secondsnake_pos[1]] = self.empty_char  # remove snake from grid
        self.grid[self.secondsnake_pos[0] - 1][self.secondsnake_pos[1]] = self.secondsnake_char  # re-add snake in new position
        self.secondsnake_pos = [self.secondsnake_pos[0] - 1, self.secondsnake_pos[1]]
        return -1, 0
  
  def spawn_bomb(self):
      spawn_points = []
      for x in range(self.grid_size):
          for y in range(self.grid_size):
              if self.grid[x][y] != self.firstsnake_char and self.grid[x][y] != self.firsttail_char and self.grid[x][y] != '💣' and self.secondsnake_char and self.grid[x][y] != self.secondtail_char and self.grid[x][y] != '💣':
                  spawn_points.append([x, y])
      random_choice = 0
      try:
          random_choice = random.randint(0, len(spawn_points) - 1)
      except ValueError:
          pass
      try:
          self.bombingrid += 1
          self.grid[spawn_points[random_choice][0]][spawn_points[random_choice][1]] = '💣'
        
      except IndexError:
          pass


  def spawn_apple(self):
      spawn_points = []
      for x in range(self.grid_size):
          for y in range(self.grid_size):
              if self.grid[x][y] != self.firstsnake_char and self.grid[x][y] != self.firsttail_char and self.grid[x][y] != '🍎' and self.secondsnake_char and self.grid[x][y] != self.secondtail_char and self.grid[x][y] != '🍎':
                  spawn_points.append([x, y])
      random_choice = 0
      try:
          random_choice = random.randint(0, len(spawn_points) - 1)
      except ValueError:
          pass
      try:
          self.appleingrid += 1
          self.grid[spawn_points[random_choice][0]][spawn_points[random_choice][1]] = '🍎'
        
      except IndexError:
          pass
  
  def tail_handle(self,round):
    if round == "first":
      if self.apples > 0:
          self.firsttail_positions.append(self.firstsnake_pos.copy())  # the copy is important
          for pos in self.firsttail_positions:
              if pos != self.firstsnake_pos:
                  self.grid[pos[0]][pos[1]] = self.firsttail_char
  
          
          if self.apples < len(self.firsttail_positions) - 1:
              if self.firsttail_positions[0] != self.firstsnake_pos:
                  self.grid[self.firsttail_positions[0][0]][
                      self.firsttail_positions[0][1]] = self.empty_char  # replace end tail with empty char
                  self.firsttail_positions.pop(0)
    else:
      if self.apples > 0:
          self.secondtail_positions.append(self.secondsnake_pos.copy())  # the copy is important
          for pos in self.secondtail_positions:
              if pos != self.secondsnake_pos:
                  self.grid[pos[0]][pos[1]] = self.secondtail_char
  
          
          if self.apples < len(self.secondtail_positions) - 1:
              if self.secondtail_positions[0] != self.secondsnake_pos:
                  self.grid[self.secondtail_positions[0][0]][
                      self.secondtail_positions[0][1]] = self.empty_char  # replace end tail with empty char
                  self.secondtail_positions.pop(0)
                
class pvp(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('pvpsnake.py is ready!')

  
  @nextcord.slash_command(name="snakepvp",description="Start a snake game!")
  
  
  async def playsnake(self, interaction: Interaction,pvpuser: nextcord.Member,size: int = SlashOption(max_value=12,min_value=1,default=12,required=False),waittime: int = SlashOption(max_value=86400,min_value=1,default=2,required=False),hardmode: str = SlashOption(name="hardcore",choices=["y","n"],default="n",required=False)):
    checker = await send_permission_error(interaction)
    if checker == "notok":
      return
    
    set_command_channel_id = read_serverdatasave(interaction.guild.id,"commandchannel_id")
    if set_command_channel_id == None:
      set_command_channel_id = str(interaction.channel.id)
    
    if set_command_channel_id == str(interaction.channel.id):
      newinv = {}
      global public_id
      global public_ingame_userid
      global invite_userid
      catelog_id = read_serverdatasave(interaction.guild.id,"category_id")
      user_rebirth = read_userdatasave(interaction.user.id,"rebirth")
      if str(interaction.user.id) == str(pvpuser.id):
        await interaction.response.send_message("You can't play against yourself!",ephemeral=True)
        return
      if pvpuser.bot:
        await interaction.response.send_message("You can't play against a bot!",ephemeral=True)
        return
      
      if user_rebirth == None:
        user_rebirth = 0

      if user_rebirth < 1 and hardmode == "y":
        await interaction.response.send_message("You need to rebirth at least once to play hardcore mode!",ephemeral=True)
        return
      
      
      if catelog_id == None:
        await interaction.response.send_message("This server has not set up Snaky yet!",ephemeral=True)
        return


      
      user_started_game = False
       
      for i in public_ingame_userid:
        if i == str(interaction.user.id):
          user_started_game = True    
      
    

          
      if user_started_game == True:
        await interaction.response.send_message("You are already create a game!Cannot create new anymore!",ephemeral=True)
        
        return
      else:

        
        await interaction.response.send_message("You have sent a pvp request! Please wait for the opponent response!",ephemeral=True)

        if str(interaction.user.id) in invite_userid:
          await interaction.response.send_message("You have already sent a pvp request!",ephemeral=True)
          return

        invite_userid.insert(0,str(interaction.user.id))
        
        dmchannel = pvpuser.dm_channel
        if dmchannel == None:
          await pvpuser.create_dm()
          dmchannel = pvpuser.dm_channel
        async for message in dmchannel.history(limit=None):
          if message.author == self.client.user:
            if message.embeds:
              if message.embeds[0].title == "Declined":
                await message.delete()
                break

        
        requestview = requestbtn()

        requestembed = nextcord.Embed(title="Pvp request",description=interaction.user.name + " from " + interaction.guild.name + "has sent you a pvp request!")

        requestembed.add_field(name="Accept time:",value="50s")
        edit_msg = None
        edit_msg = await pvpuser.send(embed=requestembed,view=requestview)
        
        
        acceptcounter = 50
        
        for i in range(50):
          await asyncio.sleep(1)
          acceptcounter -= 1
          if requestview.stoptime == True or requestview.accept == True:
            break
          
          requestupt = nextcord.Embed(title="Pvp request",description=interaction.user.name + " from " + interaction.guild.name +"has sent you a pvp request!")

          requestupt.add_field(name="Accept time:",value=str(acceptcounter) + "s")

          await edit_msg.edit(embed=requestupt,view=requestview)
          
          
        usertag = "<@"+str(interaction.user.id)+">"
        if requestview.accept == False:
        
          declineembed = nextcord.Embed(title="Declined",description="You have declined the pvp request!",color=nextcord.Color.red())

          await edit_msg.edit(embed=declineembed,view=None)
          await interaction.channel.send(usertag+"The opponent decline your pvp request!")
          
          return
        await asyncio.sleep(3)
        public_id += 1
        arg = "pvp-game-" + str(public_id)
        
        overwrites = {
    interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
    interaction.user: nextcord.PermissionOverwrite(read_messages=True),
    pvpuser: nextcord.PermissionOverwrite(read_messages=True),
    self.client.user: nextcord.PermissionOverwrite(read_messages=True)
        }
        channel = await interaction.guild.create_text_channel(name=arg,category = self.client.get_channel(int(catelog_id)),overwrites=overwrites)
          
        successembed = nextcord.Embed(title="Success",description="You have accepted the pvp request!",color=nextcord.Color.green())
        invite = await channel.create_invite(reason="Your pvp game",max_age=0,max_uses=1, temporary=False,unique=True)

        successembed.add_field(name="Pvp channel(click here):",value=invite)
        
        await edit_msg.edit(embed=successembed,view=None)
        await interaction.channel.send(usertag+"The opponent accept your pvp request! Your pvp game created! Pvp channel: " + "<#"+str(channel.id)+">")

        invite_userid.remove(str(interaction.user.id))
        
        snake = Snake(size, '⬛')
        
        
        snake.start()

        snake.firstplayer = str(interaction.user.id)
        snake.secondplayer = str(pvpuser.id)
        public_ingame_userid.append(str(interaction.user.id))
        tag = "<#"+str(channel.id)+">"
        playerstag = "<@"+str(interaction.user.id)+"> Vs <@"+str(pvpuser.id)+">"
        
        await sendingembed(snake.return_grid(),interaction,True,snake,0,"🚫",waittime,channel,str(interaction.user.id),hardmode,snake.firstplayer)
    else:
      await interaction.response.send_message("You cannot use Snaky command here!",ephemeral=True)
    
      

def setup(client):
  client.add_cog(pvp(client))