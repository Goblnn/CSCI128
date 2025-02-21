# Isaac Lane
# CSCI 128 - Section K
# Assessment 6
# References: no one
# Time: 1 hour

# All inputs and list creations

rounds = int(input("NUM ROUNDS> "))
numStocks = int(input("NUM STOCKS> "))

stocks = []
invested = []
periods = []

for i in range(numStocks):
    stocks.append(input("TICKER> "))
    invested.append(float(input("INITIAL INVESTMENT> ")))

initialInvested = invested

i = 0
for i in range(rounds):
    periods.append(input(f"SIM PERIOD {i + 1}> "))

ignoreList = []

# Main Calculations

i = 0
for i in range(len(periods)):
    period = periods[i].split(";")

    for p in range(numStocks):
        stock = stocks[p]

        if(stock in ignoreList):
            continue

        stockIndex = period.index(stock)
        stockChange = float(period[stockIndex + 1])

        invested[p] *= 1 + stockChange

        if(invested[p] <= 0):
            ignoreList.append(stock)
            invested[p] = 0

# Final calculations and outputs

if(numStocks == 0):
    print(f"OUTPUT Overall: 0.00 -> 0.00 0.00%")
elif(rounds == 0):
    stockPriceOriginal = 0

    i = 0
    for i in range(numStocks):
        stockPriceOriginal += initialInvested[i]

    for i in range(numStocks):
        stock = stocks[i]

        print(f"OUTPUT {stock}: Gain 0.00%")
    
    print(f"OUTPUT Overall: {stockPriceOriginal:.2f} -> {stockPriceOriginal:.2f} 0.00%")
else:
    stockPriceOriginal = 0

    i = 0
    for i in range(numStocks):
        stockPriceOriginal += initialInvested[i]

    stockPriceFinal = 0

    i = 0
    for i in range(numStocks):
        stock = stocks[i]
        stockPrice = invested[i]
        oldStockPrice = initialInvested[i]

        percentChange = (stockPrice / oldStockPrice - 1) * 100

        stockPriceFinal += stockPrice

        if(percentChange >= 0):
            print(f"OUTPUT {stock}: Gain {percentChange:.2f}%")
        else:
            print(f"OUTPUT {stock}: Loss {percentChange:.2f}%")

    totalChangePercent = (stockPriceFinal / stockPriceOriginal - 1) * 100

    print(f"OUTPUT Overall: {stockPriceOriginal:.2f} -> {stockPriceFinal:.2f} {totalChangePercent:.2f}%")