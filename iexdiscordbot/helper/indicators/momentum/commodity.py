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

def cciHelper(data):
    cci = pd.Series((data - data.rolling(20).mean()) / (0.015 * data.rolling(20).std()), name = 'CCI')
    return cci.to_numpy()
