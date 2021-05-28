import pandas as pd
import numpy as np



# def typicalPriceHelper(data, method):
#     open = data['open']
#     high = data['high']
#     low = data['low']
#     close = data['close']
#     hl2 = (data['high'] + data['low'] + data['close']) / 2
#     hlc3 = (data['high'] + data['low'] + data['close']) / 3
#     ohlc4 = (data['open'] + data['high'] + data['low'] + data['close']) / 4
#     formula =  {
#         'open' : open,
#         'high' : high,
#         'low' : low,
#         'close' : close,
#         'hl2' : hl2,
#         'hlc3' : hlc3,
#         'ohlc4' : ohlc4
#     }
#     typicalPrice = formula[method]
#     print(f'helper/movingaverage.typicalPriceHelper typicalPrice:{typicalPrice}')
#     return typicalPriceHelper

def sma(data, n):
    #data1 = typicalPriceHelper(data, method)
    if isinstance(data, object):
        print(f'sma object type(data): {type(data)}')
        rolling_mean = pd.DataFrame(data.rolling(window = n, min_periods=1).mean())
    #print(f'rolling mean: {rolling_mean}')
    #print(f'helper/movingaverage.sma data: {data}')
    #print(f'method: {method}')
        return rolling_mean
    elif isinstance(data, list):
        print(f'list')
    # else:
    #     print(f'not dataframe')

def rolling_std(data, n):
    #print(f'type(data): {type(data)}')
    rolling_std = pd.DataFrame(data.rolling(window = n).std(ddof=0))
    return rolling_std

def ema(data, n):
    #print(f'type(data): {type(data)}')
    if isinstance(data, object):
        ewm_mean = pd.DataFrame(data.ewm(span = n, adjust = False).mean())
        return ewm_mean
    else: print(f'not dataframe type')

def ewm_std(data, n):
    #print(f'type(data): {type(data)}')
    ewm_std = pd.DataFrame(data.ewm(span = n, adjust = False).std(ddof=0))
    return ewm_std
