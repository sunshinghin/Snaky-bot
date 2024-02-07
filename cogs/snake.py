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

directionemojis = ["⬆️", "⬇️", "⬅️", "➡","🛑"] 

public_ingame_userid = []
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
  
async def countdown(channel,WAIT_TIME,sent_time_embed,snake,hardcore,chaos):

  

  counter = WAIT_TIME

 
  loop = WAIT_TIME + 1
  #while counter > 0:
  for i in range(loop):

    minutesa, secondsa = divmod(counter, 60)
    
    aftimembed = nextcord.Embed(title="State", description=" ", color=nextcord.Color.red())
    aftimembed.add_field(name="⏰Times Left:", value=str(minutesa) + "m " + str(secondsa) + "s")

    if hardcore == "y":
      aftimembed.add_field(name="😈Hardcore Mode", value=" ")

    if chaos == "y":
      aftimembed.add_field(name="😵‍💫Chaos Mode", value=" ")

    if snake.extra_life == True:
      aftimembed.add_field(name="Extra life", value=" ")

    if snake.double_score == True:
      aftimembed.add_field(name="Double score", value=" ")
    
    if snake.lose == False:
    
      new_sent = await sent_time_embed.edit(embed=aftimembed)
    
      sent_time_embed = new_sent

    counter -= 1
    await asyncio.sleep(1)
  
  return

async def chaosmodeupdate(self,chaos):
  global CHANCE_WEAK_SNAKE
  chaos_random = random.randint(1,CHANCE_WEAK_SNAKE)

  if self.angry == True:
    self.move_for_angry += 1
    
    if self.move_for_angry > 3:
      
      self.move_for_angry = 0
      self.angry = False
      self.snake_char = "😄"
      self.tail_char = "🟨"

  if self.reverse_movement == True:
    self.move_for_reverse += 1
    if self.move_for_reverse > 3:
      self.move_for_reverse = 0
      self.reverse_movement = False
      self.snake_char = "😄"
      self.tail_char = "🟨"
  if chaos_random == 1 and chaos == "y":
    if self.angry == False and self.reverse_movement == False:
        self.weak = False
        self.snake_char = "😷"
        self.tail_char = "🟨"
    
    choose = random.randint(1,3)
    
    if choose == 1:
    #weak
      if self.weak == False and self.angry == False and self.reverse_movement == False:
        self.weak = True
        self.snake_char = "🤮"
        self.tail_char = "🟩"
      
        
    if choose == 2:
    #angry
      if self.angry == False and self.weak == False and self.reverse_movement == False:
        self.angry = True
        self.snake_char = "😡"
        self.tail_char = "🟥"
    if choose == 3:
    #reverse
      if self.reverse_movement == False and self.angry == False and self.weak == False:
        self.reverse_movement = True
        self.snake_char = "😈"
        self.tail_char = "🟪"
      
  return

async def sendingembed(map,interaction,first,snake,score,moveemoji,WAIT_TIME,channel,author,hardmode,chaos,power_up):
  if chaos == "y":

    await chaosmodeupdate(snake,chaos)
  
  
  if first == True:
   
    
    embed_message = nextcord.Embed(title="Snake Game", description="React below to decide where the snake goes!", color=nextcord.Color.red()) 
    embed_message.add_field(name=" ", value=map)
    
    embed_message.add_field(name="Last Move:", value=moveemoji)
    embed_message.add_field(name="Score:", value="Score: "+str(score))
    mention = '<@'+author+'>'
    embed_message.add_field(name="Created by:", value=mention)
    
    minutesb, secondsb = divmod(WAIT_TIME, 60)
    bftimembed = nextcord.Embed(title="State", description=" ", color=nextcord.Color.red())
    bftimembed.add_field(name="⏰Times Left:", value=str(minutesb) + "m " + str(secondsb) + "s")

    if hardmode == "y":
      bftimembed.add_field(name="😈Hardcore Mode", value=" ")

    if chaos == "y":
      bftimembed.add_field(name="😵‍💫Chaos Mode", value=" ")

    if power_up == "Extra life":
      bftimembed.add_field(name="Extra life", value=" ")
    if power_up == "Double score":
      bftimembed.add_field(name="Double score", value=" ")

    
    sent_time_embed = await channel.send(embed=bftimembed)
   
    sentembed = await channel.send(embed=embed_message)
    
    snake.embed_message = sentembed
   
    snake.timer_embed = sent_time_embed

  
  
    for i in directionemojis:
  
      await sentembed.add_reaction(i)
  
    
    await snake.console_game(channel,interaction,WAIT_TIME,sent_time_embed,author,hardmode,chaos,power_up)

      
  
  elif snake.lose == False:

    
    
    prev_message = snake.embed_message

    if prev_message == None:
      return
    
    newembed = nextcord.Embed(title="Snake Game", description="React below to decide where the snake go!",color=nextcord.Color.red()) 

    
    newembed.add_field(name=" ", value=map)

    newembed.add_field(name="Last Move:", value=moveemoji)
    newembed.add_field(name="Score:", value="Score: "+str(score))
    mention = '<@'+author+'>'
    newembed.add_field(name="Created by:", value=mention)
    
    update = await prev_message.edit(embed=newembed)
    
      
    for i in directionemojis:

      await update.add_reaction(i)

  


