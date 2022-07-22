import numpy as np
from scipy.optimize import minimize

class MoneyOptimisationCalculator:
    def __init__(this, arrayOfNumbers, betAmount, minimumBet):
        this.bestOddsArray = arrayOfNumbers
        this.betAmountFloat = betAmount
        this.minimumBetFloat = minimumBet

    #Define function to calculate profit
    def calcProfit(this, arrayOfBestBets):
        bets_placed = []
        revenue_made = []
        current_bet_revenue = 0
        for current_index in range(len(this.bestOddsArray)):
            current_bet_revenue = arrayOfBestBets[current_index] * this.bestOddsArray[current_index]
            bets_placed.append(arrayOfBestBets[current_index])
            revenue_made.append(current_bet_revenue)
        revenue = min(revenue_made)
        profit = revenue - sum(bets_placed)
        return profit

    #Define function to calculate cost
    def calcRevenue(this, arrayOfBestBets):
        bets_placed = []
        revenue_made = []
        current_bet_revenue = 0
        for current_index in range(len(this.best_odds_array)):
            current_bet_revenue = arrayOfBestBets[current_index] * this.best_odds_array[current_index]
            bets_placed.append(arrayOfBestBets[current_index])
            revenue_made.append(current_bet_revenue)
        return min(revenue_made)

    #Calculates Cost   
    def calcCost(this, arrayOfBestBets):
        return sum(arrayOfBestBets)

    #Define objective function for optimisation
    def objective(this, arrayOfBestBets):
        return -this.calcProfit(arrayOfBestBets)

    #Define constraint for optimisation
    def constraint(this,x):
        return this.bet_amount_float - this.calcCost(x)

    def betting_optimisation(this):
        bets_placed = []
        best_optimisation = []
        best_optimisation_profit = -999999
        #load constraints into dictionary form
        cons = ({'type': 'ineq', 'fun': this.constraint})

        bnds = ()
        for current_bounds in range(len(this.bestOddsArray)):
            bnds += (this.minimumBetFloat, this.betAmountFloat),

        currentBetGuess = this.minimumBetFloat + 1
        #looping till outside bounds
        while (currentBetGuess < this.betAmountFloat):
            #set initial guess values
            bet_best_guess = []
            for current_index in range(len(this.bestOddsArray)):
                bet_best_guess.append(currentBetGuess)
            #load guess values
            x0 = np.array(bet_best_guess)
            #Call solver to minimize the objective function given the constraints
            sol = minimize(this.objective,x0,method='SLSQP',bounds=bnds,constraints=cons,options={'disp':False})
            #Retrieve optimized profit and bets
            xOpt = sol.x

            #Round it
            actual_bets = []
            for x_number in range(len(xOpt)):
                actual_bets.append(round(xOpt[x_number], 2))

            profitOpt = -sol.fun
            #Calculate surface
            costOpt = this.calcCost(actual_bets)
            revenueOpt = this.calcRevenue(actual_bets)
            if (best_optimisation_profit < (revenueOpt - costOpt)):
                best_optimisation = actual_bets
            currentBetGuess += (this.betAmountFloat/20)
        return best_optimisation

