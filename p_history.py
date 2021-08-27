import os
import alpaca_trade_api as tradeapi
import pandas as pd

os.environ["APCA_API_BASE_URL"] = "https://paper-api.alpaca.markets"
api = tradeapi.REST('PK5S94NMW8O14WQPAKIT','CHOxjFZZlwOz8s5lNRs0LzeQew5bk63ZMrorCB7h', api_version='v2')

data = api.get_portfolio_history(period='10000D').df

data['LaggedEquity'] = data.equity.shift(1)
data['ChangeEquity'] = data.equity - data.LaggedEquity
data['PctChange'] = data.ChangeEquity / data.equity

print(data)
# data.df.to_csv('pfhistory.csv')
# data.equity.plot()