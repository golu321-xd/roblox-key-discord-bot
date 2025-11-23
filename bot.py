import os
import discord
from discord.ext import commands
import requests

# -----------------------------
# ENV VARIABLE (Render)
# -----------------------------
TOKEN = os.getenv("DISCORD_TOKEN")
BACKEND_URL = "https://roblox-key-system-3.onrender.com/genkey"

# -----------------------------
# Discord Bot Setup
# -----------------------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

# -----------------------------
# /genkey Command
# -----------------------------
@bot.command()
async def genkey(ctx):
    try:
        response = requests.get(BACKEND_URL)
        if response.status_code == 200:
            key = response.text
            await ctx.send(f"✅ Your Key: `{key}`")
        else:
            await ctx.send("⚠ Backend Error! Key generate nahi ho payi.")
    except Exception as e:
        await ctx.send(f"⚠ Backend se connect nahi ho paaya! Error: {e}")

# -----------------------------
# Run Bot
# -----------------------------
bot.run(TOKEN)
