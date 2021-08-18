# from alpaca_dashboard import report2
import alpaca_trade_api as tradeapi
import os
import pandas as pd
import numpy as np

days = 30
key = 'PK5S94NMW8O14WQPAKIT'
secret = 'CHOxjFZZlwOz8s5lNRs0LzeQew5bk63ZMrorCB7h'
os.environ["APCA_API_BASE_URL"] = "https://paper-api.alpaca.markets"
api = tradeapi.REST(key,secret, api_version='v2')

# pandl = report2(api, days)

# Get a list of filled orders. 
# Can also limit the results by date if desired.
activities = api.get_activities(activity_types='FILL')
print(len(activities))

# Turn the activities list into a dataframe for easier manipulation
activities_df = pd.DataFrame([activity._raw for activity in activities])

# The qty and price fields are strings. 
# Convert them to numeric values for calculations.
activities_df[['price', 'qty']] = activities_df[['price', 'qty']].apply(pd.to_numeric)

# Add columns for net_qty and net_trade. 
activities_df['net_qty'] = np.where(activities_df.side=='buy', activities_df.qty, -activities_df.qty)
activities_df['net_trade'] = -activities_df.net_qty * activities_df.price

# Filter out any stocks where the buy and sell quantities don't sum to 0
net_zero_trades = activities_df.groupby('symbol').filter(lambda trades: sum(trades.net_qty) == 0)

# Finally, group by stock and sum the net_trade amounts 
profit_per_symbol = net_zero_trades.groupby('symbol').net_trade.sum()