# Crypto-Matter
Coorprate Company Project

There are three main tasks
1. Get crypto and funding rate data + store it in a database
2. Build models and tools to explore and understand drivers
3. Make predictions on funding rates

## Establish the Database and API pipline

### coingecko API
The coingecko API didnt offer historical minutely price data.
They can only offer minutely in 24h, hourly in 90 days and daily in 1 year.

### Binance API 
the Binance API have more detailable Trading Data in Cryptro. But It still has some limitaion. The maximual data row by each request is only 1000. If we want the minutely Data in 24h(one Day) We need to request twice.

The easiest solution is to use Binance API 2 request pre Day. 
every 12 hours with 720 rows data by one request.

Next step: establish the basic SQL databank to store the day
and automatiely request all data from Binance API

#### Binance Data coloumns: 
 columns=['timestamp', 'open', 'high', 'low', 'close', 'volume',  'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']

store in the databank 'crypto_data' in table 'btc_usdt_minutely'

### Database of Crypto
There is three table,
one table for the Coin,  one table named Price and the table Funding_rate

the Reference has col coin(varch) as PK
the Funding_rate has t+c(varch) as PK which is timestamp+coin name, coin(varch) as FK, time(data), landing(float), borrow(float)
the Price has  t+c(varch) as PK which is timestamp+coin name, coin(varch) as FK, time(data), open, high, low, close, volume, quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume.

