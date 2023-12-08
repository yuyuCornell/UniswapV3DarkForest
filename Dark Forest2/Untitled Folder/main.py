#!/usr/bin/env python
# coding: utf-8

# In[1]:


import backtest as bt

def main():

    # 設定回測參數(可更改)
    start_date = '2023-10-15 03:00:00'
    end_date = '2023-11-14 03:00:00'
    target = 10000 #初始投入金額
    investment_method = "simple_interest"
    
    #回測
    important_sheets, fee_return = bt.range_backtest(start_date,end_date,target,investment_method)
    bt.show_analysis(important_sheets,target,fee_return,investment_method)
 
if __name__ == "__main__":
    main()

