import pandas as pd
from sqlalchemy import create_engine

def query_database(db_name, table_name, query=None):
    # 创建SQLite数据库连接
    engine = create_engine(f'sqlite:///{db_name}.db')
    
    if query:
        # 如果提供了SQL查询语句，使用该语句查询数据
        df = pd.read_sql(query, con=engine)
    else:
        # 否则查询整个表
        df = pd.read_sql_table(table_name, con=engine)
    
    return df

# 示例：查询整个表的数据
df_all = query_database('crypto_data', 'btc_usdt_minutely')
print("查询整个表的数据:")
print(df_all.head())

# 示例：执行SQL查询
sql_query = """
SELECT timestamp, open, close
FROM btc_usdt_minutely
WHERE timestamp BETWEEN '2024-09-14 00:00:00' AND '2024-09-15 00:01:00'
"""
df_filtered = query_database('crypto_data', 'btc_usdt_minutely', sql_query)
print("\n查询特定时间范围的数据:")
print(df_filtered.head())
