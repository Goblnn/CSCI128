# Code Review 6 Stock Market

# Team Members: Isaac Lane, Corbin Mitchell, Edward Villacres

def run():
    n_periods = int(input("NUM ROUNDS> "))
    n_companies = int(input("NUM STOCKS> "))
    ticker_list = []
    invest_list = []
    in_invest = []

    # company info
    # for company in range(n_companies):
    #     ticker_list.append(input("TICKER"))
    #     invest = float(input("INITIAL INVESTMENT"))
    #     in_invest.append(invest)
    #     invest_list.append(invest)
    
    loop = 0
    while(loop < n_companies):
        ticker_list.append(input("TICKER"))
        invest = float(input("INITIAL INVESTMENT"))
        in_invest.append(invest)
        invest_list.append(invest)
        loop += 1


    # do the simulation
    for period in range(n_periods):
        simulation = input(f"SIM PERIOD {period+1}> ").split(";")
        for i in range(len(ticker_list)):
            comp_loc = simulation.index(ticker_list[i])
            change = invest_list[i] * float(simulation[comp_loc + 1])
            if (invest_list[i] + change) <= 0:
                change = -invest_list[i]
            
            invest_list[i] += change

    # output results
    end_val = 0
    start_val = 0
    result = 0
    if(n_companies != 0):
        for i in range(n_companies):
            if(in_invest[i] != 0):
                result = (invest_list[i] / in_invest[i]) - 1
            end_val += invest_list[i]
            start_val += in_invest[i]

            if result >= 0:
                print(f"OUTPUT {ticker_list[i]}: Gain {result*100:.2f}%")
            else:
                print(f"OUTPUT {ticker_list[i]}: Loss {result*100:.2f}%")

        result = (end_val / start_val) - 1
    print(f"OUTPUT Overall: {start_val:.2f} -> {end_val:.2f} {result*100:.2f}%")

run()