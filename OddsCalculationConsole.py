#OddsCalculation Console


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
