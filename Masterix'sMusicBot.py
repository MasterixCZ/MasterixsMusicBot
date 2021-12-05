import discord
from discord.ext import commands
import youtube_dl
import os

#Volání BOTa znakem "!"
client = commands.Bot(command_prefix="!")


#Připojování do kanálu "Muzika"
@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Počkejte, než tohle audio dohraje nebo použijte příkaz 'stop'")
        return
    
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name="Muzika")
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

#Odpojování BOTa od kanálu
@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("BOT není nikde připojen.")

#BOT zastaví hudbu
@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Nehraje žádné audio.")

#BOT spustí hudbu
@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("Audio není zastaveno.")

#BOT zastaví hudbu
@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

#BOTův Token
client.run('OTE0NDQ5OTAwNTY4MTk1MDcy.YaNN1Q.FA2baoZZGI6qrJk-nF7Eu26NmK8')
