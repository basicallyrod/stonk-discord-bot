import pandas as pd
import numpy as np
import json
import asyncio

from iexdiscordbot.helper.movingaverage import sma, ema, rolling_std, ewm_std

def typicalPriceHelper(data, method):
    open = data['open']
    high = data['high']
    low = data['low']
    close = data['close']
    hl2 = (data['high'] + data['low'] + data['close']) / 2
    hlc3 = (data['high'] + data['low'] + data['close']) / 3
    ohlc4 = (data['open'] + data['high'] + data['low'] + data['close']) / 4
    formula =  {
        'open' : open,
        'high' : high,
        'low' : low,
        'close' : close,
        'hl2' : hl2,
        'hlc3' : hlc3,
        'ohlc4' : ohlc4
    }
    typicalPrice = formula[method]
    #print(f'helper/movingaverage.typicalPriceHelper typicalPrice:{typicalPrice}')
    return typicalPrice

def LowerBand(data, smooth, n, method):
    typicalPrice = typicalPriceHelper(data, method)
    # print(f'typicalPrice: {typicalPrice}')
    #print(f'method: {method}')
    #print(f'LowerBand smooth: {smooth}')
    #print(f'rolling_mean: {rolling_mean}')
    #print(f'rolling_std: {rolling_std}')
    if smooth == 'sma':
        lowerband = sma(typicalPrice, n) - (rolling_std(typicalPrice, n) * 2)
        #print(f'sma : \n{lowerband}')
        #typicalPrice.empty()
        return lowerband.to_numpy()
    elif smooth == 'ema':
        lowerband = ema(typicalPrice, n) - (2 * ewm_std(typicalPrice, n))
        #print(f'ema : \n{lowerband}')
        #typicalPrice.empty()
        return lowerband.to_numpy()
    else:
        print(f'LowerBand error')

def MiddleBand(data, smooth, n, method):
    typicalPrice = typicalPriceHelper(data,method)
    #print(f'typicalPrice: {typicalPrice}')
    #print(f'MiddleBand smooth: {smooth}')
    if smooth == 'sma':
        middleband = sma(typicalPrice, n)
        #typicalPrice.empty()
        #print(f'sma : \n{middleband}')
        return middleband.to_numpy()
    elif smooth == 'ema':
        middleband = ema(typicalPrice, n)
        #typicalPrice.empty()
        #print(f'ema : \n{middleband}')
        return middleband.to_numpy()
    else:
        print(f'MiddleBand error')

def HigherBand(data, smooth, n, method):
    typicalPrice = typicalPriceHelper(data, method)
    #print(f'typicalPrice: {typicalPrice}')
    #print(f'HigherBand smooth method: {smooth}')
    if smooth == 'sma':
        higherband = sma(typicalPrice, n) + (2 * rolling_std(typicalPrice, n))
        #typicalPrice.empty()
        #print(f'sma : \n{higherband}')
        return higherband.to_numpy()
    elif smooth == 'ema':
        higherband = ema(typicalPrice, n) + (2 * ewm_std(typicalPrice, n))
        #typicalPrice.empty()
        #print(f'ema : \n{higherband}')
        return higherband.to_numpy()
    else:
        print(f'HigherBand error')
