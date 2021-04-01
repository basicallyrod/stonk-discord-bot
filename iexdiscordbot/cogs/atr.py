import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import requests
import asyncio
import json
import numpy as np
import pandas as pd
from datetime import timedelta, date, datetime
#import tracemalloc

#import iexdiscordbot.helper.closingpricehelper as cphelp

from iexdiscordbot.helper.indicators.volatility.averagetruerange import highLowHelper, absLowCloseHelper, absHighCloseHelper, trueRangeHelper, averageTrueRangeHelper
#from iexdiscordbot.helper.closingpricehelper import priceHelper
"""IEX Variables[Sandbox/Stable]"""

load_dotenv()
IEX_API_KEY = os.getenv('IEX_API_KEY')
base_url = 'https://sandbox.iexapis.com/'
version = 'stable/'

"""Asyncio Declaration"""
loop = asyncio.get_event_loop()

"""This is the long way of writing commands"""
class atr(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('ATR Command Loaded')

    @commands.command()
    async def atr(self, ctx, *, message):
        api_call = f'{base_url+version}stock/{message}/chart/3m?token={IEX_API_KEY}'
        requestHistoricalPrices = requests.get(api_call)
        dataHistoricalPrices = requestHistoricalPrices.json()
        data = pd.DataFrame(dataHistoricalPrices)
        print(f'{data}')
        n = 14

        low = data['low']
        high = data['high']
        close = data['close']

        highLow = []
        absHighClose = []
        absLowClose = []
        trueRange = []
        ATR = []

        maxLength = len(data)
        #maxRange = range(len(data) -1)
        #print(f'maxLength: {maxLength}')
        highLow = highLowHelper(high, low, maxLength)
        absHighClose = absHighCloseHelper(high, close, maxLength)
        absLowClose = absLowCloseHelper(low, close, maxLength)
        trueRange = trueRangeHelper(highLow, absHighClose, absLowClose, maxLength)
        ATR = averageTrueRangeHelper(trueRange, maxLength, n)
        #print(f'trueRange: {trueRange}')
        #print(f'highLow: {highLow}\n absHighClose: {absHighClose}\n absLowClose: {absLowClose}')
        #print(f'atr: {ATR}')

        embed = discord.Embed(
            title=message,
            #description=f'latest price: {latestPrice}.join, changePercent : {changePercent}',
            description=''.join(f'ATR: {ATR}'),
            colour=discord.Color.green()
            )

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(atr(client))
