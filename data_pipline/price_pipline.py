import requests
import pandas as pd
from sqlalchemy import create_engine

def get_binance_klines(symbol, interval, start_time, end_time):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': start_time,
        'endTime': end_time,
        'limit': 1000  # 每次请求最多1000条记录
    }
    all_data = []
    
    while True:
        response = requests.get(url, params=params)
        data = response.json()
        
        if not data:
            break
        
        all_data.extend(data)
        params['startTime'] = data[-1][0] + 1  # 更新开始时间为上次数据的最后一个时间戳
        
        # 如果获取的数据量小于限制，说明没有更多数据了
        if len(data) < 1000:
            break
    
    # 将数据转换为DataFrame
    df = pd.DataFrame(all_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 
                                         'close_time', 'quote_asset_volume', 'number_of_trades', 
                                         'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # 转换为日期时间格式
    return df

def store_to_sql(df, db_name, table_name):
    # 创建SQLite数据库连接
    engine = create_engine(f'sqlite:///{db_name}.db')
    
    # 将数据写入SQL数据库
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"数据已存储到 {db_name}.db 数据库的 {table_name} 表中。")

# 获取上个月的时间范围
end_time = pd.Timestamp.now().replace(hour=0, minute=0, second=0, microsecond=0)
start_time = end_time - pd.DateOffset(days=1)

# 将时间转换为Unix时间戳（毫秒）
start_time_ms = int(start_time.timestamp() * 1000)
end_time_ms = int(end_time.timestamp() * 1000)

# 获取上个月的每分钟K线数据
symbol = 'BTCUSDT'  # 交易对
df = get_binance_klines(symbol, '1m', start_time_ms, end_time_ms)

# 存储到SQL数据库
store_to_sql(df, 'crypto_data', 'btc_usdt_minutely')

# 打印前5行数据以验证
print(df.head())
