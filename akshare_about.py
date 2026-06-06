import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mplfinance as mpf
from datetime import datetime

stock_df = ak.stock_zh_a_hist(
    symbol='000001',
    period='daily',
    start_date='20230101',
    end_date='20231231'
)

stock_df['date'] = pd.to_datetime(stock_df['date'])
stock_df.set_index('date', inplace=True)

plt.plot(stock_df['date'], stock_df['close'])
sns.histplot(stock_df['return'], bins=50)
sns.boxplot(stock_df['return'])

stock_df_2023 = stock_df['2023-01':'2023-12']
print(stock_df_2023.head())

print(stock_df_2023.isnull().sum())

print(stock_df)