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

OR

python trading-bot.py -p 1800 -c BTC_XMR -n 5 -s 1491048000 -e 1491091200

OR

python "trading-bot(50200strategy).py" -p 1800 -c BTC_XMR -n 5 -s 1483228800 -e 1485863999

OR

python "trading-bot(50200strategy).py" -p 1800 -c USDT_BTC -n 5 -s 1483228800 -e 1523231999

# Based on the video series by Cryptocurrency Trading
https://www.youtube.com/watch?v=sVb-rRf--6s&list=PL2U3qLYtsXsT5QuFQUtxbfj62K3AiLOse
