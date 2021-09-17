import discord
from discord.ext import commands
import nacl
import uuid
import os
from Image import Imagens
from Music import Player


#from online import online

os.system("install-pkg tesseract-ocr")

token = os.environ['TOKEN']



intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = '=', case_insensitive = True, intents = intents)

#confirmação que o bot conseguiu logar
@bot.event
async def on_ready():
  activity = discord.Game(name="a vida fora")
  await bot.change_presence(status=discord.Status.online, activity=activity)
  print('We have logged in as {0.user}'.format(bot))

#Quando um novo membro ingressar no servidor
@bot.event
async def on_member_join(member):
  #colocar florzinha no nome
  await member.edit(nick='✿ ' + member.name + ' ✿')

  #Mandar mensagem de boas vindas
  guild = member.guild
  if guild.system_channel is not None:
    to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
    await guild.system_channel.send(to_send)

#Comando "ola", que responde o usuário com um embed com uma foto
@bot.command()
async def ola(ctx):
  embed = discord.Embed(
    title = "Olá, " + ctx.author.name + ".",
    description = "Eu sou a Diimili",
    color = 10592204
  )
  embed.set_footer(text="Stawi#2917 © Nicolas Colas#9973")
  file = discord.File("imagens/Diimili_Banner.png", filename = "image.png")
  embed.set_image(url="attachment://image.png")
  await ctx.send(file=file, embed=embed)

#Comando 'Falar'
@bot.command()
async def falar(ctx, *, message = '⠀'):
  await ctx.message.delete()
  await ctx.send(f"{message}".format(message))

#comando para criar uma enquete
@bot.command(name='poll', help='Create a Poll!')
async def poll(ctx, q, i : str, *opt):
  qu = "> "
  e = "\n"
  c = 0
  opts = ""
  l = ["🟡",
       "🟠",
       "🔴",
       "🟣",
       "🔵",
       "🟢",
       "⚪",
       "⚫"]
  new_l = ["","","","","","","",""] 
  question = '**' + q + '**' + e + qu + i + e
  for i in opt:
    opts = opts + qu + l[c] + ' ' + i + (e if c <= 9 else "")
    #p = str(l[c])
    new_l[c]=l[c]
    c = c + 1
    if c == 10: break
    
  response = question + opts
  m = await ctx.send(response)

  for j in new_l:
    await m.add_reaction(j)

    
#comando de teste
@bot.command()
async def ping(ctx):
  await ctx.send('Pong!')

async def setup():
  await bot.wait_until_ready()
  bot.add_cog(Player(bot))
  bot.add_cog(Imagens(bot))

bot.loop.create_task(setup())

#online()
bot.run(token)