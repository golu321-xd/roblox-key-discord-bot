import discord
import requests
import os

TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # Render environment variable
API = os.getenv("BACKEND_URL")           # Render environment variable

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@tree.command(name="genkey", description="Generate a Roblox key")
async def genkey(interaction):
    await interaction.response.defer(ephemeral=True)  # prevent "did not respond"

    try:
        r = requests.post(f"{API}/createkey")
        key = r.json()["key"]
    except:
        await interaction.followup.send("Error connecting to backend!", ephemeral=True)
        return

    try:
        await interaction.user.send(f"Your Key: `{key}`\nUse /lock <key> <hwid> to lock it!")
        await interaction.followup.send("Key sent in DM!", ephemeral=True)
    except:
        # DM fail → ephemeral server message
        await interaction.followup.send(f"Your Key: `{key}` (DM failed, see here)", ephemeral=True)

@tree.command(name="lock", description="Lock your key with HWID")
async def lock(interaction, key: str, hwid: str):
    try:
        r = requests.post(f"{API}/lockkey", json={"key": key, "hwid": hwid})
        if r.status_code == 200:
            await interaction.response.send_message("Key locked successfully!", ephemeral=True)
        else:
            await interaction.response.send_message("Failed to lock key!", ephemeral=True)
    except:
        await interaction.response.send_message("Error connecting to backend!", ephemeral=True)

@client.event
async def on_ready():
    await tree.sync()
    print("Bot is ready!")

client.run(TOKEN)
