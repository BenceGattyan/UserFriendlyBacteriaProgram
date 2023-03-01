
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 13:57:30 2020

@author: Bence Gattyan, Norbert Balint, Sara Krenk
"""

#------------------------------------------------------------------------------
import numpy as np
from myFunctions import *

# Define used variables menu items and conditions------------------------------
#
# Mark whether data is loaded
dataProperty = 0
# Main menus items
menuItems = np.array(["Load data","Filter data","Generate statistics","Generate plots","Help","Quit"])
# Filter submenus items
filterItems = np.array(["Temperature","Growth rate","Bacteria","Reset filters","Back to main menu"])
# Data submenus items
statisticItems=np.array(["Mean Temperature","Mean Growth rate","Std Temperature","Std Growth rate","Rows","Mean cold Growth rate","Mean Hot Growth rate","Return to main menu"])
dataItems = np.array(["Clear memory","Back to main menu"])
# Slice of the main menu I wish to presend when there is no data loaded
menuSlice = [0,4,5]
# initial empty variable where the data will be loaded
data=0
# Mark whether filters are applied
filterCondition=False
# Empty variable for the filtered data.
# Needed so that we dont overwrite the original data whenever we filter it
filteredData=0   
# Bacteria/filter names used for filter feedback
bacteriaItems = np.array(["No filters","Salmonella enterica","Bacillus cereus","Listeria","Brochothrix thermosphacta"])
tempStatus="No filters"
growthStatus="No filters"
bacteriaStatus = bacteriaItems[0]
filterStatus="No filters+No filters+No Filters"
filterStatus=filterStatus.split("+")
tempFilter=np.array([0,0])
#------------------------------------------------------------------------------

# Start------------------------------------------------------------------------
while True:
    #
    # Main menu----------------------------------------------------------------
    #
    # Here I present the user with the main menu.
    # They can choose an option by inputting the respective number and
    # will get prompted to do so until they choose a valid option.
    # The menu system was made by Bence unless marked otherwise.
    # The functions called within were a mix of the groups makings and 
    # are marked respectively in myFunctions.py
    #
    # Set the main menu's options in accordance to dataProperty
    if dataProperty == 0:
        relevantMenuItems = list(menuItems[menuSlice])
    elif dataProperty == 1:
        relevantMenuItems = menuItems
    
    # Display relevant menu options and ask user to choose a menu item    
    choice = displayMenu(relevantMenuItems,"Please select one of the above: ",filterCondition,filterStatus)
    print("")
    # Menu item chosen!
    
    # Translate choice in case there is no data loaded
    if dataProperty == 0:
        if choice== 2:
            choice = 5
        elif choice == 3:
            choice = 6
    #
    # Submenus-----------------------------------------------------------------
    # Navigate and input the options of the functions.
    # Where its possible I added "Back to main menu" option in case user changes 
    # their mind, inputs wrong number ect...
    # 
    # 1. Load data-------------------------------------------------------------
    if choice == 1:
        
        # There is no data loaded currently------------------------------------
        if dataProperty == 0:
            
            filename=input("Please insert the filename containing the data: ")
            print("")
            try:
                data=dataLoad(filename)
                filteredData=data
                dataProperty = 1
                print("Data loaded")
            # Give error message in case there is one
            except FileNotFoundError:
                print("")
                print("File {} does not exist".format(filename))
            except ValueError:
                print("")
                print("Selected file format not supported,")
                print("using an N*3 array of numbers in a txt file recommended")
            except OSError:
                print("")
                print("File {} does not exist".format(filename))
 
        # There is data loaded in memory---------------------------------------
        elif dataProperty == 1:
            dataChoice = displayMenu(dataItems, "Please select one of the above: ",filterCondition,filterStatus)
            print("")
            while True:
                # Clear memory-------------------------------------------------
                if dataChoice == 1: 
                    dataProperty = 0
                    print("Memory cleared")
                    print("")
                    break
                # Back to main menu--------------------------------------------
                elif dataChoice == 2:
                    print("")
                    break

    # 2. Filter data-----------------------------------------------------------
    #If the user chooses this menu, they will be able to choose what condition they 
    #would like to filter for.(Norbert)
    elif choice == 2:
        if filterCondition:
            print("Warning: Applying filters will stack on current filters")
        filterChoice = displayMenu(filterItems,"Filter by: ",filterCondition,filterStatus) 
        print("")
        while True:

            # 1. Temperature---------------------------------------------------
            #If Temperature is chosen, return a matrix in which the Temperature
            #is whithin the chosen filter range.(Norbert)
            if filterChoice == 1:
                tempFilter=dataFilter("Temperature",1,filteredData,filterStatus)
                filteredData=tempFilter[0]
                filterStatus=tempFilter[1]
                filterCondition=True
                break
            # 2. Growth rate---------------------------------------------------
            #If Growth rate is chosen, return a matrix in which the Growth rate
            #is whithin the chosen filter range.(Norbert)
            elif filterChoice == 2:
                tempFilter=dataFilter("Growth rate",2,filteredData,filterStatus)               
                filteredData=tempFilter[0]
                filterStatus=tempFilter[1]
                filterCondition=True
                break
            # 3. Bacteria------------------------------------------------------
            #If Bacteria is chosen return a matrix containing only the chosen bacteria.(Norbert)
            elif filterChoice == 3:
                tempFilter=dataFilter("Bacteria",3,filteredData,filterStatus)
                filteredData=tempFilter[0]
                filterStatus=tempFilter[1]
                filterCondition=True
                break            
            # 4. Reset (Removes current filters)-------------------------------
            elif filterChoice == 4:
                filterStatus="No filters+No filters+No Filters"
                filterStatus=filterStatus.split("+")
                filteredData=data
                filterCondition=False

                print("Filters removed")
                print("")
                break            
            # Back to main menu------------------------------------------------
            elif filterChoice == 5:
                break
            
    # 3. Generate statistics---------------------------------------------------
    #The user can chose what sort of statistical data they wish to see. 
    #The chosen statistic and the value will be displayed:(Norbert)
    elif choice == 3:
        statisticsChoice=displayMenu(statisticItems, "Choose statistics to display:",filterCondition,filterStatus)
        while True:
            if statisticsChoice==1:
                stats=dataStatistics("Mean Temperature",filteredData)
                if np.size(filteredData)==0:
                    print("No data is loaded or all data has been filtered out")
                else:
                    print("The Temperature average for all selected bacteria types.")
                    print("Mean Temperature:" + str(stats))
                break
            elif statisticsChoice==2:
                stats=dataStatistics("Mean Growth rate",filteredData)
                if np.size(filteredData)==0:
                    print("No data is loaded or all data has been filtered out")
                else:
                    print("The average Growth rate for all selected bacteria types.")
                    print("Mean Growth rate:"+str(stats))
                break
            elif statisticsChoice==3:
                stats=dataStatistics("Std Temperature",filteredData)
                if np.size(filteredData)==0:
                    print("No data is loaded or all data has been filtered out")
                else:
                    print("The standard deviation of Temperature for all selected bacteria types.")
                    print("Std Temperature:"+str(stats))
                break
            elif statisticsChoice==4:
                stats=dataStatistics("Std Growth rate",filteredData)
                if np.size(filteredData)==0:
                    print("No data is loaded or all data has been filtered out")
                else:
                    print("The standard deviation of Growth rate for all selected bacteria types.")
                    print("Std Growth rate:"+str(stats))
                break
            elif statisticsChoice==5:
                stats=dataStatistics("Rows",filteredData)
                if np.size(filteredData)==0:
                    print("No data is loaded or all data has been filtered out")
                else:
                    print("The total number of rows in the data.")
                    print("Number of rows:"+str(stats))
                break
            elif statisticsChoice==6:
                stats=dataStatistics("Mean Cold Growth rate",filteredData)
                if str(stats)=="nan":
                    print("No data is loaded or all data has been filtered out")
                else:
                    print("Average Growth rate when Temperature is less than 20 degrees.")
                    print("Mean Cold Growth rate:"+str(stats))
                break
            elif statisticsChoice==7:
                stats=dataStatistics("Mean Hot Growth rate",filteredData)
                if str(stats)=="nan":
                    print("No data is loaded or all data has been filtered out")
                else:
                    print("Average Growth rate when Temperature is greater than 50 degrees.")
                    print("Mean Hot Growth rate:"+str(stats))
                break
            elif statisticsChoice==8:    
                break
        
    
    # 4. Generate plots--------------------------------------------------------
    elif choice == 4:
        dataPlot(data,filteredData)
            
    # 5. Help------------------------------------------------------------------
    #
    # Print instructions for the user in case they need it
    # Since the initial main menu has so few options I provided the help
    # in this way to not clutter the program with unnesecary instructions
    #
    elif choice == 5:
        print("------------------------------------<")
        print("")
        print("This program takes care of filtering data, creating statistics and plots.")
        print("")
        print("You can navigate the program with menus each having their own purpose.")
        print("")
        print("First you have to load the data you want to work with under the option: Load data.")
        print("Once you do this the other options will become accessible.")
        print("")
        print("Then you have the option to filter the data by some conditions so the statistics/plots will only use the desired conditions.")
        print("")
        print("Once you selected the desired conditions, you can request statistics and plots under the respective menu.")
        print("")
        print("To close the program select the Quit option")
        print("")
        print("------------------------------------<")
        print("")
            
    # -------------------------------------------------------------------------
    # 6. Quit
    elif choice == 6:
        # End
        break