import pandas as pd
import numpy as np
import os
import requests
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
IEX_API_KEY = os.getenv('IEX_API_KEY')
#os.environ['IEX_API_VERSION'] = 'iexcloud-sandbox'
base_url = 'https://sandbox.iexapis.com/'
version = 'stable/'

def priceGetter(json_object):
    latestPrice = json_object['latestPrice']
    return latestPrice

def percentGetter(json_object):
    changePercent = json_object['changePercent']
    return changePercent

def volumeGetter(json_object):
    latestVolume = json_object['latestVolume']
    return latestVolume
