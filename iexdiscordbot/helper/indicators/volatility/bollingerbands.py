import pandas as pd
import numpy as np
import json
import asyncio

#from iexdiscordbot.helper.movingaverage.simplemovingaverage import sma, ema



def LowerBand(data, smooth, n):
    typicalPrice = (data['high'] + data['low'] + data['close']) / 3
    rolling_mean = typicalPrice.rolling(window = n, min_periods=1).mean()
    rolling_std = typicalPrice.rolling(window = n).std(ddof=0)
    print(f'typicalPrice: {typicalPrice}')
    print(f'LowerBand smooth: {smooth}')
    print(f'rolling_mean: {rolling_mean}')
    print(f'rolling_std: {rolling_std}')
    if smooth == 'sma':
        lowerband = pd.Series(rolling_mean - rolling_std * 2)
        print(f'sma : \n{lowerband}')
        return lowerband
    elif smooth == 'ema':
        lowerband = pd.Series(typicalPrice.ewm(span = n, adjust = False).mean() - (2 * typicalPrice.ewm(span = n, adjust = False).std(ddof=0)))
        print(f'ema : \n{lowerband}')
        return lowerband
    else:
        print(f'LowerBand error')

def MiddleBand(data, smooth, n):
    typicalPrice = (data['high'] + data['low'] + data['close']) / 3
    rolling_mean = typicalPrice.rolling(window = n, min_periods=1).mean()
    rolling_std = typicalPrice.rolling(window = n).std(ddof=0)
    #print(f'typicalPrice: {typicalPrice}')
    print(f'MiddleBand smooth: {smooth}')
    if smooth == 'sma':
        middleband = pd.Series(rolling_mean)
        print(f'sma : \n{middleband}')
        return middleband
    elif smooth == 'ema':
        middleband = pd.Series(typicalPrice.ewm(span = n, adjust = False).mean())
        print(f'ema : \n{middleband}')
        return middleband
    else:
        print(f'MiddleBand error')

def HigherBand(data, smooth, n):
    typicalPrice = (data['high'] + data['low'] + data['close']) / 3
    rolling_mean = typicalPrice.rolling(window = n, min_periods=1).mean()
    rolling_std = typicalPrice.rolling(window = n).std(ddof=0)
    #print(f'typicalPrice: {typicalPrice}')
    print(f'HigherBand smooth method: {smooth}')
    if smooth == 'sma':
        higherband = pd.Series(rolling_mean + (2 * rolling_std))
        print(f'sma : \n{higherband}')
        return higherband
    elif smooth == 'ema':
        higherband = pd.Series(typicalPrice.ewm(span = n, adjust = False).mean() + (2 * typicalPrice.ewm(span = n, adjust = False).std(ddof=0)))
        print(f'ema : \n{higherband}')
        return higherband
    else:
        print(f'HigherBand error')
