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

trades.to_csv('trades.csv')

# def calculate_profit(data):
#     for index, row in data.iterrows():
#         pass

for ticker in trades.symbol.unique():
    temp_data = trades[trades.symbol == ticker].copy()

############################
dfSel = trades
dfProfit = dfSel

    # convert filled_at to date
dfSel['transaction_time'] = pd.to_datetime(dfSel['transaction_time'], format="%Y-%m-%d %H:%M:%S")
    # convert to our timezone
# dfSel['transaction_time'] = dfSel['transaction_time'].dt.tz_convert('America/Kansas_City')

    # remove millis
dfSel['transaction_time'] = dfSel['transaction_time'].dt.strftime("%Y-%m-%d %H:%M:%S")


  # sort first based on symbol, then type as per the list above, then submitted date
dfSel.sort_values(by=['symbol', 'transaction_time', 'type'], inplace=True, ascending=True)

    # reset index
dfSel.reset_index(drop=True, inplace=True)
# add empty 'profit' column
dfProfit['profit'] = ''

totalProfit = 0.0
profitCnt   = 0
lossCnt     = 0
slCnt       = 0
ptCnt       = 0
trCnt       = 0
qty         = 0
profit      = 0
sign        = {'buy': -1, 'sell': 1, 'sell_short': 1}

# show header row
#print(tabulate(dfSel[:0], headers='keys', tablefmt='simple', showindex=False))

for index, row in dfSel.iterrows():
    # show data row
    #print(index, tabulate(dfSel[index:index+1], headers='', tablefmt='plain'))

    # conditions:
    # - buy/sell have the same symbol
    # - a trade is considered if no new/held orders are still open
    # - once qty is 0 a complete trade is confirmed and profit calculated
    # - a price is not None

    if index > 0:
        if dfSel['symbol'][index - 1] != dfSel['symbol'][index]:
            qty    = 0
            profit = 0

    # if dfSel['status'][index] == 'held':
    #     continue
    # if dfSel['status'][index] == 'new':
    #     continue
    # if dfSel['price'][index] is None:
    #     continue
    # if dfSel['price'][index] == '':
    #     continue
    # if dfSel['price'][index] == 'None':
    #     continue

    #print(index, tabulate(dfSel[index:index+1], headers='', tablefmt='plain'))

    side      = dfSel['side'][index]
    filledQty = int(dfSel['qty'][index]) * sign[side]
    qty       = qty + filledQty
    price     = float(dfSel['price'][index])
    pl        = filledQty * price
    profit    = profit + pl

    #print(f"{dfSel['symbol'][index]}: qty {filledQty} price {price} profit {profit:.3f}")

    if qty==0:
        # complete trade
        trCnt = trCnt + 1
        # put the profit in its column
        #dfProfit['profit'][index] = profit
        dfProfit.loc[index, 'profit'] = round(profit, 2)
        totalProfit = totalProfit + profit
        if profit >= 0:
            profitCnt = profitCnt + 1
            if dfSel['type'][index] == 'limit':
                ptCnt = ptCnt + 1
        else:
            lossCnt = lossCnt + 1
            if dfSel['type'][index] == 'stop_limit':
                slCnt = slCnt + 1
        profit = 0

# append the total
dfProfit.loc["Total", "profit"] = round(totalProfit, 2)  
# dfProfit.profit.sum()

dfProfit.to_csv('test.csv')