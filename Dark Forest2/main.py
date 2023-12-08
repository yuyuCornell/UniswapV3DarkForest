#!/usr/bin/env python
# coding: utf-8

# In[1]:


import backtest as bt

def main():

    # parameters
    start_date = '2023-10-15 03:00:00'
    end_date = '2023-11-14 03:00:00'
    target = 10000  # investment amount in USD
    investment_method = "compound_interest"
    
    # bactesting
    important_sheets, fee_return = bt.range_backtest(start_date,end_date,target,investment_method)
    bt.show_analysis(important_sheets,target,fee_return,investment_method)
 
if __name__ == "__main__":
    main()