async def getreact(channel,snake):

  
  

  
  directiontoreturn = None
  await asyncio.sleep(0.2)
  

  msg = None
  if snake.lose == False:
    
    msg = snake.embed_message
  else:
    return
  
    
    
    
# create variables to save the highest reactions
  func_highest_reaction = ""
  func_highest_reaction_number = 0
  func_highest_reaction_count = 0


  for reaction in msg.reactions: # iterate through every reaction in the message
    if (reaction.count-1) > func_highest_reaction_number:
    # (reaction.count-1) discounts the bot's reaction
      func_highest_reaction = reaction.emoji
      func_highest_reaction_count = reaction.count-1
  
  selected = False
    
  if func_highest_reaction == "⬆️":
    
    directiontoreturn = "up"
    if snake.reverse_movement == True:
      directiontoreturn = "down"
    selected = True
  if func_highest_reaction == "⬇️":
    
    directiontoreturn = "down"
    if snake.reverse_movement == True:
      directiontoreturn = "up"
    selected = True
  if func_highest_reaction == "⬅️":
    
    directiontoreturn = "left"
    if snake.reverse_movement == True:
      directiontoreturn = "right"
    selected = True
  if func_highest_reaction == "➡️":
    
    directiontoreturn = "right"
    if snake.reverse_movement == True:
      directiontoreturn = "left"
    selected = True
  if func_highest_reaction == "🛑":
    await lose(snake,channel)
    return "down"
    
  #FOR CHAOS
  if snake.angry == True:
    alldirections = ["up","down","left","right"]
    pick = random.randint(0,3)
    directiontoreturn = alldirections[pick]
    return directiontoreturn
    
  if selected == False:
    
    directiontoreturn = "right"
    if snake.reverse_movement == True:
      directiontoreturn = "left"
    selected = True
  

  return directiontoreturn





