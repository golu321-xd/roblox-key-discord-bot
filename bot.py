import os
import discord
from discord.ext import commands
from flask import Flask
import requests

TOKEN = os.getenv("DISCORD_TOKEN")
BACKEND_URL = "https://roblox-key-system-3.onrender.com/genkey"

app = Flask(__name__)

# -------------------------
# Flask server for Render
# -------------------------
@app.route("/")
def home():
    return "Bot Running!"

# -------------------------
# Discord Bot
# -------------------------
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def genkey(ctx):
    try:
        response = requests.get(BACKEND_URL)
        if response.status_code == 200:
            key = response.text
            await ctx.send(f"Your Key: `{key}`")
        else:
            await ctx.send("⚠ Backend Error! Key generate nahi ho payi.")
    except:
        await ctx.send("⚠ Backend se connect nahi ho paaya!")
        

# -------------------------
# Run both Bot + Flask
# -------------------------
if __name__ == "__main__":
    from threading import Thread
    port = int(os.getenv("PORT", 10000))

    def run_flask():
        app.run(host="0.0.0.0", port=port)

    Thread(target=run_flask).start()
    bot.run(TOKEN)
