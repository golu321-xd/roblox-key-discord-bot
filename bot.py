import discord
import requests
import os  # <- environment variables ke liye

# Token and API URL from environment variables
TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # Set this in Render environment
API = os.getenv("BACKEND_URL")           # Set this in Render environment

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@tree.command(name="genkey", description="Generate a Roblox key")
async def genkey(interaction):
    r = requests.post(f"{API}/createkey")
    key = r.json()["key"]
    await interaction.user.send(f"Your Key: `{key}`\nUse /lock to lock with HWID!")
    await interaction.response.send_message("Key sent in DM!", ephemeral=True)

@tree.command(name="lock", description="Lock key with HWID")
async def lock(interaction, key: str, hwid: str):
    r = requests.post(f"{API}/lockkey", json={"key": key, "hwid": hwid})
    if r.status_code == 200:
        await interaction.response.send_message("Key locked successfully!", ephemeral=True)
    else:
        await interaction.response.send_message("Failed to lock key.", ephemeral=True)

@client.event
async def on_ready():
    await tree.sync()
    print("Bot Ready!")

client.run(TOKEN)
