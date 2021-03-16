import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import requests
import json
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import pandas_datareader.iex as IEX
from datetime import timedelta, date, datetime

"""IEX Variables[Sandbox/Stable]"""

load_dotenv()
IEX_API_KEY = os.getenv('IEX_API_KEY')
base_url = 'https://sandbox.iexapis.com/'
version = 'stable/'

"""This is the long way of writing commands"""
class intraday(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def intraday(ctx, member: discord.Member, *, message):
        #symbol_param = message
        #field_param = 'latestPrice'
        api_call = f'{base_url+version}stock/{message}/intraday-prices?token={IEX_API_KEY}'
        requestIntradayPrices = requests.get(api_call)
        dataIntradayPrices = requestIntradayPrices.json()
        #IntradayPrices = dataIntradayPrices['IntradayPrices']

        #print(f'{dataIntradayPrices}')


        #pandasDataIntraPrices = web.DataReader('F', 'iex')

        pdIntradayPrices = pd.DataFrame(dataIntradayPrices)
        print(pdIntradayPrices)
        # embed = discord.Embed(
        #     title=message,
        #     description=IntradayPrices,
        #     colour= discord.Color.purple()
        #     )

        # await member.send(embed=embed)
        
def setup(client):
    client.add_cog(intraday(client))

