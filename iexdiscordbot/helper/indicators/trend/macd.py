import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plot
import matplotlib.image as mpimg
from iexdiscordbot.helper.movingaverage import ema

# def macdGetter(json_object, period, period1):
#     macd = ema(json_object['close'], period) - ema(json_object['close'], period1)
#     return macd
#
# def signalGetter(json_object, period):
#     signal_line = ema(json_object, period)
#     return signal_line

'''
Has error with scalar indexing of the DataFrame
(in watchlist having multiple tickers to search up creating multiple DataFrame)
'''

'''Proposed solution, make it in to numpy/array based calculations instead of using the pandas to do so'''

'''Or have the function be based on the # of given arguments'''
# def macdGetter(json_object, period, period1):
#     #print(json_object)
#     data = pd.DataFrame(json_object)
#     macd = ema(data, period) - ema(data, period1)
#     return macd
#
# def signalGetter(json_object, period):
#     #print(json_object)
#     data = pd.DataFrame(json_object)
#     signal_line = ema(data, period)
#     return signal_line

def macdGetter(json_object, period, period1):
    #print(json_object)
    macd = ema(json_object, period) - ema(json_object, period1)
    return macd

def signalGetter(json_object, period):
    #print(json_object)
    data = pd.DataFrame(json_object)
    signal_line = ema(json_object, period)
    return signal_line
