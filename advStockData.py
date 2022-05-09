import yfinance as yahooFinance
import statistics

#author Kyle Mellott


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
    returns = list()
    for i in range (0, 252):
       dailyRet = tickerHistory[i+1] - tickerHistory[i]
       dailyRet = dailyRet / tickerHistory[i]
       returns.append(dailyRet)
    avgRet = statistics.mean(returns)
    avgRet = avgRet * 100
    annRet = ((tickerHistory[252] - tickerHistory[0])/tickerHistory[0])*100
    print("Average Daily Return: " + str(round(avgRet,2)) + "%")
    print("Annual Return: " + str(round(annRet,2)) + "%")


    
def main():
    ticker = inputPrompt()
    tickerHistory = stockInfo(ticker)
    spyHistory = spyInfo()
    stockReturns(tickerHistory)
    
        
if __name__ == '__main__':
    main()

    
