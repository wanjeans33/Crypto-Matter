from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import datetime

# 创建 GraphQL 客户端
transport = RequestsHTTPTransport(
    url="https://gateway.thegraph.com/api/49d8878bd657a7d8e26998c40548ff3b/subgraphs",
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# 查询 WBTC 历史利率数据
def get_wbtc_historical_rates(days=365*3):
    end_time = int(datetime.datetime.now().timestamp())
    start_time = end_time - days * 24 * 60 * 60

    # WBTC 的 ID 包含其地址和 Aave 的 LendingPoolAddressProvider 地址
    wbtc_id = "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599x24a42fd28c976a61df5d00d0599c34c4f90748c8"

    query = gql(
        """
        query GetRates($reserveId: ID!, $startTime: Int!, $endTime: Int!) {
            reserve(id: $reserveId) {
                id
                symbol
                paramsHistory(
                    where: {timestamp_gte: $startTime, timestamp_lte: $endTime}
                    orderBy: timestamp
                    orderDirection: asc
                ) {
                    variableBorrowRate
                    liquidityRate
                    stableBorrowRate
                    timestamp
                }
            }
        }
        """
    )

    params = {
        "reserveId": wbtc_id,
        "startTime": start_time,
        "endTime": end_time
    }

    result = client.execute(query, variable_values=params)
    return result

# 获取 WBTC 的历史利率数据
try:
    rates = get_wbtc_historical_rates()
    if rates['reserve'] and rates['reserve']['paramsHistory']:
        print("WBTC Historical Rates:")
        for rate in rates['reserve']['paramsHistory']:
            timestamp = datetime.datetime.fromtimestamp(rate['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            liquidity_rate = int(rate['liquidityRate']) / 1e27  # 转换为人类可读的百分比
            variable_borrow_rate = int(rate['variableBorrowRate']) / 1e27
            stable_borrow_rate = int(rate['stableBorrowRate']) / 1e27
            print(f"Time: {timestamp}, Liquidity Rate: {liquidity_rate:.4%}, Variable Borrow Rate: {variable_borrow_rate:.4%}, Stable Borrow Rate: {stable_borrow_rate:.4%}")
    else:
        print("No historical rate data found for WBTC.")
except Exception as e:
    print(f"Error fetching WBTC rates: {e}")
