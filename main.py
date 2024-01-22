import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import subprocess

load_dotenv()
token = os.getenv("DISCORD_BOT_TOKEN")
serverID = int(os.getenv("SERVER_ID"))
server = discord.Object(id=serverID)

bot = commands.Bot(intents=discord.Intents.all(), command_prefix='/')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync(guild=server)
    print(f'We have logged in as {client.user}')

@tree.command(name="ping", description="ping pong", guild=server)
async def Ping(ctx):
    await ctx.response.send_message("Pong")

@tree.command(name="getserverstatus", description="Get actual server status", guild=server)
async def GetStatus(ctx):
    rawStatus = subprocess.run(["systemctl --user status palServer.service"], shell=True, capture_output=True)
    status = rawStatus.stdout.decode()
    await ctx.response.send_message(status)

@tree.command(name="restartserver", description="Ask systemctl to restart server", guild=server)
async def RestartServer(ctx):
    subprocess.run(["systemctl --user restart palServer.service"], shell=True, capture_output=True)
    await ctx.response.send_message("Restart in progress...")


client.run(token)