async def lose(snake,channel):
  snake.lose = True
  global public_ingame_userid
  global DELETE_CHANNEL_TIME
  score = snake.score
  prev_message = snake.timer_embed
  prev_embed = snake.embed_message
  prev_highscore = read_userdatasave(snake.create_message_author,"user_score")
  if prev_highscore == None:
    prev_highscore = 0
  write_record = prev_highscore + score
  write_userdatasave(snake.create_message_author,"user_score",write_record)
  
  counter = DELETE_CHANNEL_TIME

  server_score = read_serverdatasave(channel.guild.id,"server_score")
  
  if server_score == None:
    server_score = 0

  save_server_score = server_score + score
  write_serverdatasave(channel.guild.id,"server_score",save_server_score)
  
  await prev_embed.clear_reactions()
  view = deletechannel(snake)
  await channel.send(view=view)

  for i in range(DELETE_CHANNEL_TIME):

    await asyncio.sleep(1)
    counter -= 1
    editembed = nextcord.Embed(title="Game Over", description="Score: "+str(score), color=nextcord.Color.red())

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
  embed_message = None
  timer_embed = None
  bombingrid = 0
  lose = False
  weak = False
  angry = False
  reverse_movement = False
  move_for_angry = 0
  move_for_reverse = 0
  point_add = 1
  extra_life = False
  double_score = False
  def __init__(self, grid_size, empty_char='⬜', snake_char='🫥', tail_char='🟨'):
      
      self.running = None  # for console running
      self.grid = [[empty_char for y in range(grid_size)] for i in range(grid_size)]  # snake grid
      self.grid_size = grid_size
      self.snake_char = snake_char
      self.tail_char = tail_char
      self.empty_char = empty_char
      self.turns = 0
      self.maxbomb = random.randint(5,10)
      row = int(len(self.grid) / 2)
      self.snake_pos = [row, row]
      self.apples = 0
      self.tail_positions = []
      self.last_move = (0, 0)
  
  
  async def load_grid(self,channel,input,WAIT_TIME,chaos):
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
        
        await sendingembed("\n".join(maparray),channel,False,self,self.score,send_emoji,WAIT_TIME,channel,self.create_message_author,None,chaos,None)       
  
  
  
  
  
  
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
      
      self.grid[self.snake_pos[0]][self.snake_pos[1]] = self.snake_char

      
  
  async def console_game(self,channel,interaction,WAIT_TIME,sent_time_embed,author,hardmode,chaos,power_up):

      if power_up == "Extra life":
        self.extra_life = True
      if power_up == "Double score":
        self.double_score = True
        self.point_add = self.point_add * 2
        
      if hardmode == "y":
        self.point_add += 1
      if chaos == "y":
        self.point_add += 1
      self.channelforlose = channel
      self.create_message_author = author
      self.running = True
      controls = {
          'up': self.move_up,
          'down': self.move_down,
          'left': self.move_left,
          'right': self.move_right,
          'exit': lambda: 'stop',
      }
     
      
      
      while self.running:
                          
          await countdown(channel,WAIT_TIME,sent_time_embed,self,hardmode,chaos)
          
          user_input = await getreact(channel,self)
          if user_input in controls.keys():
              
              controls_output = await controls[user_input]()
                               
              if controls_output == 'stop':
                return
              
              if self.appleingrid < 7:
                self.spawn_apple()
              if hardmode == "y" and self.bombingrid < self.maxbomb:
                self.spawn_bomb()
              
              self.tail_handle()
              await self.load_grid(channel,user_input,WAIT_TIME,chaos)
              
          else:
              return
  # --- Snake Movements ---
  
  async def check_move(self, x_off, y_off) -> True | False:
      
      x = self.snake_pos[1] + x_off  # I did this weird...
      y = self.snake_pos[0] + y_off
      if x >= self.grid_size or x < 0:
        if self.extra_life == False:
          await lose(self,self.channelforlose)
          
          return True
        else:
          self.extra_life = False
          return "extra"
            # snake died GG ez
      if y >= self.grid_size or y < 0:
          if self.extra_life == False:
              await lose(self, self.channelforlose)
              return True
          else:
              self.extra_life = False
              return "extra"
            # snake died GG ez
      
  
      if self.grid[y][x] == '🍎':
          if self.weak == True:
            if self.extra_life == False:
              await lose(self,self.channelforlose)
              return True
            else:
              self.extra_life = False
              return "extra"
          self.apples += 1
          self.score += self.point_add
          self.appleingrid -= 1
      if self.grid[y][x] == '💣':
        if self.extra_life == False:
          await lose(self, self.channelforlose)
          return True
        else:
          self.extra_life = False
          return "extra"
      if self.grid[y][x] == self.tail_char:
        if self.extra_life == False:
          await lose(self,self.channelforlose)
        
          return True
        else:
          self.extra_life = False
          return "extra"
      self.turns += 1
      return False
  
  async def move_right(self):  # move snake right
      result = await self.check_move(1, 0)
      if result == True:
          self.running = False
          return
      if result == "extra":
          return
      self.grid[self.snake_pos[0]][self.snake_pos[1]] = self.empty_char  # remove snake from grid
      self.grid[self.snake_pos[0]][self.snake_pos[1] + 1] = self.snake_char  # re-add snake in new position
      self.snake_pos = [self.snake_pos[0], self.snake_pos[1] + 1]
      return 0, 1
  
  async def move_left(self):  # move snake left
      result = await self.check_move(-1,0)
      if result == True:
          self.running = False
          return
      if result == "extra":
          return
      self.grid[self.snake_pos[0]][self.snake_pos[1]] = self.empty_char  # remove snake from grid
      self.grid[self.snake_pos[0]][self.snake_pos[1] - 1] = self.snake_char  # re-add snake in new position
      self.snake_pos = [self.snake_pos[0], self.snake_pos[1] - 1]
      return 0, -1
  
  async def move_down(self):  # move snake down
      result = await self.check_move(0, 1)
      if result == True:
          self.running = False
          return
      if result == "extra":
          return
      self.grid[self.snake_pos[0]][self.snake_pos[1]] = self.empty_char  # remove snake from grid
      self.grid[self.snake_pos[0] + 1][self.snake_pos[1]] = self.snake_char  # re-add snake in new position
      self.snake_pos = [self.snake_pos[0] + 1, self.snake_pos[1]]
      return 1, 0
  
  async def move_up(self):  # move snake up
      result = await self.check_move(0, -1)
      if result == True:
          self.running = False
          return
      if result == "extra":
          return
      self.grid[self.snake_pos[0]][self.snake_pos[1]] = self.empty_char  # remove snake from grid
      self.grid[self.snake_pos[0] - 1][self.snake_pos[1]] = self.snake_char  # re-add snake in new position
      self.snake_pos = [self.snake_pos[0] - 1, self.snake_pos[1]]
      return -1, 0
  
      # I hate boilerplate
      # That one o'hare youtber is cool tho
  
  def spawn_bomb(self):
      spawn_points = []
      for x in range(self.grid_size):
          for y in range(self.grid_size):
              if self.grid[x][y] != self.snake_char and self.grid[x][y] != self.tail_char and self.grid[x][y] != '💣':
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
              if self.grid[x][y] != self.snake_char and self.grid[x][y] != self.tail_char and self.grid[x][y] != '🍎':
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
  
  def tail_handle(self):
      if self.apples > 0:
          self.tail_positions.append(self.snake_pos.copy())  # the copy is important
          for pos in self.tail_positions:
              if pos != self.snake_pos:
                  self.grid[pos[0]][pos[1]] = self.tail_char
  
          
          if self.apples < len(self.tail_positions) - 1:
              if self.tail_positions[0] != self.snake_pos:
                  self.grid[self.tail_positions[0][0]][
                      self.tail_positions[0][1]] = self.empty_char  # replace end tail with empty char
                  self.tail_positions.pop(0)

