import requests
import pandas as pd

def get_binance_klines(symbol, interval, start_time, end_time):
    url = f"https://api.binance.com/api/v3/klines"
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': start_time,
        'endTime': end_time,
        'limit': 1000  # 每次请求最多1000条记录
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    # 将数据转换为DataFrame
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# 获取比特币的每分钟K线数据，symbol为BTCUSDT
start_time = int(pd.Timestamp('2020-01-01').timestamp() * 1000)  # 开始时间，单位为毫秒
end_time = int(pd.Timestamp('2024-01-02').timestamp() * 1000)  # 结束时间，单位为毫秒
df = get_binance_klines('BTCUSDT', '1m', start_time, end_time)

print(df.head())
print(df.tail())
print(df.shape)