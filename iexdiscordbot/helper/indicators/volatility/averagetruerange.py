import pandas as pd
import numpy as np

def highLowHelper(high, low, maxLength):
    highLow = []
    x = 1
    while x < maxLength:
            valHighLow = high[x] - low[x]
            highLow.append(valHighLow)

            print(f'{x} | high:{high[x]} | low:{low[x]} | valHighLow: {valHighLow}')
            x += 1
        #else: print(f'highLowHelper Error')

    return highLow

def absHighCloseHelper(high, close, maxLength):
    absHighClose = []
    x = 1
    while x < maxLength:
            valAbsHighClose = abs(high[x] - close[x-1])
            absHighClose.append(valAbsHighClose)
            print(f'{x} | high:{high[x]} | close:{close[x]} | valAbsHighClose: {valAbsHighClose}')
            x += 1
        #else: print(f'absHighCloseHelper Error')

    return absHighClose

def absLowCloseHelper(low, close, maxLength):
    absLowClose = []
    x = 1
    while x < maxLength:
            valAbsLowClose = abs(low[x] - close[x-1])
            absLowClose.append(valAbsLowClose)
            print(f'{x} | low:{low[x]} | close:{close[x]} | valAbsLowClose: {valAbsLowClose}')
            x += 1
        #else: print(f'absLowCloseHelper Error')

    return absLowClose

def trueRangeHelper(highLow, absHighClose, absLowClose, maxLength):
    trueRange = []
    x = 1
    #valTrueRange = max(highLow[x], absLowClose[x], absHighClose[x])
    #print(f'highLow: {highLow[x]}\n\nabsHighClose: {absHighClose[x]}\n\nabsLowClose: {absLowClose[x]}')
    while x < maxLength - 1:
        valTrueRange = max(highLow[x], absLowClose[x], absHighClose[x]) #only gets current ATR
        #valTrueRange = max(highLow[x-14:x], absLowClose[x-14:x], absHighClose[x-14:x])
        trueRange.append(valTrueRange)
        print(f'{x} | highLow: {highLow[x]}\n\nabsHighClose: {absHighClose[x]}\n\nabsLowClose: {absLowClose[x]}\n\n')
        x += 1
    #else: print(f'trueRangeHelper Error')

    return trueRange

def averageTrueRangeHelper(trueRange, maxLength, n):
    ATR = []
    x = 14

    while x < maxLength -1:
        valATR = (1/n) * sum(trueRange[x-14:x])
        ATR.append(valATR)
        x += 1
    #ATR = (1/n) * sum(trueRange[])
    return ATR
