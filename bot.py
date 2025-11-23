import os
import discord
from discord.ext import commands
import requests
import json

TOKEN = os.getenv("DISCORD_TOKEN")
BACKEND_URL = "https://roblox-key-system-3.onrender.com"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Load keys locally (or backend can store)
KEY_FILE = "keys.json"
if not os.path.exists(KEY_FILE):
    with open(KEY_FILE, "w") as f:
        json.dump({}, f)

def load_keys():
    with open(KEY_FILE, "r") as f:
        return json.load(f)

def save_keys(keys):
    with open(KEY_FILE, "w") as f:
        json.dump(keys, f, indent=4)

def generate_key():
    import string, random
    return ''.join(random.choices(string.ascii_letters + string.digits, k=24))

# -----------------------------
# /genkey command
# -----------------------------
@bot.command()
async def genkey(ctx):
    keys = load_keys()
    user_id = str(ctx.author.id)
    key = generate_key()

    keys[key] = {
        "owner": user_id,
        "hwid": None
    }

    save_keys(keys)
    await ctx.author.send(f"✅ **Your Key:** `{key}`\nUse `/lockkey <key> <hwid>` to lock it.")
    await ctx.reply("📩 Check your DM for your key!")

# -----------------------------
# /lockkey command
# -----------------------------
@bot.command()
async def lockkey(ctx, key: str, hwid: str):
    keys = load_keys()
    user_id = str(ctx.author.id)

    if key not in keys:
        return await ctx.reply("❌ Invalid key")
    if keys[key]["owner"] != user_id:
        return await ctx.reply("❌ You don't own this key")
    keys[key]["hwid"] = hwid
    save_keys(keys)
    await ctx.reply(f"🔒 HWID locked for key `{key}`!")

# -----------------------------
# /verifykey command (optional)
# -----------------------------
@bot.command()
async def verifykey(ctx, key: str, hwid: str):
    keys = load_keys()
    if key not in keys:
        return await ctx.reply("❌ Invalid key")
    if keys[key]["hwid"] != hwid:
        return await ctx.reply("❌ HWID Mismatch")
    await ctx.reply("✅ Key Verified!")

# -----------------------------
# Bot Ready
# -----------------------------
@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

bot.run(TOKEN)
