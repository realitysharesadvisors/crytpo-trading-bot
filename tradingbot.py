import time
import sys, getopt
import datetime
import gemini
import requests
from poloniex import poloniex ##Convenient python wrapper##

def main(argv):
    period = 10
    pair = "USDT_BTC"
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
    total = 100000
    bitcoin = 10

    # r = gemini.PrivateClient("API Key", "Private Key", sandbox=True)
    # print(r)

    try:
        opts, args = getopt.getopt(argv, "hp:c:n:s:e:", ["period=", "currency=", "points="])
    except getopt.GetoptError:
        print('trading-bot.py -p <period length> -c <currency pair> -n <period of moving average>')
        sys.exit(2)

    ##Parse arguments##
    for opt, arg in opts:
        if opt == '-h':
            print('trading-bot.py -p <period length> -c <currency pair> -n <period of moving average>')
            sys.exit()
        elif opt in ("-p", "--period"):
            if (int(arg) in [300, 900, 1800, 7200, 14400, 86400]):
                period = arg
            else:
                print('Poloniex requires periods in 300,900,1800,7200,14400, or 86400 second increments')
                sys.exit(2)
        elif opt in ("-c", "--currency"):
            pair = arg
        elif opt in ("-n", "--points"):
            lengthOfMA = int(arg) ##Number of points used to calc Moving Average(MA)##
        elif opt in ("-s"):
            startTime = arg ##Has to be in UNIX Timestamp##
        elif opt in ("-e"):
            endTime = arg ##Has to be in UNIX Timestamp##

    ##Connect with poloniex with its API keys##
    conn = poloniex('API Key',
                    'Private Key')

    if (startTime):
        ##Returns candlestick chart data##
        historicalData = conn.api_query("returnChartData", {"currencyPair": pair, "start": startTime, "end": endTime, "period": period})
        # log = open("compare.txt", "w")
        # print(historicalData, file = log)

    while True:
        ##If startTime exists, this means that we are retrieving historical data##
        if (startTime and historicalData):
            nextDataPoint = historicalData.pop(0)
            lastPairPrice = nextDataPoint['weightedAverage']
            dataDate = datetime.datetime.fromtimestamp(int(nextDataPoint['date'])).strftime('%Y-%m-%d %H:%M:%S')
        ##Error for wrong period of time##
        elif (startTime and not historicalData):
            exit()
        ##Live data##
        else:
            currentValues = conn.api_query("returnTicker")
            lastPairPrice = currentValues[pair]["last"]
            dataDate = datetime.datetime.now()

        if (len(prices) > 0):
            currentMovingAverage = sum(prices) / float(len(prices))
            previousPrice = prices[-1] ## Latest price ##
            if (not tradePlaced):
                ##If price > MA and price < exactly previous one##
                if ((lastPairPrice > currentMovingAverage) and (lastPairPrice < previousPrice)):
                    print("SELL 1 BTC at " + str(lastPairPrice))
                    #orderNumber = conn.sell(pair, lastPairPrice, .01)
                    total = total + lastPairPrice
                    bitcoin = bitcoin - 1
                    print("Total funds: " + str(total))
                    print("Total bitcoin: " + str(bitcoin))
                    tradePlaced = True
                    typeOfTrade = "short"
                ##If price < MA and price > exactly previous one##
                elif ((lastPairPrice < currentMovingAverage) and (lastPairPrice > previousPrice)):
                    print("BUY ORDER")
                    #orderNumber = conn.buy(pair, lastPairPrice, .01)
                    print("BUY 1 BTC at " + str(lastPairPrice))
                    total = total - lastPairPrice
                    bitcoin = bitcoin + 1
                    print("Total funds: " + str(total))
                    print("Total bitcoin: " + str(bitcoin))
                    tradePlaced = True
                    typeOfTrade = "long"
            elif (typeOfTrade == "short"):
                if (lastPairPrice < currentMovingAverage):
                    print("EXIT TRADE")
                    #conn.cancel(pair, orderNumber)
                    tradePlaced = False
                    typeOfTrade = False
            elif (typeOfTrade == "long"):
                if (lastPairPrice > currentMovingAverage):
                    print("EXIT TRADE")
                    #conn.cancel(pair, orderNumber)
                    tradePlaced = False
                    typeOfTrade = False
        else:
            previousPrice = 0

        ##timestamp##
        print(
            "%s Period: %ss %s: %s Moving Average: %s" % (dataDate, period, pair, lastPairPrice, currentMovingAverage))

        prices.append(float(lastPairPrice))
        prices = prices[-lengthOfMA:] ##Last lengthOfMA prices##
        ##Sleep for real time data, no sleep for historical data##
        if (not startTime):
            time.sleep(int(period))

if __name__ == "__main__":
    main(sys.argv[1:])
