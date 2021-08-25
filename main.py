import discord
import uuid
from discord.ext import commands


from PIL import Image

import os
#from online import online

token = os.environ['TOKEN']

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = '=', case_insensitive = True, intents = intents)

#confirmação que o bot conseguiu logar
@bot.event
async def on_ready():
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
    description = "Eu sou a Diimili.",
    color = 10432809
  )
  file = discord.File("imagens/Eri 2.gif", filename = "image.gif")
  embed.set_image(url="attachment://image.gif")
  await ctx.send(file=file, embed=embed)

#Comando 'Falar'
@bot.command()
async def falar(ctx, *, message):
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



#Método para mudar o contraste de imagens
def change_contrast(img, level):
  factor = (259 * (level + 255)) / (255 * (259 - level))
  def contrast(c):
      return 128 + factor * (c - 148)
  return img.point(contrast)

#Comando mudar contraste da imagem
@bot.command()
async def doc(ctx, contrast = 100):
  try:
    url = ctx.message.attachments[0].url
  except IndexError:
    await ctx.send("Nenhuma imagem detectada!")
  else:
    if url[0:26] == "https://cdn.discordapp.com":
      imageName = str(uuid.uuid4()) + '.jpg'
      await ctx.message.attachments[0].save(imageName)

      img = Image.open(imageName).convert('L') #mudar cor pra preto e branco
      img = change_contrast(img, contrast)
        
      img.save('output_file.jpg')
      file = discord.File("output_file.jpg", filename = "image.jpg")
      os.remove(imageName)
      os.remove('output_file.jpg')
      await ctx.send(file=file)
      await ctx.send(str(contrast))
#comando de teste
@bot.command()
async def ping(ctx):
  await ctx.send('Pong!')

#online()
bot.run(token)
