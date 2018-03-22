import sys, getopt

from botchart import BotChart
from botstrategy import BotStrategy

def main(argv):
	chart = BotChart("poloniex","USDT_BTC",86400,backtest=True)

	strategy = BotStrategy()

	for candlestick in chart.getPoints():
		strategy.tick(candlestick)

if __name__ == "__main__":
	main(sys.argv[1:])