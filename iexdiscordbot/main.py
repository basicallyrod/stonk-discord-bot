import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import numpy
import pandas
import requests

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

""" IEX_TOKEN = os.getenv('IEX_TOKEN')

base_url = 'https://sandbox.iexapis.com/'
version = 'stable/'

symbol_param = 'PLTR'
#for using the chart endpoint
#range_param = '1d'
#endpoint_path = f'stock/{symbol_param}/chart/{range_param}'

#for using the quote end point
field_param = 'latestPrice'
endpoint_path = f'stock/{symbol_param}/quote/{field_param}'

query_params = f'?token={IEX_TOKEN}'
api_call = f'{base_url}{version}{endpoint_path}{query_params}'
print(f'API Calls: {api_call}')

r = requests.get(api_call)
data = r.json()
print(f'\nHeaders: {r.headers}')
print(f"IEX Cloud Messages Used: {r.headers['iexcloud-messages-used']}")
print(f'\nData: {data}')
#take this data and split it into packs of 5po """

#client = discord.Client()
client = commands.Bot(command_prefix = '$')



@client.command(pass_context=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command(pass_context=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(DISCORD_TOKEN)
