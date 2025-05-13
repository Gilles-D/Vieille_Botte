import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

from pubmed import search_pubmed

#get the token from .env file
load_dotenv()
TOKEN = os.environ['DISCORD_TOKEN']

#config from bot creation
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

@bot.command()
async def pubmed(ctx, *args):
    """
    Recherche PubMed avec une requête et nombre de résultats (optionnel)
    Exemple : !pubmed Parkinson sleep 3
    """
    if not args:
        await ctx.send("❗ Utilisation : `!pubmed <requête> [nombre de résultats]`")
        return

    *query_parts, last_arg = args

    # Vérifie si le dernier mot est un nombre
    try:
        max_results = int(last_arg)
        query = " ".join(query_parts)
    except ValueError:
        max_results = 5
        query = " ".join(args)

    await ctx.send(f"🔍 Recherche PubMed pour : `{query}` ({max_results} résultats)...")

    results = search_pubmed(query, max_results=max_results)
    if not results:
        await ctx.send("❌ Aucun résultat trouvé.")
        return

    for title, url in results:
        await ctx.send(f"**{title}**\n{url}")

bot.run(TOKEN)
