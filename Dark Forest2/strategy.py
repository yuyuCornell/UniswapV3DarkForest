#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import pandas as pd

def simple_long_strategy(df,start_date,end_date):
    # Add columns for the buy range
    df['buy_lower'] = 0.0000 * df['close'].shift(1)  # 0.9 times the previous day's close
    df['buy_upper'] = 10000000000.00 # 1.1 times the previous day's close

    # Initialize a position column
    df['position'] = None

    # Dictionaries to store buy transactions
   
    buy_transactions = {df.index[0]:(0,999999)}
    sell = [df.index[-1]]

    print(f"buy actions {buy_transactions}")
    print(f"sell actions {sell}")
    print(f"the length are equal {len(buy_transactions),len(sell)}")
    

    return df, buy_transactions, sell


def simple_long_strategy2(df, start_date, end_date):
    # Calculate a simple moving average and standard deviation
    period = 14
    df['SMA'] = df['close'].rolling(window=period).mean()
    df['std'] = df['close'].rolling(window=period).std()

    # Dynamically set the buy range based on the standard deviation
    df['buy_lower'] = df['SMA'] - 0.5 * df['std']  # Adjust the multiplier as needed
    df['buy_upper'] = df['SMA'] + 0.5 * df['std']  # Adjust the multiplier as needed

    # Initialize a position column
    df['position'] = None

    # Dictionaries to store buy and sell transactions
    buy_transactions = {}
    sell = []

    # Iterate through the DataFrame
    for i in range(period, len(df)):  # Start from 'period' to avoid NaNs
        if df.loc[df.index[i-1], "position"] is None and \
           df.loc[df.index[i-1], 'close'] >= df.loc[df.index[i-1], 'buy_lower'] and \
           df.loc[df.index[i-1], 'close'] <= df.loc[df.index[i-1], 'buy_upper']:
            df.loc[df.index[i]:, "position"] = "long"
            buy_transactions[df.index[i]] = (df.loc[df.index[i], 'buy_lower'], df.loc[df.index[i], 'buy_upper'])

        if df.loc[df.index[i-1], "position"] == "long":
            df.loc[df.index[i]:, "position"] = None
            sell.append(df.index[i]) 

    print(f"buy actions {buy_transactions}")
    print(f"sell actions {sell}")
    print(f"the length are equal {len(buy_transactions) == len(sell)}")

    return df, buy_transactions, sell


def my_strategy1(df,start_date,end_date):
    ##strategy計算
    #  BB 
    period = 14  # 布林帶期間大小
    df["SMA"] = df["close"].rolling(period).mean()
    df["std"] = df["close"].rolling(period).std()
    df["upper_band"] = df["SMA"] + 2 * df["std"]
    df["lower_band"] = df["SMA"] - 2 * df["std"]
    df["BB%B"] = (df["close"] - df["lower_band"]) / (df["upper_band"] - df["lower_band"])
    overbought_threshold = 1
    oversold_threshold = 0
    df["position"] = None
    
    #注意格式! buy、sell
    buy = {}  
    sell = [] 
    
    # 
    for i in range(2, len(df)):
        if df.loc[df.index[i-2], "BB%B"] <= oversold_threshold and df.loc[df.index[i-1], "BB%B"] > oversold_threshold :
            if df.loc[df.index[i-1], "position"] is None: 
                df.loc[df.index[i]:,"position"] = "long"
                stop_ls  = df.loc[df.index[i-1],"SMA"] - 3 * df.loc[df.index[i-1],"std"]
                stop_pt  = df.loc[df.index[i-1],"SMA"] + 3 * df.loc[df.index[i-1],"std"]  
                buy[df.index[i]] = (stop_ls, stop_pt)
                             
        if df.loc[df.index[i-1], "position"] == "long":
            
            if df.loc[df.index[i-1], "close"] <= stop_ls or df.loc[df.index[i-1], "close"] >= stop_pt :  
                df.loc[df.index[i]:,"position"] = None
                sell.append(df.index[i]) 
    
            else :
                # 超買反轉時賣出
                if df.loc[df.index[i-2], "BB%B"] >= overbought_threshold and df.loc[df.index[i-1], "BB%B"] < overbought_threshold : 
                    df.loc[df.index[i]:,"position"] = None
                    sell.append(df.index[i])

    print(f"buy actions {buy}")
    print(f"sell actions {sell}")
    print(f"the length are equal {len(buy),len(sell)}")
    return df, buy, sell




def my_strategy_atr(df, start_date, end_date):
    # Strategy calculation
    period = 30  # Bollinger Bands and ATR period size
    df["SMA"] = df["close"].rolling(period).mean()
    df["std"] = df["close"].rolling(period).std()

    # Calculate Average True Range (ATR) for volatility
    df['high_low'] = df['high'] - df['low']
    df['high_close'] = (df['high'] - df['close'].shift()).abs()
    df['low_close'] = (df['low'] - df['close'].shift()).abs()
    df['TR'] = df[['high_low', 'high_close', 'low_close']].max(axis=1)
    df['ATR'] = df['TR'].rolling(period).mean()

    # Adjust Bollinger Bands width based on ATR
    multiplier = df['ATR'] / df['std']
    df["upper_band"] = df["SMA"] + multiplier * df["std"]
    df["lower_band"] = df["SMA"] - multiplier * df["std"]
    df["BB%B"] = (df["close"] - df["lower_band"]) / (df["upper_band"] - df["lower_band"])
    overbought_threshold = 1
    oversold_threshold = 0
    df["position"] = None
    
    buy = {}  
    sell = [] 

    for i in range(2, len(df)):
        # Dynamically adjust stop loss and stop profit based on ATR
        stop_loss_multiplier = 3  # Can be adjusted or made dynamic
        stop_profit_multiplier = 3  # Can be adjusted or made dynamic
        stop_ls = df.loc[df.index[i-1], "SMA"] - stop_loss_multiplier * df.loc[df.index[i-1], "ATR"]
        stop_pt = df.loc[df.index[i-1], "SMA"] + stop_profit_multiplier * df.loc[df.index[i-1], "ATR"]

        if df.loc[df.index[i-2], "BB%B"] <= oversold_threshold and df.loc[df.index[i-1], "BB%B"] > oversold_threshold:
            if df.loc[df.index[i-1], "position"] is None: 
                df.loc[df.index[i]:,"position"] = "long"
                buy[df.index[i]] = (stop_ls, stop_pt)
                             
        if df.loc[df.index[i-1], "position"] == "long":
            if df.loc[df.index[i-1], "close"] <= stop_ls or df.loc[df.index[i-1], "close"] >= stop_pt:
                df.loc[df.index[i]:, "position"] = None
                sell.append(df.index[i])
            elif df.loc[df.index[i-2], "BB%B"] >= overbought_threshold and df.loc[df.index[i-1], "BB%B"] < overbought_threshold:
                df.loc[df.index[i]:, "position"] = None
                sell.append(df.index[i])

    return df, buy, sell

# %%
