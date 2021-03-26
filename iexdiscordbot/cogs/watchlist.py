import discord
import os
from discord.ext import tasks, commands
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
#IEX_API_KEY = 'pk_f2b12e738efc48ffbac89e2a756fb545'
#IEX_API_KEY ='Tpk_c25278fb5799400b816ae24f8d24acf8'
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
class watchlist(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Watchlist Command Loaded')

    @commands.command()
    async def test(self, ctx):
        print(f'{ctx.author}')
        return

    #$watchlist -a QS
    @commands.command(pass_ctx =True)
    async def watchlist(self, ctx, *, message):
        #if(user == None):
        #        user = ctx.message.author
        messageArgs = message.split()
        watchlist = []
        #user = member.message.author #ctx.message.author

        #print(f"Author: {message.author}")
        if messageArgs[0] == 'add' or '-a':
            #print(author)
            #print(f"Author: {message.author}")
            watchlist.append(messageArgs[1]) #This will append the Ticker Symbol into the watchlist array
            print(f"{ctx.author}'s watchlist: {messageArgs[1]}")
            #save the message to the database using the discord.Member
            embed = discord.Embed(
                title=ctx.author,
                #description=f'latest price: {latestPrice}.join, changePercent : {changePercent}',
                description=messageArgs[1],
                colour=discord.Color.green()
                )
            return
            await member.send(embed=embed)


def setup(client):
    client.add_cog(watchlist(client))
