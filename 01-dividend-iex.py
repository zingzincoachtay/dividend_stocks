#!/usr/bin/python
#
# https://ntguardian.wordpress.com/2018/07/17/stock-data-analysis-python-v2/
# https://iexcloud.io/docs/api/
# 
import sys,json,os
import requests as web
import pandas
from pandas.io.json import json_normalize
from datetime import datetime as dt
from datetime import timedelta as td
import numpy as np

def spokesperson(msg,xlist):
  return msg+' '+','.join(xlist)

stocks = []
# 
#	 Obtain stock prices. Only weekdays are the trading days.
#	 - Yearly
#	 - Quarterly
#	 - Monthly
#	 - Weekly
# 
#duras = [5*4*12,5*4*3,5*4,5]
#units = {duras[0]:"Y",duras[1]:"Q",duras[2]:"M",duras[3]:"W"}
to0 = dt.today()
end = to0.strftime('%Y-%m-%d')
tokens = {
	 'IEX':'pk_58d08bc6bb04433cbb9265a14bd28ca4'
	,'TIINGO':'de528961c1616b8d4275d3a51e419a43a9bcc979'
}
# 
#	Dividend Paying Stock
# 
#symbols = ['gm','luv','cvs','pgr','dal','dis','wdc','stx','ge','syk','ntdoy','ipb','chl','nvda']
#	- watch list
symbols = ['aeo','anat','bbby','bcs','cop','cs','educ','et','fitb','ggb','gild','gme','gt','hpq','hsqvy','intc','khc','lnt','mt','nsrgy','ottr','qabsy','qcom','ubs','umpq','vod']
#	- stock by trading
#symbols = ['amd','mu','ctlt','',"PBR","CHK","FPI","NNA","ASC","SALT","MAXR","IVC","ORA","SQ","PYPL"]
#	- stock by dividend
#symbols = ['celp','f','rf','nsany','pbct','sne','ua','viaca']
advanced_symbols = []

headers = {
    'Content-Type':'application/json'
}
token = tokens['IEX']

dividend_refresh_schedule = 'refresh_dividend.schedule'
# 
# Refresh Schedule
# 	Load refresh_dividend.schedule
#	refresh_dividend.schedule: [
#		{ dividend_info_file:
#			['symbol':'F','dated':'UNIX TIME','due':dated+1 MONTH-1 DAY]
#		}
#		,{...}
#	]
# 

for symbol in symbols:
	print( spokesperson('Investingating: '+symbol,[]) )
	#
	print( spokesperson('Obtaining its dividend info',[]) )
	# dividend information
	# [10] per symbol per period
	#
	# https://cloud.iexapis.com/stable/stock/f/dividends/1m?token=pk_58d08bc6bb04433cbb9265a14bd28ca4
	rDiv = web.get("https://cloud.iexapis.com/stable/stock/"+symbol+"/dividends/3m?token="+token, headers=headers)
	dSched = rDiv.json()
	if( len(dSched)==0 ): continue
	t = dSched[0]
	exday = t['exDate']
	payday = t['paymentDate']
	###dInfo[symbol] = {'dated':exday,'dueby':payday}
	try:
		d = float(t['amount'])
	except NoneType:
		d = 0
	#
	# daily - previous
	# [2] per symbol
	#
	# -- https://sandbox.iexapis.com/stable/stock/rf/previous?token=pk_58d08bc6bb04433cbb9265a14bd28ca4
	# daily snapshot of market
	# -- https://sandbox.iexapis.com/stable/stock/market/previous?token=Tsk_3a7c04d7e1ad4987b95cf6ee4943b026
	#
	print( spokesperson('Obtaining its stock pricing info',[]) )
	# quote information
	# [1] per quote
	# 
	# Last Closed Price
	# -- https://cloud.iexapis.com/stable/stock/rf/quote/close?token=pk_58d08bc6bb04433cbb9265a14bd28ca4
	# Price-to-Earning Ratio
	# -- https://cloud.iexapis.com/stable/stock/rf/quote/peRatio?token=pk_58d08bc6bb04433cbb9265a14bd28ca4
	rDay = web.get("https://cloud.iexapis.com/stable/stock/"+symbol+"/quote?token="+token, headers=headers)
	dDaily = rDay.json()
	t = dDaily
	p = t['close']
	try:
		payout = d/p*100
	except:
		payout = 0
	peee = t['peRatio']
	#
	stock = {'*':symbol,'LastClosed':p,'Dividend':d,'Yield%':round(payout,3),'exDate':exday,'P/E':peee}
	#
	print( spokesperson('Obtaining its Earning to Price ratio',[]) )
	# EPS info
	# [1000] per symbol per period
	#
	# -- https://cloud.iexapis.com/stable/stock/aapl/earnings/1/actualEPS?token=
	#rEPS = web.get("https://cloud.iexapis.com/stable/stock/"+symbol+"/earnings/1/actualEPS?token="+token, headers=headers)
	#dEPS = rEPS.text
	#try:
	#	EPS = float(dEPS)
	#except:
	#	EPS = 0
	#stock['E2P'] = EPS
	stocks.append( stock )
