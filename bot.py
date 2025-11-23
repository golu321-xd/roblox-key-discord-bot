import discord
import requests

TOKEN = "MTQ0MjA1OTg1MDk0MjEyMDEwOA.GBMELS.GU1HHjIdsFUOjQqkqmVVkLneKge24vtkQJDeKo"   # <-- Yaha apna bot token dalna
API = "https://roblox-key-system-3.onrender.com"  # <-- Yaha apna backend Render URL dalna

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@tree.command(name="genkey", description="Generate a Roblox key")
async def genkey(interaction):
    r = requests.post(API + "/createkey")
    key = r.json()["key"]
    await interaction.user.send(f"Your Key: `{key}`\nUse /lock command to lock with HWID!")
    await interaction.response.send_message("Key sent in your DM!", ephemeral=True)

@tree.command(name="lock", description="Lock your key with HWID")
async def lock(interaction, key: str, hwid: str):
    r = requests.post(API + "/lockkey", json={"key": key, "hwid": hwid})
    if r.status_code == 200:
        await interaction.response.send_message("Key locked successfully!", ephemeral=True)
    else:
        await interaction.response.send_message("Failed to lock key.", ephemeral=True)

@client.event
async def on_ready():
    await tree.sync()
    print("Bot is Ready!")

client.run(TOKEN)
