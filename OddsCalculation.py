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
import numpy as np
import os
import sys, time, msvcrt

#Opens the webpage
def open_web_page(page_to_open):
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

def print_table(table):
    longest_cols = [
        (max([len(str(row[i])) for row in table]) + 1)
        for i in range(len(table[0]))
    ]
    row_format = "".join(["{:>" + str(longest_col) + "}" for longest_col in longest_cols])
    for row in table:
        print(row_format.format(*row))
        
#Optimisation algorythms
best_odds_array = []

content_file = ""

#Define function to calculate profit
def calcProfit(x):
    bets_placed = []
    revenue_made = []
    current_bet_revenue = 0
    for current_index in range(len(best_odds_array)):
        current_bet_revenue = x[current_index] * best_odds_array[current_index]
        bets_placed.append(x[current_index])
        revenue_made.append(current_bet_revenue)
    revenue = min(revenue_made)
    profit = revenue - sum(bets_placed)
    return profit

#Define function to calculate cost
def calcRevenue(x):
    bets_placed = []
    revenue_made = []
    current_bet_revenue = 0
    for current_index in range(len(best_odds_array)):
        current_bet_revenue = x[current_index] * best_odds_array[current_index]
        bets_placed.append(x[current_index])
        revenue_made.append(current_bet_revenue)
    return min(revenue_made)

#Calculates Cost   
def calcCost(x):
    return sum(x)

#Define objective function for optimisation
def objective(x):
    return -calcProfit(x)

#Define constraint for optimisation
def constraint(x):
    return maximum_bet - calcCost(x)


def betting_optimisation(best_odds_array, best_odds_and_names, racers_name_optim):
    bets_placed = []

    best_optimisation = []
    best_optimisation_profit = -999999
    #load constraints into dictionary form
    cons = ({'type': 'ineq', 'fun': constraint})

    #upper_bound = 100
    #bnds
    bnds = ()
    for current_bounds in range(len(best_odds_array)):
        bnds += (minimum_bet, maximum_bet),

    current_append = minimum_bet + 1
    #looping till outside bounds
    while (current_append < maximum_bet):
        #set initial guess values
        bet_best_guess = []
        for current_index in range(len(best_odds_array)):
            bet_best_guess.append(current_append)
        #load guess values
        x0 = np.array(bet_best_guess)
        #Call solver to minimize the objective function given the constraints
        sol = minimize(objective,x0,method='SLSQP',bounds=bnds,constraints=cons,options={'disp':False})
        #Retrieve optimized profit and bets
        xOpt = sol.x

        #Round it
        actual_bets = []
        for x_number in range(len(xOpt)):
            actual_bets.append(round(xOpt[x_number], 2))

        profitOpt = -sol.fun
        #Calculate surface
        costOpt = calcCost(actual_bets)
        revenueOpt = calcRevenue(actual_bets)
        if (best_optimisation_profit < (revenueOpt - costOpt)):
            best_optimisation = actual_bets
        current_append += (maximum_bet/20)
        

    #Display Optimisation
    print("Bets")
    export_horse_company_bet_table = []
    export_horse_company_bet_table.append(["     Horse Name:","     Betting Company:", "     Best Odds:","     Amount on Horse:", "     Return:"])
    for current_bet_index in range(len(best_optimisation)):
        export_horse_company_bet_table.append([str(racers_name_optim[current_bet_index]),\
                                               str(best_odds_and_names[current_bet_index][0]),\
                                               str(best_odds_and_names[current_bet_index][1]),\
                                               str(best_optimisation[current_bet_index]),
                                               str(round(float(best_optimisation[current_bet_index])\
                                                         * float(best_odds_and_names[current_bet_index][1]), 2))])
    print_table(export_horse_company_bet_table)
    print()
    print("Profit: " + str(round(revenueOpt - costOpt, 2)))
    print("Revenue: " + str(round(revenueOpt, 2)))
    print("Cost: " + str(round(costOpt, 2)))
    if (costOpt == 0):
        print("Return: " + str(round(100 * (revenueOpt - costOpt)/1,2)) + "%")
    else:
        print("Return: " + str(round(100 * (revenueOpt - costOpt)/costOpt,2)) + "%")
    if ((record_results == "y") & (round(revenueOpt - costOpt, 2) > 0)):
        right_now = datetime.now()
        save_table(table_of_race_odds, race_names[race])
        save_table(export_horse_company_bet_table, "Bets")
        content_str = "<h2>" + str(right_now) + "</h2>" + "<br>Profit: " + str(round(revenueOpt - costOpt, 2)) + "<br>Revenue: " + str(round(revenueOpt, 2)) + "\
<br>Cost: " + str(round(costOpt, 2)) + "<br>Return: " + str(round(100 * (revenueOpt - costOpt)/costOpt,2)) + "%"
        text_file = open('ConfirmedWins.html', 'r', encoding = 'UTF-8')
        content_file = text_file.readline()
        text_file.close()
        content_file = content_file[:len(content_file) - 18] + content_str + content_file[len(content_file) - 18:]
        text_file = open('ConfirmedWins.html', 'w', encoding = 'UTF-8')
        text_file.write(content_file)
        text_file.close()
#Best odds
def bestOdds(current_race_odds):
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

def save_table(table, table_name):
    if (record_results == "y"):
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
    

