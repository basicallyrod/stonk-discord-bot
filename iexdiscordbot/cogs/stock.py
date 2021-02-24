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
#IEX_API_KEY = 'pk_f2b12e738efc48ffbac89e2a756fb545'
#IEX_API_KEY ='Tpk_c25278fb5799400b816ae24f8d24acf8'
IEX_API_KEY = os.getenv('IEX_API_KEY')
#os.environ['IEX_API_VERSION'] = 'iexcloud-sandbox'
base_url = 'https://sandbox.iexapis.com/'
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
        print('We have logged in')


    #$stock {ticker_symbol}
    @commands.command()
    async def stock(ctx, member: discord.Member, *, message):
        #symbol_param = message
        #field_param = 'latestPrice'
        api_call = f'{base_url+version}stock/{message}/quote?token={IEX_API_KEY}'

        requestQuote = requests.get(api_call)
        #requestTechnicalIndicators = 

        dataQuote = requestQuote.json()
        latestPrice = dataQuote['latestPrice']
        changePercent = dataQuote['changePercent']

        if changePercent < 0:
            messageColour = discord.Color.red()
        else:
            messageColour = discord.Color.green()

        #messageData = f'latest price: {latestPrice}.join \nchangePercent : {changePercent}'
        embed = discord.Embed(
            title=message,
            #description=f'latest price: {latestPrice}.join, changePercent : {changePercent}',
            description=''.join(f'latest price: {latestPrice} \nchangePercent : {changePercent}'),
            colour=messageColour
            )

        await member.send(embed=embed)

    @commands.command()
    async def intradayPrice(ctx, member: discord.Member, *, message):
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

