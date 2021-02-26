#!/usr/bin/python
#
# https://api.tiingo.com/documentation/end-of-day
# https://iexcloud.io/docs/api/
# 
import sys,json,os
import requests as web
from datetime import datetime as dt
from datetime import timedelta as td
import numpy as np

headers = {
    'Content-Type': 'application/json'
}

#rTiingo = web.get("https://api.tiingo.com/tiingo/daily/dis/prices?startDate=2019-11-09&endDate=2019-12-09&token=de528961c1616b8d4275d3a51e419a43a9bcc979", headers=headers)
#rTiingo = web.get("https://api.tiingo.com/tiingo/daily/ipb/prices?startDate=2019-11-09&endDate=2019-12-11&resampleFreq=daily&token=de528961c1616b8d4275d3a51e419a43a9bcc979", headers=headers)
#print( json.dumps(rTiingo.json(),indent=4) )


from alpha_vantage.timeseries import TimeSeries
key = 'WBP42C3OA2QX3PY0'
ts = TimeSeries(key)
aapl,meta = ts.get_daily(symbol='AAPL')
print(aapl['2019-11-11'])

