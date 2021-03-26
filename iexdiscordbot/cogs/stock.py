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
#os.environ['IEX_API_VERSION'] = 'iexcloud-sandbox'
base_url = 'https://cloud.iexapis.com/'
version = 'stable/'

#url_version = base_url + version

"""The short way of writing commands"""
# @client.command(pass_context=True)
# async def foo(ctx, arg):
#     await ctx.send(arg)

"""This is the long way of writing commands"""
class stock(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Stock Command Loaded')


    #$stock {ticker_symbol}
    @commands.command()
    #async def stock(ctx, member: discord.Member, *, message):
    async def stock(self, ctx, *, message):
        #symbol_param = message
        #field_param = 'latestPrice'
        api_call = f'{base_url+version}stock/{message}/quote?token={IEX_API_KEY}'

        requestQuote = requests.get(api_call)
        #requestTechnicalIndicators =

        dataQuote = requestQuote.json()
        latestPrice = dataQuote['latestPrice']
        changePercent = dataQuote['changePercent']
        latestVolume = dataQuote['latestVolume']

        # if changePercent < 0:
        #     messageColour = discord.Color.red()
        # else:
        #     messageColour = discord.Color.green()
        # if '-' in message:
        #     print('found -')
        #messageData = f'latest price: {latestPrice}.join \nchangePercent : {changePercent}'
        embed = discord.Embed(
            title=message,
            #description=f'latest price: {latestPrice}.join, changePercent : {changePercent}',
            description=''.join(f'latest price: {latestPrice} \nchangePercent : {changePercent}\nlatestVolume : {latestVolume}'),
            #colour=messageColour
            )
        #print(f'{member}')
        #await member.send(embed=embed)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(stock(client))
