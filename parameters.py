import time
import sys, getopt
import parameters
import datetime
import gemini
import requests
from poloniex import poloniex
import csv
import openpyxl
from openpyxl import Workbook
import tradingstrategy
import tradingbot

def getopts(argv):
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
            if (int(arg) in [300, 900, 1800, 7200, 14400, 86400]):
                tradingbot.period = arg
            else:
                print('Poloniex requires periods in 300,900,1800,7200,14400, or 86400 second increments')
                sys.exit(2)
        elif opt in ("-c", "--currency"):
            tradingbot.pair = arg
        elif opt in ("-n", "--points"):
            tradingbot.lengthOfMA = int(arg)
        elif opt in ("-s"):
            tradingbot.startTime = arg
        elif opt in ("-e"):
            tradingbot.endTime = arg
