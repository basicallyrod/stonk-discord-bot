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
from iexdiscordbot.helper.movingaverage import sma

#from iexdiscordbot.helper.closingpricehelper import closingPrices

"""IEX Variables[Sandbox/Stable]"""

load_dotenv()
IEX_API_KEY = os.getenv('IEX_API_KEY')
base_url = 'https://cloud.iexapis.com/'
version = 'stable/'

"""Asyncio Declaration"""
loop = asyncio.get_event_loop()

"""This is the long way of writing commands"""
class stochrsi(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Stoch RSI Command Loaded')

#Calculate RSI Here

    """
Future iterations:
Look at the whole month(28 days) and starting from the 14th day of the month, we can use the 1st day of the month as data for the RS/RSI calculation
    """
    @commands.command()
    async def stochrsi(self, ctx, *, message):

        #Step 1: Calculate the price movement everyday.
        print(f'STEP ONE: Pulling the Data')

        #Native IEX Method
        api_call = f'{base_url+version}stock/{message}/chart/3m?token={IEX_API_KEY}'
        requestHistoricalPrices = requests.get(api_call)
        dataHistoricalPrices = requestHistoricalPrices.json()
        pdStochRSI = pd.DataFrame(dataHistoricalPrices)

        aggregatedPandasData = pdStochRSI[['date','close']]


        #print(f'Pandas Data Frame: \n{aggregatedPandasData}\n len : {len(aggregatedPandasData)}')

        #helper.ta.momentum.rsi.priceDelta
        """
        #Declare/Initialize an array to  hold the closing prices of each day.
        #We only need to call the closing price of the stock the previous 14 days
        #Append the data from the pd.DataFrame into a LIST so we can manage the data locally.
        #Write a while loop here to put the iloc values into a list
        """
        date = []
        closingPrice = []


        """Appending the value of the row to the closingPrices list"""

        """While Loop Version"""
        # i = 0
        # while i < len(aggregatedPandasData):
        #     closingPrices.append(aggregatedPandasData.iloc[i, 0])
        #     i += 1

        """For Loop Version using range()"""
        # for row in range(len(aggregatedPandasData)):
        #     closingPrices.append(aggregatedPandasData.iloc[row, 0])

        """For Loop Version using df.iterrow()"""
        for label, row in aggregatedPandasData.iterrows():
           closingPrice.append(row['close'])
           date.append(row['date'])
        #calls to helper to add everything to a array
        #cphelp.closingPriceHelper.closingPrice(pdRSI)
        #cphelp.closingPriceHelper.date(pdRSI)
        #print(f'{pdRSI}')

        #loop.create_task(closingPrices(aggregatedPandasData))
        #await cphelp(aggregatedPandasData)
        #cphelp.dates(aggregatedPandasData)

        #print(f' closing price of index : {closingPrice}\ndate : {date}')

        #Step 2: Gather the average gain and loss over the last 14 days.
        #Initialize the gains and one for the losses

        #x = 0
        gain =  []
        loss = []
        avgGain = []
        avgLoss = []
        maxLength = len(aggregatedPandasData) - 1 #this is because len starts from 1 and not 0.
        print(f'maxLength : {maxLength}')

        #By using both the row and the column
        print(f'STEP 2: Calculating the RSI')

        """STEP 2.1 : Gathers all priceDeltas between each market day and seperates the gains from the losses"""


        """For Loop Version: Iterate this later"""
        maxRange = range(len(closingPrice)-1)
        print(f'maxRange: {maxRange}')
        for x in maxRange:
            if x == 0:
                gain.append(0)
                loss.append(0)
            if closingPrice[x] < closingPrice[x+1]:
                priceDelta = closingPrice[x+1] - closingPrice[x] # try using diff?
                #priceDelta = abs(closingPrices[x+1] - closingPrices[x])
                gain.append(priceDelta)
                loss.append(0)
            else:
                priceDelta = closingPrice[x] - closingPrice[x+1]
                loss.append(priceDelta)
                gain.append(0)

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
            avgGain.append(totalGain/10)

        for x in range(len(loss)):
            totalLoss += loss[x]
            avgLoss.append(totalLoss/10)

        print(f'totalGain: {totalGain}\ntotalLoss: {totalLoss}')
        print(f'length of avgGain: {len(avgGain)}\nlength of avgLoss: {len(avgLoss)}')

        #Step 3: Calculate the Relative Strength(RS) and the Relative Strength Index(RSI)
        #Initialize the RS and RSI arrays.
        #To calculate the RS, the formula is avgGain/avgLoss
        RS = []
        RSI = []

        #currently can't finish the avgGain/avgLoss due to there being more of one array size than the other one
        for x in maxRange:
            if x <= 13: #We only want to get the data after the 14th day because we need use the previous 14 days on the 15th to calculate the RSI
                RS.append(0)
                RSI.append(0)
            elif (x > 13 & x < (maxLength - 1)):
                #print(f'avgGain[{x}] : {avgGain[x]}')
                #print(f'avgLoss[{x}] : {avgLoss[x]}')
                valueRS = avgGain[x]/avgLoss[x]
                valueRSI = (100 - (100/(1+valueRS)))
                RS.append(valueRS)
                RSI.append(valueRSI)
                #print(f'valueRS[{x}] : {valueRS}')
                print(f'valueRSI[{x}] : {valueRSI}')
                #print(f'RSI : {RSI}')
                #print(f'X: {x}; Current RS: {RS[x]}; Current RSI : {RSI[x]}')
            else:
                print(f'RSI error')

        # start_date = (datetime.now() + timedelta(days = -5)) #this should be a 5 days range
        # end_date = datetime.now()
        # #delta = timedelta(days = 1)
        # print(f'{start_date} - {end_date}')
        # current_date = start_date
        #typeTester = np.dtype(date)
        #print(f'{typeTester}')
        #print(f'Date : {len(date)}\nCurrent RS : {len(RS)}\nCurrent RSI : {len(RSI)}')
        print(f'Date : {date}\nCurrent RS : {RS}\nCurrent RSI : {RSI}')
        #print(f'Date : {date[-14:]}\nCurrent RS : {RS[-14:]}\nCurrent RSI : {RSI[-14:]}') #date is the 15th and rs is the 14th

        StochRSI = []
        maStochRSI = []
        #Step 4: Calculate the Stochastic RSI
        # (Current RSI - min RSI ) / (max RSI - min RSI)
        for x in maxRange:
            if x <= 26:
                StochRSI.append(0)
            elif(x > 26 & (maxLength - 1)):
                currentRSI = RSI[x]
                minRSI = min(RSI[x-14:x])
                maxRSI  = max(RSI[(x-14):x])
                valueStochRSI = ((currentRSI - minRSI) / (maxRSI - minRSI))
                print(f'{x} | {currentRSI} | {minRSI} | {maxRSI} | {valueStochRSI}')
                StochRSI.append(valueStochRSI)
            else:
                print(f'Stoch RSI error')

        for x in maxRange:
            if x <= 40:
                maStochRSI.append(0)
            elif(x > 40 & (maxLength - 1)):
                valueMAStochRSI = sum(StochRSI[(x-14):x])/14
                maStochRSI.append(valueMAStochRSI)
                print(f'{x} | {valueMAStochRSI}')
            else:
                print(f'maStochRSI error')

        #maStochRSI = sma(StochRSI, 14)
        print(f'maStochRSI: {maStochRSI}')

        print(f'date length = {len(date)}')
        print(f'StochRS length = {len(StochRSI)}')
        print(f'maStochRS length = {len(maStochRSI)}')
        #Step 5: Plot the values
        plt.plot(date[41:], StochRSI[40:])
        plt.plot(date[41:], maStochRSI[40:])
        plt.ylabel('Stoch RSI')
        plt.xlabel('Date')
        #plt.show()
        plt.savefig('stochrsi.jpg')
        plt.close()

        #Step 5: Output the values
        file = discord.File('stochrsi.jpg')
        embed = discord.Embed(
            title=message,
            #description=f'latest price: {latestPrice}.join, changePercent : {changePercent}',
            description=''.join(f'Stochastic RSI: {StochRSI[-31:]}'),
            colour=discord.Color.green()
            )
        embed.set_image(url='attachment://stochrsi.jpg')

        await ctx.send(file = file, embed=embed)

def setup(client):
    client.add_cog(stochrsi(client))
