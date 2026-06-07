import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mplfinance as mpf
from datetime import datetime

# 获取数据
stock_df = ak.stock_zh_a_hist(
    symbol='000001',
    period='daily',
    start_date='20230101',
    end_date='20231231'
)

# 转为英文将列名
stock_df.rename(columns={
    '日期': 'date',
    '开盘': 'open',
    '收盘': 'close',
    '最高': 'high',
    '最低': 'low',
    '成交量': 'volume',
    '涨跌幅': 'change_pct'
}, inplace=True)

#将日期列转换为datetime格式，设置索引为日期
stock_df['date'] = pd.to_datetime(stock_df['date'])
stock_df.set_index('date', inplace=True)

#计算收益率
stock_df['return'] = stock_df['close'].pct_change() * 100

#拆线图
plt.figure(figsize=(12,4))
plt.plot(stock_df.index, stock_df['close'])
plt.title('close price trend')
plt.show()

plt.figure(figsize=(10,4))
sns.histplot(stock_df['return'].dropna(), bins=50)
plt.title('return distribution')
plt.show()

plt.figure(figsize=(6,4))
sns.boxplot(data=stock_df, y='return')
plt.title('return boxplot')
plt.show()

mpf.plot(stock_df[['open', 'high', 'low', 'close', 'volume']], type='candle', volume=True, title='k-line chart')

print(stock_df.head())

print(stock_df.isnull().sum())