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
import tracemalloc
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#import iexdiscordbot.helper.closingpricehelper as cphelp

#from iexdiscordbot.helper.closingpricehelper import closingPrices
from iexdiscordbot.helper.indicators.momentum.commodity import typicalPriceHelper, cciHelper

"""IEX Variables[Sandbox/Stable]"""

load_dotenv()
IEX_API_KEY = os.getenv('IEX_API_KEY')
base_url = 'https://sandbox.iexapis.com/'
version = 'stable/'

"""Asyncio Declaration"""
loop = asyncio.get_event_loop()

"""This is the long way of writing commands"""
class cci(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('CCI Command Loaded')

#Calculate RSI Here
    @commands.command()
    async def cci(self, ctx, *, message):

        #CCI = ([(highest + lowest + close)/3] - n Moving Average of M) / (0.015 * mean deviation between the mean price and moving average of mean prices)
        api_call = f'{base_url+version}stock/{message}/chart/3m?token={IEX_API_KEY}'
        requestHistoricalPrices = requests.get(api_call)
        dataHistoricalPrices = requestHistoricalPrices.json()
        data = pd.DataFrame(dataHistoricalPrices)

        #aggregatedData = data[['high','low', 'close', 'date']]
        print(f'{data}')

        # date = []
        # high = []
        # low = []
        # closingPrice = []

        # for label, row in aggregatedData.iterrows():
        #    date.append(row['date'])
        #    high.append(row['high'])
        #    low.append(row['low'])
        #    closingPrice.append(row['close'])
        method = 'hlc3'

        typicalPrice = typicalPriceHelper(data, method)
        #typicalPrice = (data['high'] + data['low'] + data['close']) / 3
        #print(f'{data['high']} + {data['low']} + {data['close']}')
        #CCI = pd.Series((typicalPrice - typicalPrice.rolling(20).mean()) / (0.015 * typicalPrice.rolling(20).std()), name = 'CCI')
        #data = data.join(CCI)
        cci = cciHelper(typicalPrice)
        #print(f'{typicalPrice} \n {CCI}')
        print(f'{cci}')

        date = data['date']
        lenDate = len(date)
        lenCCI = len(cci)
        print(f'date length = {lenDate}')
        print(f'cci length = {lenCCI}')
        plt.plot(date[19:], cci[19:], label = 'cci')
        plt.ylabel('cci')
        plt.xlabel('Date')
        plt.savefig('cci.jpg')
        plt.close()
        file = discord.File('cci.jpg')


        embed = discord.Embed(
            title=message,
            #description=f'latest price: {latestPrice}.join, changePercent : {changePercent}',
            description=''.join(f'CCI: {cci[-5:]}'),
            colour=discord.Color.green()
            )
        embed.set_image(url='attachment://cci.jpg')
        #await ctx.send(embed=embed)
        await ctx.send(file = file, embed=embed)

def setup(client):
    client.add_cog(cci(client))