while True:
    try:
        record_results = input('Do you want to record results? (y or n): ')
        if ((record_results == "y") | (record_results == "n")):
            break
        else:
            print("Sorry, input was not valid")
            continue
    except:
        print("Sorry, input was not valid")
        continue
    else:
        break
if (record_results == "y"):
    while True:
        try:
            create_new = input('Do you want to overwrite the previous confirmed wins? (y or n): ')
            if ((create_new == "y") | (create_new == "n")):
                break
            else:
                print("Sorry, input was not valid")
                continue
        except:
            print("Sorry, input was not valid")
            continue
        else:
            break
    if (create_new == "y"):
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

while True:
    try:
        infinite_mode_boolean = input('Do you want infinite mode turned on? (y or n): ')
        if ((infinite_mode_boolean == "y") | (infinite_mode_boolean == "n")):
            break
        else:
            print("Sorry, input was not valid")
            continue
    except:
        print("Sorry, input was not valid")
        continue
    else:
        break

if (infinite_mode_boolean == "y"):
    while True:
        try:
            no_tote = input('Do you want to include tote bets? (y or n or j for just tote): ')
            if ((no_tote == "y") | (no_tote == "n") | (no_tote == "j")):
                break
            else:
                print("Sorry, input was not valid")
                continue
        except:
            print("Sorry, input was not valid")
            continue
        else:
            break
    while True:
        try:
            maximum_bet = float(input('How much do you want to bet? '))
            minimum_bet = float(input('What is the minimum allowed bet? '))
        except:
            print("Sorry, input was not valid")
            continue
        else:
            break
while True:
    if (infinite_mode_boolean == "n"):
        while True:
            try:
                no_tote = input('Do you want to include tote bets? (y or n or j for just tote): ')
                if ((no_tote == "y") | (no_tote == "n") | (no_tote == "j")):
                    break
                else:
                    print("Sorry, input was not valid")
                    continue
            except:
                print("Sorry, input was not valid")
                continue
            else:
                break
        print(no_tote + " - was selected")
        while True:
            try:
                maximum_bet = float(input('How much do you want to bet? '))
                minimum_bet = float(input('What is the minimum allowed bet? '))
            except:
                print("Sorry, input was not valid")
                continue
            else:
                break
    url = 'https://www.punters.com.au/odds-comparison/horse-racing/all/'; #all
    
    # Read the contents of the web page as a character string,
    # suitable for printing to an ASCII-only Tk widget, using
    # backslashes to "escape" any non-ASCII characters

    web_page_text = open_web_page(url)
    #web_page_text = open('WithErrorAtBalaklava.html', encoding = 'utf8').read()

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
    new_text = findall(race_string_find, web_page_text)
    #print(new_text)

    #Keeps track of all the line beginnings
    line_numbers = findall(new_line_regex, web_page_text)

    #Racers name
    racers_name_regex = '&nbsp;</span>[ \\n\\r]+([\'A-Za-z0-9\- ]+)[ \\n\\r]+<'
    racers_name_array = []

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
    #print(race_names)
    #print("\n")
    #print(racers_name_array)
    #print("\n")

    #List of maximums
    list_of_maximums = []

    print()
    #Creates a nice list to put into table displayer
    for race in range(len(organised_lines_array)):
        print("-------------------------------------------------------------------------")
        #deletes lay bet and totes
        for line in range(len(organised_lines_array[race])):
            del organised_lines_array[race][line][18:]
            if (no_tote == "n"):
                del organised_lines_array[race][line][:3]
            if (no_tote == "j"):
                del organised_lines_array[race][line][3:]
        table_of_race_odds = []
        race_list_of_maximums = []
        #prints race name
        print("Race: " + str(race + 1) + " - " + str(race_names[race]) + "\n")
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
            temporary_line_array.insert(0, str(line + 1) + str(racers_name_array[race][line][:8]))
            
        #prints out more important information
        print_table(table_of_race_odds)
        
        list_of_maximums.append(race_list_of_maximums)
        print("\n")
        best_odds_current_race = bestOdds(organised_lines_array[race])
        best_odds_array = best_odds_current_race[0]
        best_odds_array_names = best_odds_current_race[1]
        
        betting_optimisation(best_odds_array, best_odds_array_names, racers_name_array[race])
        print("\n")
    #": " + str(racers_name_array[race][line]) + " - " +

    #####print(number_of_lines)
    #####print(number_locations)
    bet_numbers = findall('sign ([A-Za-z0-9 ]+)">bet</span>([0-9]+)', web_page_text)
    #">bet</span> </a></div>

    if (infinite_mode_boolean == "n"):
        while True:
            try:
                repeat_again = input('Would you like to run program again? (y or n): ')
                if ((repeat_again == "y") | (repeat_again == "n")):
                    break
                else:
                    print("Sorry, input was not valid")
                    continue
            except:
                print("Sorry, input was not valid")
                continue
            else:
                break
        if (repeat_again == "n"):
            break
        while True:
            try:
                clear_previous_attempts = input('Would you like to clear previous inputs? (y or n) - unavailable in IDLE: ')
                if ((clear_previous_attempts == "y") | (clear_previous_attempts == "n")):
                   break
                else:
                    print("Sorry, input was not valid")
                    continue
            except:
                print("Sorry, input was not valid")
                continue
            else:
                break
        if (clear_previous_attempts == 'y'):
            os.system('CLS')
    else:
        print("-------------------------------------------------------------------------")
        time.sleep(360)
