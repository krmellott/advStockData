import yfinance as yahooFinance
import statistics
import numpy as np
import math

#author Kyle Mellott
riskFree = 0.008

#====================
# Purpose: Prints out the input prompt and collects user input
#====================
def inputPrompt():
    ticker = input("Please enter the Stock Ticker you'd like to look up: ")
    return ticker

#====================
# Purpose: Takes user input and finds the stock information on
#   Yahoo Finance. Returns 1 year of historical closing price data
#====================
def stockInfo(ticker):
    tickerHistory = list()
    stockData = yahooFinance.Ticker(ticker)
    print(stockData.info['shortName'])
    for value in stockData.history(period="1y")["Close"]:
        tickerHistory.append(value)
    return tickerHistory
    
#====================
# Purpose: Finds S&P 500 on Yahoo Finance
#   Returns 1 year of historical closing price data
#====================
def spyInfo():
    spyHistory = list()
    spyData = yahooFinance.Ticker("SPY")
    for value in spyData.history(period="1y")["Close"]:
        spyHistory.append(value)
    return spyHistory


#====================
# Uses tickerHistory to compute the average daily return and the
# previous 1 year return of the stock
#====================
def stockReturns(tickerHistory):
    sReturns = list()  #stock returns
    for i in range (0, 252):
       dailyRet = tickerHistory[i+1] - tickerHistory[i]
       dailyRet = (dailyRet / tickerHistory[i]) * 100
       sReturns.append(dailyRet)
    avgRet = statistics.mean(sReturns)
    annRet = ((tickerHistory[252] - tickerHistory[0])/tickerHistory[0]) * 100
    print("Average Daily Return (Previous Year): " + str(round(avgRet,2)) + "%")
    print("Annual Return: " + str(round(annRet,2)) + "%")
    stdDev = statistics.stdev(sReturns)
    print("Standard Deviation: " + str(round(stdDev,2)) + "%")
    return sReturns

def marketReturns(spyHistory):
    mReturns = list() #market returns
    for i in range (0, 252):
       dailyRet = spyHistory[i+1] - spyHistory[i]
       dailyRet = (dailyRet / spyHistory[i]) * 100
       mReturns.append(dailyRet)    
    return mReturns

def beta(sReturns,mReturns):
    sVar = statistics.stdev(sReturns)
    mVar = statistics.stdev(mReturns)
    corr = np.corrcoef(sReturns, mReturns)[0][1]
    beta = corr * (sVar / mVar)
    print("Beta (1Y): " + str(round(beta,3)))
    return beta

def alpha(sReturns, mReturns, sBeta):
    sExcess = list()
    mExcess = list()
    cAlpha = float(0)
    for i in range (0, 252):
        sExcess.append(sReturns[i] - riskFree)
        mExcess.append(mReturns[i] - riskFree)
    for i in range(0, 252):
        cAlpha = cAlpha + (sExcess[i] - (sBeta * mExcess[i]))
    print("Cumulative Alpha (1Y): " + str(round((cAlpha/100), 3)))


def sharpe(sReturns):
    avgRet = statistics.mean(sReturns)
    sRatio = (avgRet - riskFree) / (statistics.stdev(sReturns))
    sRatio = sRatio * math.sqrt(252)
    print("Sharpe Ratio: " + str(round(sRatio, 5)))
    
    
def main():
    ticker = inputPrompt()
    tickerHistory = stockInfo(ticker)
    spyHistory = spyInfo()
    sReturns = stockReturns(tickerHistory)
    mReturns = marketReturns(spyHistory)
    sBeta = beta(sReturns, mReturns)
    alpha(sReturns, mReturns, sBeta)
    sharpe(sReturns)
        
if __name__ == '__main__':
    main()

    