#Calculate RSI Here

    """
Future iterations:
Look at the whole month(28 days) and starting from the 14th day of the month, we can use the 1st day of the month as data for the RS/RSI calculation
    """
    @commands.command()
    async def RSI(ctx, member: discord.Member, *, message):

        #Step 1: Calculate the price movement everyday. 

        
        #Pandas DataReader Method: This uses the Historical Prices API
        print(f'STEP ONE: Pulling the Data')
        # today = datetime.now().strftime('%m/%d/%Y')
        # previousMonth = (datetime.now() + \
        #     timedelta(weeks = -4)).strftime('%m/%d/%Y') #this should be 1 month range

        #iexDataRSI = web.DataReader(message, 'iex', previousMonth, today)['close']
        #topsDataRSI = web.DataReader(message, 'iex-tops', previousMonth, today)     
        #lastDataRSI = web.DataReader(message, 'iex-last', previousMonth, today)
        #bookDataRSI = web.DataReader(message, 'iex-book', previousMonth, today)

        #print(f'{iexDataRSI.tail(14)})

        #Native IEX Method
        api_call = f'{base_url+version}stock/{message}/chart/1m?token={IEX_API_KEY}'
        requestHistoricalPrices = requests.get(api_call)
        dataHistoricalPrices = requestHistoricalPrices.json()
        pdRSI = pd.DataFrame(dataHistoricalPrices)
        aggregatedPandasDataRSI = pdRSI[['close']].tail(14) 
        print(f'Pandas Data Frame: \n{aggregatedPandasDataRSI}\n len : {len(aggregatedPandasDataRSI)}')

       # """ 2 """

        """         
        #Declare/Initialize an array to  hold the closing prices of each day.
        #We only need to call the closing price of the stock the previous 14 days
        #Append the data from the pd.DataFrame into a LIST so we can manage the data locally.
        #Write a while loop here to put the iloc values into a list 
        """
        closingPrices = []

        """Appending the value of the row to the closingPrices list"""

        """While Loop Version"""
        # i = 0
        # while i < len(aggregatedPandasDataRSI):
        #     closingPrices.append(aggregatedPandasDataRSI.iloc[i, 0])
        #     i += 1

        """For Loop Version using range()"""
        # for row in range(len(aggregatedPandasDataRSI)):
        #     closingPrices.append(aggregatedPandasDataRSI.iloc[row, 0])

        """For Loop Version using df.iterrow()"""
        for label, row in aggregatedPandasDataRSI.iterrows():
            closingPrices.append(row['close'])

        print(f' closing price of index : {closingPrices}\n')

        #Next Interation
        """Maybe we can reduce it to less than .5% changes to reduce the outliers?"""
            #We see that 12,13 are within 6 cents of each other and we should reduce this outlier
        """
        Pandas Data Frame: 
            close
        6   43.82
        7   48.91
        8   47.53
        9   47.00
        10  45.31
        11  46.92
        12  46.16
        13  46.10
        14  55.97
        15  52.72
        16  69.72
        17  65.00
        18  63.22
        19  66.07
        """

        
        #Step 2: Gather the average gain and loss over the last 14 days.
        #Initialize the gains and one for the losses

        #x = 0
        gain =  []
        loss = []
        avgGain = []
        avgLoss = []
        maxLength = len(aggregatedPandasDataRSI) - 1 #this is because len starts from 1 and not 0.
        
        #By using both the row and the column
        print(f'STEP 2: Calculating the RSI')

        """STEP 2.1 : Gathers all priceDeltas between each market day and seperates the gains from the losses"""

        # """While Loop Version"""
        # while x < maxLength: #we will interate though the 14 rows
        #     if closingPrices[x] < closingPrices[x+1]:
        #         priceDelta = closingPrices[x+1] - closingPrices[x] 
        #         gain.append(priceDelta)
        #     else:
        #         priceDelta = closingPrices[x] - closingPrices[x+1]
        #         loss.append(priceDelta)       
        #     x += 1
        # print(f'gain : {gain}\nloss : {loss}')
        

        """For Loop Version: Iterate this later"""
        #print(f'{range(len(closingPrices))}')
        maxRange = range(len(closingPrices))
        for x in maxRange:
            if x == 13:
                gain.append(0)
                loss.append(0)
            elif closingPrices[x] < closingPrices[x+1]:
                priceDelta = closingPrices[x+1] - closingPrices[x]
                gain.append(priceDelta)
            else:
                priceDelta = closingPrices[x] - closingPrices[x+1]
                loss.append(priceDelta)
    
        print(f'gain : {gain}\nloss : {loss}\n')

        """STEP 2.2: Calculate the Total Possible Gain/Loss for the 14 day period"""
        """STEP 2.3: Calculate the Average Gain/Loss for the 14 day period"""
        #We need to consistently have it be atleast 14 days to compare the RSI
        #We currently always get the average of 14 days even though, we do not have 14 days of data to compare to
        totalGain = 0
        totalLoss = 0
        avgGain = []
        avgLoss = []
        for x in range(len(gain)):
            totalGain += gain[x]
            #print(f'{totalGain/14}')
            avgGain.append(totalGain/14)

        for x in range(len(loss)):
            totalLoss += loss[x]
            avgLoss.append(totalLoss/14)

        print(f'totalGain: {totalGain}\ntotalLoss: {totalLoss}')

        
        #avgGain = totalGain/14
        #avgLoss = totalLoss/14
        print(f'avgGain: {avgGain}\navgLoss: {avgLoss}')

        #Step 3: Calculate the Relative Strength(RS) and the Relative Strength Index(RSI)
        #Initialize the RS and RSI arrays.
        #To calculate the RS, the formula is avgGain/avgLoss
        testRS = 0 
        RS = []
        RSI = []

        for x in maxRange:
            if x >= 7:
                #RS.append(0)
                #RSI.append(0)
                break
                print(f'break')
            else:
                #print(f'avgGain[{x}] : {avgGain[x]}')
                #print(f'avgLoss[{x}] : {avgLoss[x]}')
                valueRS = avgGain[x]/avgLoss[x]
                RS.append(valueRS)
                valueRSI = (100 - (100/(1+RS[x])))
                RSI.append(valueRSI)
                #print(f'valueRS[{x}] : {valueRS}')
                #print(f'valueRSI[{x}] : {valueRSI}')
                #print(f'RSI : {RSI}')

        #Step 4: Output the values
        print(f'Current RS: {RS[-1]}\nCurrent RSI : {RSI[-1]}')

    @commands.command()
    async def hisotricalRSI(ctx, member: discord.Member, *, message):
        print(f'')
    @commands.command()
    async def intradayRSI(ctx, member: discord.Member, *, message):
        print(f'')
        
def setup(client):
    client.add_cog(stock(client))

