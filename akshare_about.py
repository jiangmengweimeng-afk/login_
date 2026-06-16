import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mplfinance as mplf
import time

# 获取数据
def get_stock(symbol, start_date, end_date):
    success = False
    stock_df = None

    try:
        stock_df = ak.stock_zh_a_hist(
            symbol=symbol,
            period='daily',
            start_date=start_date,
            end_date=end_date
        )
        if stock_df is not None and not stock_df.empty and not stock_df['close'].isnull().any():
            success = True
            stock_df.to_csv(f'{symbol}_data.csv')
            print('获取数据成功')
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

            #将日期列转换为datetime格式，设置索引为日
            stock_df['date'] = pd.to_datetime(stock_df['date'])
            stock_df.set_index('date', inplace=True)

            #计算收益率
            stock_df['return'] = stock_df['close'].pct_change() * 100

            return stock_df
        else: 
            print('获取数据失败')
            success = False
    except Exception as e:
        print(f'第一次请求失败: {e}')
        success = False
    
    if not success:
        for attempt in range(1, 3):
            print(f'sanmaiohoudi{attempt + 1}次重试')
            time.sleep(3) 
            try:
                stock_df = ak.stock_zh_a_hist(
                    symbol=symbol,
                    period='daily',
                    start_date=start_date,
                    end_date=end_date
                )
                if stock_df is not None and not stock_df.empty and not stock_df['close'].isnull().any():
                    success  = True
                    stock_df.to_csv(f'{symbol}_data.csv')
                    return stock_df
                else:
                    print(f'第{attempt + 1}次失败')
                    success = False
            except RuntimeError as e:
                print(f'第{attempt + 1}次重试失败: {e}')
                continue
        
        try:
            df = pd.read_csv(f'{symbol}_data.csv')
            if df.empty or df['close'].isnull().any():
                raise RuntimeError('本地数据没有意义')
            else:
                print(f'读取本地文件: {df.head()} 成功')
                return df
        except FileNotFoundError:
            raise RuntimeError('本地文件不存在')
        except Exception as e:
            raise RuntimeError(f'读取本地文件失败: {e}')
    


def plot_stock_analysi(data):

    #拆线图
    plt.figure(figsize=(12,4))
    plt.plot(data.index, data['close'])
    plt.title('close price trend')
    plt.show()

    plt.figure(figsize=(10,4))
    sns.histplot(data['return'].dropna(), bins=50)
    plt.title('return distribution')
    plt.show()

    plt.figure(figsize=(6,4))
    sns.boxplot(data=data, y='return')
    plt.title('return boxplot')
    plt.show()

    mplf.plot(data[['open', 'high', 'low', 'close', 'volume']], type='candle', volume=True, title='k-line chart', savefig='kline.png')

def print_summary_data(data):
    print(data.head)
    print(data.isnull().sum())


if __name__ == '__main__':
    data = get_stock(symbol='000001', start_date='20200101', end_date='20231231')
    plot_stock_analysi(data)
    print_summary_data(data)
