import asyncio
import youtube_dl
import pafy
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True


class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.song_queue = {}

        self.setup()

    def setup(self):
        for guild in self.bot.guilds:
            self.song_queue[guild.id] = []

    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            ctx.voice_client.stop()
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)

    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format" : "bestaudio", "quiet" : True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0: return None

        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def play_song(self, ctx, song):
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)), after=lambda error: self.bot.loop.create_task(self.check_queue(ctx)))
        ctx.voice_client.source.volume = 0.5

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()

        await ctx.send("Eu não estou conectada em um canal de voz.")

    @commands.command()
    async def play(self, ctx, *, song=None):
        if song is None:
            return await ctx.send("Você precisa me falar uma música para que eu consiga tocá-la!")

        if ctx.voice_client is None:
            if ctx.author.voice is None:
                return await ctx.send("Você não está em nenhum canal de voz... Por favor, conecte-se em um canal de voz.")

            else:
              await ctx.author.voice.channel.connect()

        # handle song where song isn't url
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send("🔎 Procurando pela sua música, espere um pouquinho.")

            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send("Desculpe, eu não consegui encontrar a música que você queria. Tente usar o comando de busca.")

            song = result[0]

        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue[ctx.guild.id])

            if queue_len < 10:
                self.song_queue[ctx.guild.id].append(song)
                return await ctx.send(f"Eu já estou tocando uma música no momento, a sua música foi adicionada na fila na posição: {queue_len+1}.")

            else:
                return await ctx.send("Desculpa, eu só consigo 10 músicas por vez (meus pais precisam dar um jeito de arrumar minha memória), por favor espere essa música acabar para colocar outra na fila.")

        await self.play_song(ctx, song)
        await ctx.send(f"Tocando: {song}")

    @commands.command()
    async def search(self, ctx, *, song=None):
        if song is None: return await ctx.send("Você esqueceu de colocar alguma música para eu procurar.")

        await ctx.send("🔎 Procurando pela música, espere um pouquinho...")

        info = await self.search_song(5, song)

        embed = discord.Embed(title=f"Resultados para '{song}':", description="*Você pode usar esses links caso a música que você queria não seja a primeira.*\n\n", colour=10592204)
        
        amount = 0
        for entry in info["entries"]:
            embed.description += f"[{entry['title']}]({entry['webpage_url']})\n"
            amount += 1

        embed.set_footer(text=f"Mostrando os primeiros {amount} resultados.")
        await ctx.send(embed=embed)

    @commands.command()
    async def queue(self, ctx): # display the current guilds queue
        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send("Não tem nenhuma música na fila.")

        embed = discord.Embed(title="Lista de músicas", description="", colour=10592204)
        i = 1
        for url in self.song_queue[ctx.guild.id]:
            embed.description += f"{i}) {url}\n"
          
            i += 1

        await ctx.send(embed=embed)


    @commands.command()
    async def clear(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            self.song_queue[ctx.guild.id].clear()
            await ctx.send("A fila agora está vazia!")
        
        else:
          await ctx.send("A fila já estava vazia...")

    @commands.command()
    async def skip(self, ctx):
      ctx.voice_client.stop()
      await self.check_queue(ctx)


    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_paused():
            return await ctx.send("A música já está pausada.")

        ctx.voice_client.pause()
        await ctx.send("A música foi pausada.")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("Eu não estou conectada em nenhum canal de voz :/")

        if not ctx.voice_client.is_paused():
            return await ctx.send("Eu já estou tocando uma música")
        
        ctx.voice_client.resume()
        await ctx.send("A música voltou a ser tocada")