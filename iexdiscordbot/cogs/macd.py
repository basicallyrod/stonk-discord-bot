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
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#from iexdiscordbot.helper.trend.macd import
from iexdiscordbot.helper.movingaverage import ema

"""IEX Variables[Sandbox/Stable]"""

load_dotenv()
IEX_API_KEY = os.getenv('IEX_API_KEY')
base_url = 'https://cloud.iexapis.com/'
version = 'stable/'

"""This is the long way of writing commands"""
class macd(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('MACD Command Loaded')

    @commands.command()
    async def macd(self, ctx, *, message):
        api_call = f'{base_url+version}stock/{message}/chart/3m?token={IEX_API_KEY}'
        requestHistoricalPrices = requests.get(api_call)
        dataHistoricalPrices = requestHistoricalPrices.json()
        data = pd.DataFrame(dataHistoricalPrices)
        print(f'{data}')

        macd = ema(data['close'], 12) - ema(data['close'], 26)
        signal_line = ema(macd, 9)

        date = data['date']

        print(f'date length = {len(date[14:])}')
        print(f'macd length = {len(macd[14:])}')
        print(f'signal_line length = {len(signal_line[14:])}')
        print(f'macd: {macd}\n\nsignal_line: {signal_line}')
        plt.plot(date[14:], macd[14:], label = 'macd')
        plt.plot(date[14:], signal_line[14:], label = 'signal line')
        plt.ylabel('MACD')
        plt.xlabel('Date')
        #plt.show()
        plt.savefig('macd.jpg')
        plt.close()
        file = discord.File('macd.jpg')
        embed = discord.Embed(
            title=message,
            #description=f'latest price: {latestPrice}.join, changePercent : {changePercent}',
            #description=''.join(f'macd: {macd}\nsignal_line: {signal_line}'),
            colour=discord.Color.green()
            )
        embed.set_image(url='attachment://macd.jpg')

        await ctx.send(file = file, embed=embed)

def setup(client):
    client.add_cog(macd(client))
