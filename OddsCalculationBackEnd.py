#-----------------------------------------------------------
#
# Odds Calculator
#
# The Python script below reads the contents of a website, sorts
# it into useful arrays and then displays it
from urllib.request import Request, urlopen
from re import findall, finditer, MULTILINE, DOTALL
from copy import deepcopy
from scipy.optimize import minimize
from tkinter import messagebox
from datetime import datetime
from win10toast import ToastNotifier
import numpy as np
import os
import sys, time, msvcrt
from playsound import playsound

class BestHorseOdds:
    def __init__(this):
        this.output_odds_array = []
        this.best_odds_array = []
        this.url = 'https://www.punters.com.au/odds-comparison/horse-racing/all/';
        #this.url = 'https://www.punters.com.au/odds-comparison/greyhounds/all/';
        this.content_file = ""

        this.record_results = "No"
        this.no_tote = "No"
        this.auto_refresh_int = 0
        this.bet_amount_float = 300
        this.minimum_bet_float = 0
        this.notifications_bool = 0

    #Opens the webpage
    def open_web_page(this, page_to_open):
        req = Request(page_to_open, headers={'User-Agent': 'Mozilla/5.0'})
        #Open the target URL
        web_page = urlopen(req)
        try:
            #Extract webpage contents
            web_page_bytes = web_page.read()
            web_page_contents = web_page_bytes.decode('ASCII', 'backslashreplace')
            #Close the page
            web_page.close()
            return web_page_contents
        except OSError:
            return 'Connect to Internet'

    def print_table(this, table):
        table_string = ''
        longest_cols = [
            (max([len(str(row[i])) for row in table]) + 1)
            for i in range(len(table[0]))
        ]
        row_format = "".join(["{:>" + str(longest_col) + "}" for longest_col in longest_cols])
        for row in table:
            table_string = table_string + row_format.format(*row) + '\n'
        return table_string

    #Define function to calculate profit
    def calcProfit(this, x):
        bets_placed = []
        revenue_made = []
        current_bet_revenue = 0
        for current_index in range(len(this.best_odds_array)):
            current_bet_revenue = x[current_index] * this.best_odds_array[current_index]
            bets_placed.append(x[current_index])
            revenue_made.append(current_bet_revenue)
        revenue = min(revenue_made)
        profit = revenue - sum(bets_placed)
        return profit

    #Define function to calculate cost
    def calcRevenue(this, x):
        bets_placed = []
        revenue_made = []
        current_bet_revenue = 0
        for current_index in range(len(this.best_odds_array)):
            current_bet_revenue = x[current_index] * this.best_odds_array[current_index]
            bets_placed.append(x[current_index])
            revenue_made.append(current_bet_revenue)
        return min(revenue_made)

    #Calculates Cost   
    def calcCost(this, x):
        return sum(x)

    #Define objective function for optimisation
    def objective(this,x):
        return -this.calcProfit(x)

    #Define constraint for optimisation
    def constraint(this,x):
        return this.bet_amount_float - this.calcCost(x)


    def betting_optimisation(this,best_odds_array1, best_odds_and_names, racers_name_optim, name_of_race, table_of_race_odds1):
        bettingOptimisationString = ""
        bets_placed = []
        best_optimisation = []
        best_optimisation_profit = -999999
        #load constraints into dictionary form
        cons = ({'type': 'ineq', 'fun': this.constraint})

        bnds = ()
        for current_bounds in range(len(best_odds_array1)):
            bnds += (this.minimum_bet_float, this.bet_amount_float),

        current_append = this.minimum_bet_float + 1
        #looping till outside bounds
        while (current_append < this.bet_amount_float):
            #set initial guess values
            bet_best_guess = []
            for current_index in range(len(best_odds_array1)):
                bet_best_guess.append(current_append)
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
            current_append += (this.bet_amount_float/20)
            

        #Display Optimisation
        export_horse_company_bet_table = []
        export_horse_company_bet_table.append(["     Horse Name:","     Betting Company:", "     Best Odds:","     Amount on Horse:", "     Payout:"])
        for current_bet_index in range(len(best_optimisation)):
            export_horse_company_bet_table.append([str(racers_name_optim[current_bet_index]),\
                                                   str(best_odds_and_names[current_bet_index][0]),\
                                                   str(best_odds_and_names[current_bet_index][1]),\
                                                   str(best_optimisation[current_bet_index]),
                                                   str(round(float(best_optimisation[current_bet_index])\
                                                             * float(best_odds_and_names[current_bet_index][1]), 2))])
        bettingOptimisationString += this.print_table(export_horse_company_bet_table) + '\n'
        bettingOptimisationString += "Profit: " + str(round(revenueOpt - costOpt, 2)) + "\n"
        bettingOptimisationString += "Revenue: " + str(round(revenueOpt, 2)) + "\n"
        bettingOptimisationString += "Cost: " + str(round(costOpt, 2)) + "\n"

        returnPercent = 0
        if (costOpt == 0):
            returnPercent = round(100 * (revenueOpt - costOpt)/1,2)
        else:
            returnPercent = round(100 * (revenueOpt - costOpt)/costOpt,2)

        bettingOptimisationString += "Return: " + str(returnPercent) + "%" + "\n"
        #this.send_notification(this.notifications_bool, name_of_race, returnPercent)
        #print(returnPercent)
        if ((this.show_returns_float != 0.0) & (this.show_returns_float > returnPercent)):
                bettingOptimisationString = ""
                
        if ((this.record_results != "No") & (round(revenueOpt - costOpt, 2) > 0)):
            right_now = datetime.now()
            this.save_table_without_overwrite(table_of_race_odds1, name_of_race)
            this.save_table_without_overwrite(export_horse_company_bet_table, "Bets")
            content_str = "<h2>" + str(right_now) + "</h2>" + "<br>Profit: " + str(round(revenueOpt - costOpt, 2)) + "<br>Revenue: " + str(round(revenueOpt, 2)) + "\
    <br>Cost: " + str(round(costOpt, 2)) + "<br>Return: " + str(round(100 * (revenueOpt - costOpt)/costOpt,2)) + "%"
            text_file = open('ConfirmedWins.html', 'r', encoding = 'UTF-8')
            content_file = text_file.readline()
            text_file.close()
            content_file = content_file[:len(content_file) - 18] + content_str + content_file[len(content_file) - 18:]
            text_file = open('ConfirmedWins.html', 'w', encoding = 'UTF-8')
            text_file.write(content_file)
            text_file.close()
        return bettingOptimisationString

    #Best odds
    def bestOdds(this,current_race_odds):
        export_best_odds = []
        export_best_odds_without_name = []
        #loops through the race for each horse
        for horse_array_number in range(len(current_race_odds)):
            horse_best_odds = []
            #loops through each companies odds for that horse
            for each_company_odds in current_race_odds[horse_array_number]:
                #if there is a blank
                if (each_company_odds[1] != ''):
                    horse_best_odds.append(float(each_company_odds[1]))
                else:
                    horse_best_odds.append(0)
            #print(horse_best_odds)
            if (horse_best_odds != []):
                maximum_odd = max(horse_best_odds)
                #print(maximum_odd)
                loop_max_odd = 0
                #end loop when the maximum is hit
                while (maximum_odd != horse_best_odds[loop_max_odd]):
                    loop_max_odd += 1
                
                if (current_race_odds[horse_array_number][loop_max_odd][1] != ''):
                    #export either with or without names (use tupling to do both)
                    export_best_odds.append(current_race_odds[horse_array_number][loop_max_odd])
                    export_best_odds_without_name.append(float(current_race_odds[horse_array_number][loop_max_odd][1]))
                else:
                    export_best_odds.append(['None', float(0)])
                    export_best_odds_without_name.append(float(0))
        #print(export_best_odds)
        return (export_best_odds_without_name, export_best_odds)

    def save_table_without_overwrite(this,table, table_name):
        
            text_file = open('ConfirmedWins.html', 'r', encoding = 'UTF-8')
            content_file = text_file.readline()
            text_file.close()
            content_str = ""
            content_str += "<br> <h2> " + str(table_name) + " </h2> <br> <table class='center'>"
            for row in table:
                content_str += "<tr>"
                for element in row:
                    content_str += "<td> " + str(element) + " </td>"
                content_str += "</tr>"
            content_str += "</table>      "
            #print(content_file)
            content_file = content_file[:len(content_file) - 18] + content_str + content_file[len(content_file) - 18:]
            #content_file = content_file[2:] + "Cancer" + content_file[:2]
            text_file = open('ConfirmedWins.html', 'w', encoding = 'UTF-8')
            text_file.write(content_file)
            text_file.close()

    def create_new_record(this):
        html_file = open('ConfirmedWins.html', 'w', encoding = 'UTF-8')
        html_file.write("<html> <head> <title> Confirmed Wins </title> <style>\
    body {background-color: white; text-align:center}\
    p {margin-left:5%; margin-right:5%; text-align:center}\
    h1 {margin-left:5%; margin-right:5%; text-align:center}\
    h2 {margin-left:5%; margin-right:5%; text-align:center}\
    img.center {display:block; margin-left:auto; margin-right:auto;}\
    table.center {margin-left: auto; margin-right:auto}\
    table, th, td {border: 1px solid black; text-align:center} </style>\
    </head> <body>      </body> </html>")
        html_file.close()
        
    def record_results_set(this, recordInput):
        this.record_results = recordInput
        print("Record Results: " + str(this.record_results))

    def url_set(this, urlInput):
        this.url = recordInput
        print("URL: " + str(this.url))

    def include_tote_bets_set(this, toteBetInput):
        this.no_tote = toteBetInput
        print("Tote: " + str(this.no_tote))

    def auto_refresh_set(this, autoRefreshInput):
        this.auto_refresh_int = int(autoRefreshInput)
        print("Auto Refresh: " + str(this.auto_refresh_int))

    def bet_amount_set(this, betAmountInput):
        this.bet_amount_float = float(betAmountInput)
        print("Bet Amount: " + str(this.bet_amount_float))

    def minimum_bet_set(this, minimumBetInput):
        this.minimum_bet_float = float(minimumBetInput)
        print("Minimum Bet: " + str(this.minimum_bet_float))

    def show_returns_set(this, showReturnsInput):
        this.show_returns_float = float(showReturnsInput)
        print("Show Returns: " + str(this.show_returns_float))

    def send_notifications_set(this, notificationsInput):
        this.notifications_bool = bool(notificationsInput)
        print("Send Notifications: " + str(this.notifications_bool))
        
    def send_notification(this, notificationsBool, race_name, return_percent):
        if (notificationsBool == True and return_percent > this.show_returns_float):
            toaster = ToastNotifier()
            toaster.show_toast("Horse Odds Notification", race_name + " " + str(return_percent) + "%")

    def set_all_variables(this, recordInput, betAmountInput, minimumBetInput, showReturnsInput, notificationsInput):
        this.record_results = recordInput
        this.no_tote = toteBetInput
        this.bet_amount_float = float(betAmountInput)
        this.minimum_bet_float = float(minimumBetInput)
        this.show_returns_float = float(showReturnsInput)
        this.notifications_bool = bool(notificationsInput)

    def createNewUrls(this, websiteText):
        findLocationRegex = '"location": "([A-Za-z0-9\- ]+)"}'
        findDateRegex = '{"day": "([A-Za-z0-9\- ]+)",'
        findLocation = findall(findLocationRegex, websiteText)
        #url = "https://www.punters.com.au/odds-comparison/"
        #url += ""
        print(findLocation)
        
    def run_on_press(this):
        #Hopefully the neat output data array
        organised_lines_array = []

        #Keeps track of all the races
        #race_string_find = '</a>[ \\n\\r]+</div>[ \\n\\r]+</div>[ \\n\\r]+<div class="oc-table\-body">'
        #race_regex = '<div class="oc-table-body">[^<]+<div class="oc-table-tr gutter" id="[A-Za-z_0-9]+">[^<]+<div[ \\n\\r]+ class'
        #race_string_find = '</a>\n              </div>\n          </div>\n\n\n          <div class="oc-table-body">'
        race_string_find = '\n\n          <div class="oc-table-body">\n              <div class="oc-table-tr gutter" id="ocSelection_'
        race_name_regex = 'name-full">([A-Za-z0-9\- ]+)</div>'


        #race variables
        number_of_races = 0
        current_race_number = 0
        previous_race_number = 0
        current_race_string = ''
        current_race_array = []

        #line regex
        new_line_regex = '<div class="border-line"></div>[^<]*</div>[^<]*<div class="oc-table-tr gutter" id="ocSelection_'
        new_line_string_find = '<div class="border-line"></div>\n              </div>\n              <div class="oc-table-tr gutter" id="ocSelection_'
        # Read the contents of the web page as a character string,
        # suitable for printing to an ASCII-only Tk widget, using
        # backslashes to "escape" any non-ASCII characters

        web_page_text = this.open_web_page(this.url)
        new_text = findall(race_string_find, web_page_text)
        #Keeps track of all the line beginnings
        line_numbers = findall(new_line_regex, web_page_text)

        #Racers name
        racers_name_regex = '&nbsp;</span>[ \\n\\r]+([\'A-Za-z0-9\- ]+)[ \\n\\r]+<'
        racers_name_array = []
        

        #Race Time
        race_time_regex = 'fullDateYear" data-utime="(1[\d]+)"'
        
        #Bet numbers
        bet_number_regex = 'data-key="[0-9]+\-([^"]+)" data-event="[^"]+">(?:[ \\n\\r]+</div>|[^>]+>[^>]+>bet</span>([0-9\.]+))'#|sign ([A-Za-z0-9 ]+)">bet</span>([0-9\.]+)'

        #Line number variables
        number_of_lines = 0
        current_line_number = 0
        previous_line_number = 0
        number_locations = [0]
        current_line_string = ''

        #Find the racenames
        race_names = findall(race_name_regex, web_page_text)

        this.createNewUrls(web_page_text)

        #Find the race times
        race_times = findall(race_time_regex, web_page_text)
        #print(race_times)

        #Output reset
        this.output_odds_array = []

        if (this.record_results == "Yes and Overwrite"):
            this.create_new_record()

        #While there are still more races
        while web_page_text.find(race_string_find, current_race_number) != -1:
            previous_race_number = current_race_number
            #current string location 
            current_race_number = web_page_text.find(race_string_find, current_race_number + 5)
            
            if previous_race_number == 0:
                number_of_races = 0
                current_race_string = web_page_text[previous_race_number: current_race_number]
                racers_name_array.append(findall(racers_name_regex, current_race_string))
                
            else:
                if current_race_number == -1:
                    current_race_string = web_page_text[previous_race_number: len(web_page_text)]
                    #organised_lines_array.append(findall('sign ([A-Za-z0-9 ]+)">bet</span>([0-9]+)', current_race_string))  
                else:
                    current_race_string = web_page_text[previous_race_number: current_race_number]
                    racers_name_array.append(findall(racers_name_regex, current_race_string))
                    #organised_lines_array.append(findall('sign ([A-Za-z0-9 ]+)">bet</span>([0-9]+)', current_race_string))
                                
                while web_page_text.find(new_line_string_find, current_line_number) != -1:
                    #finds the current line location and prints it
                    previous_line_number = current_line_number
                    current_line_number = current_race_string.find(new_line_string_find, current_line_number + 100)
                    ###########print(current_line_number)

                    number_locations.append(current_line_number)

                    #Checks if previous line is 0 to stop errors
                    if previous_line_number == 0:
                        number_of_lines = 0
                        current_line_string = current_race_string[previous_line_number: current_line_number]
                        current_race_array.append(findall(bet_number_regex, current_line_string))

                    #Updates the current string and uses it to find the numbers and companies within it
                    elif current_line_number == -1:
                        current_line_string = current_race_string[previous_line_number: len(web_page_text)]
                        current_race_array.append(findall(bet_number_regex, current_line_string))  
                    else:
                        current_line_string = current_race_string[previous_line_number: current_line_number]
                        current_race_array.append(findall(bet_number_regex, current_line_string))  

                    number_of_lines += 1
                #Appends output array with the current race then clears the race array
                #print(str(current_race_array) + "\n\n\n")
                bridge_array = deepcopy(current_race_array)
                organised_lines_array.append(bridge_array)
                current_race_array.clear()
                #print(organised_lines_array)
                previous_line_number = 0
                current_line_number = 0

            number_of_races += 1
            
        #Prints out the race

        #List of maximums
        list_of_maximums = []

        #print()
        #Creates a nice list to put into table displayer
        for race in range(len(organised_lines_array)):
            #try:
            #deletes lay bet and totes
            for line in range(len(organised_lines_array[race])):
                del organised_lines_array[race][line][18:]
                if (this.no_tote == "No"):
                    del organised_lines_array[race][line][:3]
                if (this.no_tote == "Just Display Totes"):
                    del organised_lines_array[race][line][3:]
                if (this.no_tote == "Yes"):
                    del organised_lines_array[race][line][:2]
            table_of_race_odds = []
            race_list_of_maximums = []
            #prints race name
            current_race_best_odds_string = "Race: " + str(race + 1) + " - " + str(race_names[race]) + "\n"
            #Print time
            current_race_time = datetime.utcfromtimestamp(int(race_times[race]))
            #print(current_race_time)
            current_race_hour = (current_race_time.hour - 2) % 24
            current_race_time = current_race_time.replace(hour = int(current_race_hour))
            current_race_time_string = current_race_time.strftime('%Y-%m-%d %H:%M:%S')
            current_race_best_odds_string +=  current_race_time_string + "\n"
            #prints companies
            temporary_company_names_array = []
            for element in range(len(organised_lines_array[race][0])):
                temporary_company_name_string = organised_lines_array[race][0][element][0]
                temporary_company_name_string = temporary_company_name_string[:temporary_company_name_string.index("-")]
                temporary_company_names_array.append(temporary_company_name_string)
            temporary_company_names_array.insert(0, "Horses ")
            table_of_race_odds.append(temporary_company_names_array)

            #prints each racer
            for line in range(len(organised_lines_array[race])):
                temporary_line_array = [] 
                #prints each odd from companies    
                for element in range(len(organised_lines_array[race][line])):
                    temporary_line_array.append(organised_lines_array[race][line][element][1])
                table_of_race_odds.append(temporary_line_array)
                #Calculates maxiumum
                race_list_of_maximums.append(max(temporary_line_array))
                #Adds the horse name
                #print(len(racers_name_array))
                temporary_line_array.insert(0, str(line + 1) + str(racers_name_array[race][line][:8]))
                
            #prints out more important information
            list_of_maximums.append(race_list_of_maximums)
            best_odds_current_race = this.bestOdds(organised_lines_array[race])
            this.best_odds_array = best_odds_current_race[0]
            best_odds_array_names = best_odds_current_race[1]
            
            bettingOpString = this.betting_optimisation(this.best_odds_array, best_odds_array_names, racers_name_array[race], race_names[race], table_of_race_odds)
                
            current_race_best_odds_string += bettingOpString
            
            if (bettingOpString != ""):
                this.output_odds_array.append(current_race_best_odds_string)
                if (this.notifications_bool == True):
                    playsound('audio.mp3')
            #except:
             #   print("Something Wrong")
                

        #bet_numbers = findall('sign ([A-Za-z0-9 ]+)">bet</span>([0-9]+)', web_page_text)
            
        #for x in range(len(this.output_odds_array)):
            #print(this.output_odds_array[x])
        return this.output_odds_array
