#!/usr/bin/python
#
# 
import csv,sys,pandas
from pandas.io.json import json_normalize
#
# 
#stocks = json.dumps(list(csv.DictReader(open(sys.argv[1]),delimiter="\t")))
stocks = list(csv.DictReader(open(sys.argv[1]),delimiter="\t"))
#stocks = csv.DictReader(open(sys.argv[1]),delimiter="\t")
spaced = json_normalize(stocks)
#Name    Price   Dividend Yield  Market Cap ($M) Forward P/E Ratio       Payout Ratio    Beta
spaced = spaced.reindex( columns=['Name','Price','Dividend Yield','Forward P/E Ratio','Payout Ratio','Beta'] )
with open('1.txt','w') as f:
  f.write( spaced.to_string() )

pe = []
for stock in stocks:
  try:
    Npe = float( stock['Forward P/E Ratio'] )
  except:
    Npe = -10
  try:
    Npo = float( stock['Payout Ratio'] )
  except:
    Npo = -10
  if Npe<-2: continue
  if Npo<-10: continue
  pe.append(stock)

with open('pe.txt','w') as f:
  f.write( json_normalize(pe).reindex( columns=['Name','Price','Dividend Yield','Forward P/E Ratio','Payout Ratio','Beta'] ).to_string() )

