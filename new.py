import os
import alpaca_trade_api as tradeapi
import pandas as pd

os.environ["APCA_API_BASE_URL"] = "https://paper-api.alpaca.markets"
api = tradeapi.REST('PK5S94NMW8O14WQPAKIT','CHOxjFZZlwOz8s5lNRs0LzeQew5bk63ZMrorCB7h', api_version='v2')

count = 0
search = True

while search:

    if count < 1:
        # get most recent activities
        data = api.get_activities()
        # Turn the activities list into a dataframe for easier manipulation
        data = pd.DataFrame([activity._raw for activity in data])
        # get the last order id for pagination
        split_id = data.id.iloc[-1]

        trades = data

    else:
        data = api.get_activities(direction='desc', page_token=split_id)
        data = pd.DataFrame([activity._raw for activity in data])

        if data.empty:
            search = False

        else:
            split_id = data.id.iloc[-1]
            trades = trades.append(data)

    count += 1
    
trades = trades.reset_index(drop=True)
trades = trades.sort_index(ascending=False).reset_index(drop=True)

print(trades.side.unique())

# trades.to_csv('trades.csv')

# def calculate_profit(data):
#     for index, row in data.iterrows():
#         pass

for ticker in trades.symbol.unique():
    temp_data = trades[trades.symbol == ticker].copy()