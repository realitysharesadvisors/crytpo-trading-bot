import time
import sys, getopt
import datetime
# import gemini
import requests
from poloniex import poloniex ##Convenient python wrapper##

def main(argv):
    period = 10
    pair = "USDT_BTC"
    prices = []
    currentMovingAverage = 0
    currentFiftyMovingAverage = 0
    currentTwoHundredMovingAverage = 0
    lengthOfMA = 0
    startTime = False
    endTime = False
    historicalData = False
    tradePlaced = False
    typeOfTrade = False
    dataDate = ""
    orderNumber = ""
    dataPoints = []
    fiftyMaPoints = []
    twoHundredMaPoints = []
    total = 100000
    bitcoin = 10
    fifty = 50
    twohundred = 200

    # r = gemini.PrivateClient("JBCBbwEmXfD6IwS6Q4WN", "2YzrK8cq5jCRs8r8QKLKUtDDJxqV", sandbox=True)
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
    conn = poloniex('OICTWNLZ-NG2ATAQN-S3DYCUWH-QGWMPXD3',
                    '0348b3b5932f49b1e84feeacbec88a8b9eb0770d11fe553515f6a946b8b23eb2abe9748ee06417f1fd27310759e3b6535782c03de75c3499f42c714b0b6530a5')

    output = open("output.html",'w')
    output.truncate()
    output.write("""
        <html>
            <head>
                <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
                <script type="text/javascript">
                    google.charts.load('current', {'packages':['line']});
                    google.charts.setOnLoadCallback(drawChart);
                    function drawChart(){
                        var data = new google.visualization.DataTable();
                        data.addColumn('string', 'time');
                        data.addColumn('number', 'value');
                        data.addColumn('number', '50 MA');
                        data.addColumn('number', '200 MA');
                        data.addRows([""")


    if (startTime):
        ##Returns candlestick chart data##
        historicalData = conn.api_query("returnChartData", 
        	{"currencyPair": pair, "start": startTime, "end": endTime, "period": period})
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
            for point, fiftyma, twohundma in zip(dataPoints, fiftyMaPoints, twoHundredMaPoints):
                output.write("['" + point['date'] + "'," + point['price'] + "," + fiftyma['price'] + "," + twohundma['price'])
                output.write("],\n")
            output.write("""]);
                var formatter = new google.visualization.NumberFormat({
                    pattern: '##.######'
                });

                for (var i = 1; i < data.getNumberOfColumns(); i++) {
                    formatter.format(data, i);
                }

                var options = {title: 'Price Chart', legend: { position: 'bottom' }};
                var chart = new google.charts.Line(document.getElementById('curve_chart'));
                chart.draw(data, options);}</script>
                </head>
                <body>
                    <div id="curve_chart" style="width: 100%; height: 100%"></div>
                </body>
                </html>""")
            exit()
        ##Live data##
        else:
            currentValues = conn.api_query("returnTicker")
            lastPairPrice = currentValues[pair]["last"]
            dataDate = datetime.datetime.now()

        dataPoints.append({'date':dataDate, 'price': str(lastPairPrice)})

        if (len(prices) > 0):
            currentFiftyMovingAverage = sum(fiftyprices) / 50.0
            currentTwoHundredMovingAverage = sum(twohundredprices) / 200.0
            previousPrice = prices[-1] ## Latest price ##
            # if (not tradePlaced):
            #     ##If price > MA and price < exactly previous one##
            #     if ((previousPrice < currentMovingAverage) and (currentMovingAverage < lastPairPrice) and (previousPrice < lastPairPrice)):
            #         print("\nSELL 1 BTC at " + str(lastPairPrice))
            #         #orderNumber = conn.sell(pair, lastPairPrice, .01)
            #         total = total + lastPairPrice
            #         bitcoin = bitcoin - 1
            #         print("Total funds: " + str(total))
            #         print("Total bitcoin: " + str(bitcoin))
            #         # tradePlaced = True
            #         # typeOfTrade = "short"
            #     ##If price < MA and price > exactly previous one##
            #     elif ((previousPrice > currentMovingAverage) and (currentMovingAverage > lastPairPrice) and (previousPrice > lastPairPrice) and (bitcoin > 0)):
            #         print("\nBUY ORDER")
            #         #orderNumber = conn.buy(pair, lastPairPrice, .01)
            #         print("BUY 1 BTC at " + str(lastPairPrice))
            #         total = total - lastPairPrice
            #         bitcoin = bitcoin + 1
            #         print("Total funds: " + str(total))
            #         print("Total bitcoin: " + str(bitcoin))
                    # tradePlaced = True
                    # typeOfTrade = "long"
            # elif (typeOfTrade == "short"):
            #     if (lastPairPrice < currentMovingAverage):
            #         print("EXIT TRADE")
                    #conn.cancel(pair, orderNumber)
                    # tradePlaced = False
                    # typeOfTrade = False
            # elif (typeOfTrade == "long"):
            #     if (lastPairPrice > currentMovingAverage):
            #         print("EXIT TRADE")
                    #conn.cancel(pair, orderNumber)
                    # tradePlaced = False
                    # typeOfTrade = False
        else:
            previousPrice = 0

        fiftyMaPoints.append({'date':dataDate, 'price': str(currentFiftyMovingAverage)})
        twoHundredMaPoints.append({'date':dataDate, 'price': str(currentTwoHundredMovingAverage)})

        ##timestamp##
        print(
            # "%s Period: %ss %s: %s Moving Average: %s" % (dataDate, period, pair, lastPairPrice, currentMovingAverage))
            "Previousprice: %s , %s: %s \nFifty Moving Average: %s \nTwo Hundred Moving Average: %s" % (previousPrice, pair, lastPairPrice, currentFiftyMovingAverage, currentTwoHundredMovingAverage))

        prices.append(float(lastPairPrice))
        fiftyprices = prices[-50:] ##Last lengthOfMA prices##
        twohundredprices = prices[-200:] ##Last lengthOfMA prices##
        ##Sleep for real time data, no sleep for historical data##
        if (not startTime):
            time.sleep(int(period))

        print("Total funds: " + str(total))
        print("Total bitcoin: " + str(bitcoin) + "\n")
if __name__ == "__main__":
    main(sys.argv[1:])
    
