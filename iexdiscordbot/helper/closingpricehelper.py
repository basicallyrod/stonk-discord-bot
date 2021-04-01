from pandas import Series as s
#import tracemalloc
from datetime import timedelta, date, datetime
import asyncio

#loop = asyncio.get_event_loop()
def priceHelper(data, type):
    #date = []
    price = []

    #print(f'Pandas Data Frame: \n{data}')
    for index, item in s.items(data):
        price.append(item)
        #date.append(row['date'])
        #print(f'Closing Price: {closingPrice}\ndate: {date} ')

    return price
