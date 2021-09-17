import pytesseract
import uuid
from PIL import Image
import os
import cv2
import discord
from discord.ext import commands


pytesseract.pytesseract.tesseract_cmd = "tesseract"
os.environ["TESSDATA_PREFIX"] = "/home/runner/.apt/usr/share/tesseract-ocr/4.00/tessdata/"

class Imagens(commands.Cog):

  def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  #método para melhorar imagem
  def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

  #Método para mudar o contraste de imagens
  def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
      return 128 + factor * (c - 148)
    return img.point(contrast)

#Comando para transcrever o texto de uma imagem
  @commands.command()
  async def tcv(ctx):
    try:
      url = ctx.message.attachments[0].url
    except IndexError:
      await ctx.send("Nenhuma imagem detectada!")
    else:
      if url[0:26] == "https://cdn.discordapp.com":
        imageName = str(uuid.uuid4()) + '.jpg'
        await ctx.message.attachments[0].save(imageName)

        #Melhorando a imagem para conseguir transcrever
        img = cv2.imread(imageName)
        img = cv2.resize(img,(0,0),fx=3,fy=3)
        img = get_grayscale(img)
        img = thresholding(img)
        text = pytesseract.image_to_string(img)

        os.remove(imageName)
        embed = discord.Embed(
        title = "💻 🪄 🗒️ \n\nTexto transcrito: ",
        description = '```' + text + '```',
        color = 10592204)
        await ctx.send(ctx.message.author.mention, embed = embed)

  #Comando mudar contraste da imagem
  @commands.command()
  async def scan(ctx, contrast = 100):
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