import requests
import pandas as pd

def get_crypto_minutely_prices(crypto_id, vs_currency, days):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
    params = {
        'vs_currency': vs_currency,
        'days': days,  # 设置为1，表示过去24小时
        'interval': 'minutely'  # 每分钟的数据
    }
    response = requests.get(url, params=params)

    try:
        data = response.json()  # 尝试将响应转换为JSON
    except ValueError:
        print("无法将响应转换为JSON，响应内容:", response.text)
        return None

    # 打印API返回的数据
    print("API 响应数据:", data)    
    # 提取价格数据
    prices = data['prices']
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # 转换时间戳为日期时间格式
    return df

# 获取比特币过去24小时的每分钟价格
df = get_crypto_minutely_prices('bitcoin', 'usd', 1)
print(df.head())
df.shape