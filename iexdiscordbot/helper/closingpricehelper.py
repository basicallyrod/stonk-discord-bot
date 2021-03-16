from pandas import DataFrame as df
import tracemalloc
from datetime import timedelta, date, datetime
import asyncio

loop = asyncio.get_event_loop()
async def closingPrices(data):
    date = []
    closingPrice = []

    print(f'Pandas Data Frame: \n{data}')
    for label, row in df.iterrows(data):
        closingPrice.append(row['close'])
        date.append(row['date'])
        #print(f'Closing Price: {closingPrice}\ndate: {date} ')

    await closingPrice, date