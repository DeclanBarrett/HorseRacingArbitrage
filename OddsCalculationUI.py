# Odds Calculator Main UI
#
#
#from OddsCalculation import *
import tkinter as tk
import tkinter.ttk as ttk
from OddsCalculationBackEnd import *
from functools import partial

class OddsCalculationUI:

    def __init__(this):
        #Set up the windows
        this.the_window = tk.Tk()
        this.the_window.title("Horse Odds Calculator")
        this.the_window.geometry('1250x500')

        #common variables
        this.label_width = 10
        this.margin = 4
        this.best_odds_text_array = []
        this.race_buttons_array = []
        this.currentButtonNumber = -1

        # Define Widgets
        this.windowTitle = tk.Label(this.the_window,
                            text="HORSE ODDS CALCULATOR", )

        #Record Results Combo Box
        this.recordResultsTitle = tk.Label(this.the_window,
                                 width=35,
                                 text="Record Results?",
                                 anchor='e')
            
        this.recordResultsCombo = ttk.Combobox(this.the_window,
                                      width=20,
                                      state="readonly",
                                      values = ["No", "Yes and Overwrite", "Yes but don't Overwrite"])
        this.recordResultsCombo.current(0)
        #this.recordResultsCombo.bind("<<ComboboxSelected>>", this.recordResultsSent)

        #Include Tote Bets
        this.includeToteTitle = tk.Label(this.the_window,
                                 width=35,
                                 text="Include Tote Bet?",
                                 anchor='e')
        this.includeToteCombo = ttk.Combobox(this.the_window,
                                    width=20,
                                    state="readonly",
                                    values = ["No", "Yes", "Just Display Totes"])
        this.includeToteCombo.current(0)
        #this.includeToteCombo.bind("<<ComboboxSelected>>", this.includeToteSent)

        #Auto Refresh
        this.autoRefreshDefault = int(0)
        this.autoRefreshTitle = tk.Label(this.the_window,
                                 width=35,
                                 text="Automatically Refresh Every [Minutes]",
                                 anchor='e')
        this.autoRefreshInput = tk.Spinbox(this.the_window,
                                   from_=0,to=99999999,
                                   width=8,
                                   validate = 'all')
        #this.autoRefreshInput.insert(0,this.autoRefreshDefault)

        #How Much To Bet?
        this.betAmountDefault = int(500)
        this.betAmountTitle = tk.Label(this.the_window,
                                 width=35,
                                 text="Bet Amount? [AUD]",
                                 anchor='e')
        this.betAmountInput = tk.Spinbox(this.the_window,
                                 from_=0,to=99999999,
                                 width=8,
                                 validate = 'all')
        this.betAmountInput.delete(0, tk.END)
        this.betAmountInput.insert(0,this.betAmountDefault)

        #What Is The Minimum Bet?
        this.minimumBetDefault = int(0)
        this.minimumBetTitle = tk.Label(this.the_window,
                                 width=35,
                                 text="Minimum Bet? [AUD]",
                                 anchor='e')
        this.minimumBetInput = tk.Spinbox(this.the_window,
                                  from_=0,to=99999999,
                                  width=8)
        #this.minimumBetInput.insert(0,this.minimumBetDefault)

        #Only Show Races With Returns Over %
        this.showReturnsDefault = int(0)
        this.showReturnsTitle = tk.Label(this.the_window,
                                 width=35,
                                 text="Show Races Over % Return",
                                 anchor='e')
        this.showReturnsInput = tk.Spinbox(this.the_window,
                                   from_=0,to=99999999,
                                   width=8)
        #this.showReturnsInput.insert(0,this.showReturnsDefault)

        #Send Notifications RadioButton
        this.sendNotificationsStatus = tk.IntVar()
        this.sendNotificationsButton = tk.Checkbutton(this.the_window,
                                                      text = "Send Notifications",
                                                      variable = this.sendNotificationsStatus)

        


        #Refresh
        this.refreshButton = tk.Button(this.the_window, text = "Refresh", command = this.refreshAndGetOdds)

        #Table of Bets
        this.tableFrame = tk.Frame(this.the_window, width = 1, height = 1, relief = "groove", borderwidth = 2)
        this.bettingTable = tk.Text(this.tableFrame, width = 95, height = 27, wrap = 'word', state = 'disabled')

        #Placing Widgets in the grid
        this.windowTitle.grid(column = 0, row = 0, pady = this.margin,padx = this.margin, columnspan = 3)
        this.recordResultsTitle.grid(column = 0, row = 1, pady = this.margin,padx = this.margin, sticky='e')
        this.recordResultsCombo.grid(column = 1, row = 1, pady = this.margin,padx = this.margin, sticky='w')

        this.includeToteTitle.grid(column = 0, row = 2, pady = this.margin,padx = this.margin, sticky='e')
        this.includeToteCombo.grid(column = 1, row = 2, pady = this.margin,padx = this.margin, sticky='w')

        this.autoRefreshTitle.grid(column = 0, row = 3, pady = this.margin,padx = this.margin, sticky='e')
        this.autoRefreshInput.grid(column = 1, row = 3, pady = this.margin,padx = this.margin, sticky='w')

        this.betAmountTitle.grid(column = 0, row = 4, pady = this.margin,padx = this.margin, sticky='e')
        this.betAmountInput.grid(column = 1, row = 4, pady = this.margin,padx = this.margin, sticky='w')

        this.minimumBetTitle.grid(column = 0, row = 5, pady = this.margin,padx = this.margin, sticky='e')
        this.minimumBetInput.grid(column = 1, row = 5, pady = this.margin,padx = this.margin, sticky='w')

        this.showReturnsTitle.grid(column = 0, row = 6, pady = this.margin,padx = this.margin, sticky='e')
        this.showReturnsInput.grid(column = 1, row = 6, pady = this.margin,padx = this.margin, sticky='w')

        this.sendNotificationsButton.grid(column = 0, row = 7, pady = this.margin,padx = this.margin, sticky='e')

        this.refreshButton.grid(column = 1, row = 7, pady = this.margin,padx = this.margin, sticky='w')

        this.tableFrame.grid(column = 2, row = 1, rowspan = 14)
        this.bettingTable.grid(column = 0, row = 0)

        this.the_window.mainloop()
        
    def recordResultsSent(this, event):
        this.horse_odds_inst.record_results_set(this.recordResultsCombo.get())

    def includeToteSent(this, event):
        this.horse_odds_inst.include_tote_bets_set(this.includeToteCombo.get())

    def autoRefreshSent(this):
        this.horse_odds_inst.auto_refresh_set(this.autoRefreshInput.get())

    def betAmountSent(this):
        this.horse_odds_inst.bet_amount_set(this.betAmountInput.get())

    def minimumBetSent(this):
        this.horse_odds_inst.minimum_bet_set(this.minimumBetInput.get())

    def showReturnsSent(this):
        this.horse_odds_inst.show_returns_set(this.showReturnsInput.get())

    def sendNotificationsSent(this):
        this.horse_odds_inst.send_notifications_set(this.sendNotificationsStatus)

    def setAllVariablesSent(this):
        this.horse_odds_inst.record_results_set(this.recordResultsCombo.get())
        this.horse_odds_inst.include_tote_bets_set(this.includeToteCombo.get())
        this.horse_odds_inst.auto_refresh_set(this.autoRefreshInput.get())
        this.horse_odds_inst.bet_amount_set(this.betAmountInput.get())
        this.horse_odds_inst.minimum_bet_set(this.minimumBetInput.get())
        this.horse_odds_inst.show_returns_set(this.showReturnsInput.get())
        this.horse_odds_inst.send_notifications_set(this.sendNotificationsStatus.get())
        #this.horse_odds_inst.url_set(urlList)

    def urlList(this, inputSelected):
        url = "https://www.punters.com.au/odds-comparison/"

    def refreshAndGetOdds(this):
            #Instantiation of Horse Odds
            this.horse_odds_inst = BestHorseOdds()
            this.setAllVariablesSent()
            this.best_odds_text_array = this.horse_odds_inst.run_on_press()
            this.spawnButtonsToChangeRace(this.best_odds_text_array)
            if (this.currentButtonNumber != -1 & this.currentButtonNumber < len(this.bets_odds_text_array)):
                this.displayTable(this.currentButtonNumber)
            this.autoRefreshAfterRefresh(int(this.autoRefreshInput.get()))
            #print("Finished")

    def spawnButtonsToChangeRace(this, bestOddsArray):
        this.destroyAllButtons()
        for buttonNumber in range(len(bestOddsArray)):
            this.displayButtonForRaces = tk.Button(this.the_window, text = str(bestOddsArray[buttonNumber][:35]).strip(),width=50, command=partial(this.displayTable, buttonNumber) )
            this.displayButtonForRaces.grid(column = 0, row = 8 + buttonNumber, pady = this.margin,padx = this.margin, columnspan = 2)
            this.race_buttons_array.append(this.displayButtonForRaces)

    def displayTable(this, raceNumber):
        this.currentButtonNumber = raceNumber
        this.bettingTable.config(state=tk.NORMAL)
        this.bettingTable.delete(1.0, tk.END)
        this.bettingTable.insert(tk.END, this.best_odds_text_array[raceNumber])
        this.bettingTable.config(state=tk.DISABLED)

    def destroyAllButtons(this):
        for buttonNumber in range(len(this.race_buttons_array)):
            this.race_buttons_array[buttonNumber].grid_forget()
            this.race_buttons_array[buttonNumber].destroy()
        this.race_buttons_array = []

    def autoRefreshAfterRefresh(this, waitTime):
        if (waitTime > 0):
            this.the_window.after(waitTime * 1000 * 60, this.refreshAndGetOdds)
        
OddsCalculationUI()