class snakestart(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('Snake.py is ready!')

  
  @nextcord.slash_command(name="playsnake",description="Start a snake game!")
  
  
  async def playsnake(self, interaction: Interaction,snakehead = SlashOption(default="😉",required=False),snaketail = SlashOption(default="🟨", required=False),size: int = SlashOption(max_value=12,min_value=1,default=12,required=False),waittime: int = SlashOption(max_value=86400,min_value=1,default=2,required=False),power_up: str = SlashOption(choices=["Extra life","Double score"], default=None,required=False),hardmode: str = SlashOption(name="hardcore",choices=["y","n"],default="n",required=False),chaos: str = SlashOption(name="chaos",choices=["y","n"],default="n",required=False),private: str = SlashOption(name="private", choices=["y","n"], default="n",required=False)):
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
      catelog_id = read_serverdatasave(interaction.guild.id,"category_id")
      user_rebirth = read_userdatasave(interaction.user.id,"rebirth")
      userinv = read_userdatasave(interaction.user.id,"inventory")
      if power_up != None:
        
        if userinv == None:
          await interaction.response.send_message("You don't have "+power_up+".You can buy it from the shop!",ephemeral=True)
          return
        buyname = None
        if power_up == "Extra life":
          buyname = "user_extralife"
        elif power_up == "Double score":
          buyname = "user_doublescore"

      
        for key in userinv:
          if key == buyname:
            if userinv[key] < 1:
              await interaction.response.send_message("You don't have "+power_up+".You can buy it from the shop!",ephemeral=True)
              return
            else:
              newinv[buyname] = userinv[key] - 1
          else:
            newinv[key] = userinv[key]
          write_userdatasave(interaction.user.id,"inventory",newinv)
      
      
      if user_rebirth == None:
        user_rebirth = 0

      if user_rebirth < 1 and hardmode == "y":
        await interaction.response.send_message("You need to rebirth at least once to play hardcore mode!",ephemeral=True)
        return
      
      if user_rebirth < 3 and chaos == "y":
        await interaction.response.send_message("You need to rebirth at least 3 times to play chaos mode!",ephemeral=True)
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

        public_id += 1
        arg = "game-" + str(public_id)
        if private == "n":
        
          channel = await interaction.guild.create_text_channel(name=arg,category = self.client.get_channel(int(catelog_id)))
        else:
          overwrites = {
    interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
    interaction.user: nextcord.PermissionOverwrite(read_messages=True),
    self.client.user: nextcord.PermissionOverwrite(read_messages=True)
          }
          channel = await interaction.guild.create_text_channel(name=arg,category = self.client.get_channel(int(catelog_id)),overwrites=overwrites)
        
        
        snake = Snake(size, '⬛')
        
        snake.snake_char = snakehead
        snake.tail_char = snaketail
        snake.start()
        
        public_ingame_userid.append(str(interaction.user.id))
        tag = "<#"+str(channel.id)+">"
        await interaction.response.send_message("Game created: " + tag)
        
        await sendingembed(snake.return_grid(),interaction,True,snake,0,"🚫",waittime,channel,str(interaction.user.id),hardmode,chaos,power_up)
    else:
      await interaction.response.send_message("You cannot use Snaky command here!",ephemeral=True)
    
      

def setup(client):
  client.add_cog(snakestart(client))