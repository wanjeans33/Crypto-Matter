# Crypto-Matter
Coorprate Company Project

## coingecko API
The coingecko API didnt offer historical minutely price data.
They can only offer minutely in 24h, hourly in 90 days and daily in 1 year.

## Binance API 
the Binance API have more detailable Trading Data in Cryptro. But It still has some limitaion. The maximual data row by each request is only 1000. If we want the minutely Data in 24h(one Day) We need to request twice.

The easiest solution is to use Binance API 2 request pre Day. 
every 12 hours with 720 rows data by one request.

Next step: establish the basic SQL databank to store the day
and automatiely request all data from Binance API