#
print(json_normalize(stocks))


# time-series
# [2] per symbol per interval
#https://cloud.iexapis.com/stable/stock/f/chart/1y?chartCloseOnly=true&token=pk_58d08bc6bb04433cbb9265a14bd28ca4
#https://cloud.iexapis.com/stable/stock/f/chart/6m?chartCloseOnly=true&token=pk_58d08bc6bb04433cbb9265a14bd28ca4
#https://cloud.iexapis.com/stable/stock/f/chart/1m?chartCloseOnly=true&token=pk_58d08bc6bb04433cbb9265a14bd28ca4


# earnings
# [1000] per symbol per period
# https://sandbox.iexapis.com/stable/stock/aapl/earnings/1/actualEPS?token=Tsk_3a7c04d7e1ad4987b95cf6ee4943b026
# financial
# [5000] per symbol per period
#https://sandbox.iexapis.com/stable/stock/aapl/financials?token=Tsk_3a7c04d7e1ad4987b95cf6ee4943b026
# income statement
# [1000] per symbol per period
#https://sandbox.iexapis.com/stable/stock/aapl/income?token=Tsk_3a7c04d7e1ad4987b95cf6ee4943b026


def empty_pd():
  df_ = pd.DataFrame()
  return df_.fillna(0)
def YYYY_mm_dd(delta,today):
  ye0 = today - td(days=delta)
  return ye0.strftime('%Y-%m-%d')

def retrieve_stock_data(symb,repo,start,end):
  symL = {}
  validsymb = []
  for s in symb:
    try:
      symL[s] = web.DataReader(s,repo,start,end)
      validsymb.append(s)
    except KeyError:
      print("Symbol:"+s+" was invalid.")
  return (symL,validsymb)
def close_price_data(symb,repo,start,end):
  symL,validsymb = retrieve_stock_data(symb,repo,start,end)
  # 
  # Carry over to the next steps with the valid symbols.
  # 
  valid_stock_data = {}
  for s in validsymb:
    valid_stock_data[s] = symL[s]['close']
  return (pd.DataFrame(valid_stock_data),validsymb)

def Risk_LR(apr,spy,rrf):
  sy = apr.drop("SPY", 1).std()
  sx = apr.SPY.std()
  ybar = apr.drop("SPY", 1).mean() - rrf
  xbar = apr.SPY.mean() - rrf
  corr = apr.drop("SPY", 1).corrwith(apr.SPY)
  beta = corr * sy/sx
  alph = ybar - beta*xbar
  srpe = (ybar-rrf)/sy
  return (corr,beta,alph,srpe)

#RESULTS_CORR = empty_pd() # literary, COOR is VAR(APRY)
#RESULTS_BETA = empty_pd() # literary, BETA is AVG(APRY)
#RESULTS_ALPH = empty_pd()
#RESULTS_SRPE = empty_pd()

# 
# Getting Data
# ... Three-Month U.S. Treasury Bill 
# ... Used for calcualting the linear regression
# 
#tbill,rrfsymb = retrieve_stock_data(["TB3MS"],"fred", YYYY_mm_dd(duras[1],to0) ,end)
#rrf = tbill["TB3MS"].iloc[-1,0]


#spokesperson( 'Market correlation w.r.t. SPY' , RESULTS_CORR)
#spokesperson( 'Linear Regression model (beta)' , RESULTS_BETA)
#spokesperson( 'Sharpe ratios (s)' , RESULTS_SRPE)

