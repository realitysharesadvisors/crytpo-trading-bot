import gemini
import time
import sys, getopt
import datetime
from poloniex import poloniex

def main(argv):
    period = 10
    pair = "BTCUSD"
    prices = []
    currentMovingAverage = 0
    lengthOfMA = 0
    startTime = False
    endTime = False
    historicalData = False
    tradePlaced = False
    typeOfTrade = False
    dataDate = ""
    orderNumber = ""
    net = []
    total = 100000
    bitcoin = 10

    '''
    Following code is for command line arguments. opts and args represents options
    such as -h, -p, -c etc. Those options with a colon following require an argument.
    -h for help
    -p, --period for period length
    -c, --currency for currency pair
    -n, --points for number of points for moving average
    -s is starttime for historical backtesting
    -e is endtime for historical backtesting
    '''
    try:
        opts, args = getopt.getopt(argv, "hp:c:n:s:e:", ["period=", "currency=", "points="])
    except getopt.GetoptError:
        print('tradingbot.py -p <period length> -c <currency pair> -n <period of moving average>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('tradingbot.py -p <period length> -c <currency pair> -n <period of moving average>')
            sys.exit()
        elif opt in ("-p", "--period"):
            if (int(arg) in [10, 300, 900, 1800, 7200, 14400, 86400]):
                period = arg
            else:
                print('Poloniex requires periods in 300,900,1800,7200,14400, or 86400 second increments')
                sys.exit(2)
        elif opt in ("-c", "--currency"):
            pair = arg
        elif opt in ("-n", "--points"):
            lengthOfMA = int(arg)
        elif opt in ("-s"):
            startTime = arg
        elif opt in ("-e"):
            endTime = arg

    # establish connection to gemini exchange, sandbox=True indicates sandbox
    r = gemini.PrivateClient("Public Key", "Private Key", sandbox=True)

    conn = poloniex('Public Key',
                    'Private Key')

    if (startTime):
            historicalData = r.get_trade_history("BTCUSD", since="17/06/2017")


    while True:

        #if we are doing a historical backtest
        if (startTime and historicalData):
            nextDataPoint = historicalData.pop(0)
            lastPairPrice = nextDataPoint['weightedAverage']
            dataDate = datetime.datetime.fromtimestamp(int(nextDataPoint['date'])).strftime('%Y-%m-%d %H:%M:%S')
        elif (startTime and not historicalData):
            exit()

        #if we are doing live trading
        else:
            currentValues = r.get_ticker(pair)
            lastPairPrice = float(currentValues["last"])
            dataDate = datetime.datetime.now()


        """
        This is the code that will actually execute the trades
        """
        if (len(prices) > 0):
            currentMovingAverage = sum(prices) / float(len(prices))
            previousPrice = prices[-1]
            if ((not tradePlaced) and (total > 0)):
            # if (not tradePlaced):
                if ((lastPairPrice > currentMovingAverage) and (lastPairPrice < previousPrice) and (bitcoin > 0)):
                    orderNumber = r.new_order(pair, "1", str(lastPairPrice), "sell")
                    print("SELL 1 BTC AT " + str(lastPairPrice * 1))
                    tradePlaced = True
                    typeOfTrade = "short"
                    priceSoldAt = lastPairPrice
                    total = total + (priceSoldAt * 1)
                    bitcoin = bitcoin - 1
                    print("total: " + str(total))

                elif ((lastPairPrice < currentMovingAverage) and (lastPairPrice > previousPrice)):
                    print("BUY 1 BTC AT " + str(lastPairPrice * 1))
                    orderNumber = r.new_order(pair, "1", str(lastPairPrice), "buy")
                    tradePlaced = True
                    typeOfTrade = "long"
                    priceBoughtAt = lastPairPrice
                    total = total - (priceBoughtAt * 1)
                    bitcoin = bitcoin + 1
                    print("total: " + str(total))

            elif (typeOfTrade == "short"):
                if (lastPairPrice < currentMovingAverage):
                    print("EXIT TRADE")
                    # conn.cancel(pair,orderNumber)
                    tradePlaced = False
                    typeOfTrade = False
            elif (typeOfTrade == "long"):
                if (lastPairPrice > currentMovingAverage):
                    print("EXIT TRADE")
                    # conn.cancel(pair,orderNumber)
                    tradePlaced = False
                    typeOfTrade = False
        else:
            previousPrice = 0

        print(
            "%s Period: %ss %s: %s Moving Average: %s" % (dataDate, period, pair, lastPairPrice, currentMovingAverage))

        prices.append(float(lastPairPrice))
        prices = prices[-lengthOfMA:]
        if (not startTime):
            time.sleep(int(period))

        if(bitcoin > 0):
            print ("bitcoin:", bitcoin)

if __name__ == "__main__":
    main(sys.argv[1:])


