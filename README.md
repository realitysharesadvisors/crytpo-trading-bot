# crytpo-trading-bot
The bot accepts the following command line options/arguments:

-h 
-p, --period
-c, --currency
-n, --points
-s
-e

which correlate with

help,
time period
currency pair
points for SMA
start time (for historical backtest)
and end time (for historical backtest)

respectively.

An example of running the program would be:

python trading-bot.py -p 14400 -c BTC_USDT -n 15


