import requests

api_key = "49d8878bd657a7d8e26998c40548ff3b"

# The Graph 的 API 网关 URL，替换 {api-key} 为你的实际 API 密钥
url = "https://gateway.thegraph.com/api/"+ api_key +"/subgraphs/id/8wR23o1zkS4gpLqLNU4kG3JHYVucqGyopL5utGxP2q1N"

# GraphQL 查询 WBTC 的历史利率数据，放宽查询限制
query = """
{
  reserve(id: "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599x24a42fd28c976a61df5d00d0599c34c4f90748c8") {
    id
    symbol
    paramsHistory(first: 100, orderBy: timestamp, orderDirection: desc) {
      variableBorrowRate
      liquidityRate
      stableBorrowRate
      timestamp
    }
  }
}
"""

# 请求的 JSON 数据
payload = {
    "query": query
}

# 设置请求头
headers = {
    "Content-Type": "application/json"
}

# 发送 POST 请求
response = requests.post(url, json=payload, headers=headers)

# 检查响应状态码并打印结果
if response.status_code == 200:
    data = response.json()
    if data["data"]["reserve"] and data["data"]["reserve"]["paramsHistory"]:
        print("WBTC Historical Rates:")
        for entry in data["data"]["reserve"]["paramsHistory"]:
            timestamp = entry["timestamp"]
            liquidity_rate = int(entry["liquidityRate"]) / 1e27  # 转换为人类可读的百分比
            variable_borrow_rate = int(entry["variableBorrowRate"]) / 1e27
            stable_borrow_rate = int(entry["stableBorrowRate"]) / 1e27
            print(f"Time: {timestamp}, Liquidity Rate: {liquidity_rate:.4%}, Variable Borrow Rate: {variable_borrow_rate:.4%}, Stable Borrow Rate: {stable_borrow_rate:.4%}")
    else:
        print("No historical rate data found for WBTC.")
else:
    print(f"Query Failed. Status Code: {response.status_code}")
    print(response.text)