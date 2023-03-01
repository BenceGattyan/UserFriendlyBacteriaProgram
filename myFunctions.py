# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 13:57:30 2020

@author: Bence Gattyan, Norbert Balint, Sara Krenk
"""

import numpy as np
import matplotlib.pyplot as plt

def inputNumber(prompt):
    #(originally from python excersize modules)
    # INPUTNUMBER Prompts user to input a number
    #
    # Usage: num = inputNumber(prompt) Displays prompt and asks user to input a
    # number. Repeats until user inputs a valid number.
    #
    # Author: Mikkel N. Schmidt, mnsc@dtu.dk, 2015
    while True:
        try:
            num = float(input(prompt))
            break
        except ValueError:
            pass
    return num

def displayMenu(options,question,filterCondition,filterStatus):
    # (originally from python excersize modules)
    # DISPLAYMENU Displays a menu of options, ask the user to choose an item
    # in a requested way and returns the number of the menu item chosen.
    #
    # Usage: choice = displayMenu(options,question)
    #
    # Input options Menu options (array of strings) 
    #               Question (string)
    # Output choice Chosen option (integer)
    #
    # Author: Mikkel N. Schmidt, mnsc@dtu.dk, 2015
    # Slightly modified by Bence
    #
    # I added the option to define the prompt question so it can fit
    # the presented options better.
    # It will also print the current list of filters active
    # before printing the menu out.
    #
    filterDisplay(filterCondition,filterStatus)
    # Display menu options
    for i in range(len(options)):
        print("{:d}. {:s}".format(i+1, options[i]))
    # Get a valid menu choice
    menuChoice = 0   
    while not(np.any(menuChoice == np.arange(len(options))+1)):
        menuChoice = inputNumber(question)
    return menuChoice

def dataLoad(filename): 
    # dataLoad loads the data from the requested file and will filter out data deemed to be out of range
    # made by Sara
    filteredRows = [] # an empty list is made where we can put our filtered rows
    wrongTemp = []    # we make more lists for the values in our matrix that are invalid
    wrongGrowth = []
    wrongBact = [] 
    rawdata = np.loadtxt(filename) #we extract the information from the file
    x = 1             # this line of code assigns the first row the row number 1 
    errorRow1 = []    # more empty lists, this time for the row numbers of the rows containing invalid data
    errorRow2 = []
    errorRow3 = [] 
    for row in rawdata:            #we use a loop to check the rows for certain conditions
        column1 = row[0] > 10 and row[0] < 60 #column1 has the conditions for the first column
        column2 = row[1] > 0                  #column2 has for the second column and 
        column3 = row[2] in [1, 2, 3, 4]      #column3 has for the third column
        if all([column1, column2, column3]): #if a row fulfils all conditions it
            filteredRows.append(row)        #is added to the empty list for filtered rows
        else:
            if column1 == False:            #if the conditions are not met then the invalid information is put into
                wrongTemp.append(row[0])    #one of the previously established lists depending on what information
                errorRow1.append(int(x))    #is invalid along with the respective row's row number
            if column2 == False:
                wrongGrowth.append(row[1])
                errorRow2.append(int(x))
            if column3 == False:
                wrongBact.append(row[2])
                errorRow3.append(int(x))    #once the first row has been checked the row number for the next row becomes the
        x = x + 1                           #previous one's plus one, and so forth until all rows have been checked
    # these lines print out error messages and inform the user what errors are in their matrix,
    # and which row their errors are on using the lists we put the invalid information in earlier
    # Bence made the error messages disappear in case there is no error to message, the messages were wrote by Sara.
    if not(len(wrongTemp) == 0):
        print("The temperature(s) {} in row(s) {} (respectively) are out of range.".format(wrongTemp, errorRow1))
        print("")
    if not(len(wrongGrowth) == 0):
        print("The bacterial growth {} in row(s) {} (respectively) are out of range.".format(wrongGrowth, errorRow2))
        print("")
    if not(len(wrongBact) == 0):
        print("The bacteria type(s) {} in row(s) {} (respectively) are out of range.".format(wrongBact, errorRow3 ))
        print("")
    #all the filtered rows are stacked to make a single matrix with the data we want, that is then returned
    data = np.stack(filteredRows)  
    return data 

def dataFilter(field,columnNumber,filteredData,filterStatus):
    bacteriaItems = np.array(["No filters","Salmonella enterica","Bacillus cereus","Listeria","Brochothrix thermosphacta"])

    # A function to filter the loaded data. The function returns an Nx3 matrix filtered with the chosen parameters. (Norbert)
    if field != "Bacteria":
        M=0   #M is an empty string where data will be loaded(Norbert)
        #Prompts the user to insert a range in which Temperature or Growth rate will be examined.(Norbert)
        while True:
            try:
                lowerLimit=float(input("Please enter a lower limit for " + field + ":"))
                upperLimit=float(input("Please enter an upper limit for "+ field + ":"))
                if field=="Temperature" and (lowerLimit<10 or upperLimit>60):
                     raise ValueError
                elif field=="Growth rate" and (lowerLimit<=0 or upperLimit<=0):
                     raise ValueError
                #M will a part of a chosen column, that is whithin the chosen range.(Norbert) 
                M=filteredData[filteredData[:,(columnNumber-1)]>lowerLimit,:]                
                break
            
            #Warns the user of an error during input, and prompts them to insert a valid input.(Norbert)  
            except ValueError:
                if field=="Growth rate":
                    print("Invalid input, please insert a positive number")
                elif field=="Temperature":
                    print("Invalid input, please choose a range between 10°C and 60°C")
        if field=="Temperature":
            filterStatus[0]=("From {} to {}°C".format(lowerLimit,upperLimit))
        elif field=="Growth rate":
            filterStatus[1]=("From {} to {}".format(lowerLimit,upperLimit))
        #Returns the filtered matrix.(Norbert) , and filter feedback (Bence)
        return np.array([M[M[:,(columnNumber-1)]<upperLimit,:],filterStatus])
    #Prompts the user to select a bacteria type to filter for.(Norbert)
    else:  
        while True:
            try:
                bacteriaNumber=float(input(
                                   "1:Salmonella enterica\n"
                                   "2:Bacillus cereus\n"
                                   "3:Listeria\n"
                                   "4:Brochothrix thermosphacta\n"
                                   "Please select bacteria type:"))
                #Warns the user if wrong input was given and prompts them to give a valid input.(Norbert)
                if bacteriaNumber not in [1,2,3,4]:
                    raise ValueError
                break
            except ValueError:
                print("Invalid choice,please select a valid number.")
        #Returns the filtered matrix.(Norbert)   
        if field=="Bacteria":
            filterStatus[2]=(bacteriaItems[int(bacteriaNumber)])
        #Returns the filtered matrix.(Norbert) , and filter feedback (Bence)
        return np.array([filteredData[filteredData[:,(columnNumber-1)]==bacteriaNumber,:],filterStatus])

def filterDisplay(filterCondition,filterStatus):
    # 
    # This function will print out the current filters
    # filterCondition should be a boolean marking whether there are filters active
    #
    # I am calling this function from displayMenu in order to appear whenever the user
    # is presented with an interface, and filterCondition is supposed to be changed a line after 
    # a filter was applied/removed
    #
    # Made by: Bence   
    if filterCondition:
         print("Current filters active are:")
         print("Temperature: {}".format(filterStatus[0]))
         print("Growth rate: {}".format(filterStatus[1]))
         print("Bacteria family: {}".format(filterStatus[2]))
         print("")
    else:
        print("There are no filters active")
        print("")

def dataStatistics(statistics,filteredData):
    #A function to show statistics for the data.
    #It receives the filtered or non-filtered data as an input 
    #and gives a number as an output.(Norbert)
    #Filtered data is loaded in. Keep in mind that if there are no filters
    #active, filteredData covers the imported, unfiltered data.(Norbert)
    stats=""
    
    #The matrix is transposed, and the 3 rows of the new matrix(Temperature,
    #Growth rate and Bacteria type), are seperated into single arrays.(Norbert)
    T=filteredData.T
    Temp=T[0,:]
    Growth=T[1,:]
    Bact=T[2,:]
    if statistics=="Mean Temperature":
        stats=np.mean(Temp)                 #Calculates the average of the elements in the Temperature array.(Norbert)
    elif statistics=="Mean Growth rate":
        stats=np.mean(Growth)               #Calculates the average of the elements in the Growth rate array.(Norbert)
    elif statistics=="Std Temperature":
        stats=np.std(Temp)                  #Calculates the standard deviation of the elements in the Temperature array.(Norbert)
    elif statistics=="Std Growth rate":
        stats=np.std(Growth)                #Calculates the standard deviation of the elements in the Growth rate array.(Norbert)
    elif statistics=="Rows":
        stats=np.size(Bact)                 #Calculates the number of elements in the Bacteria array.(Norbert)
    elif statistics=="Mean Cold Growth rate":
        stats=np.mean(Temp[Temp<20])        #Calculates the average of the elements in the Temperature array, 
                                            #for elements lower than 20 degrees.(Norbert)
    elif statistics=="Mean Hot Growth rate":
        stats=np.mean(Temp[Temp>50])        #Calculates the average of the elements in the Temperature array, 
                                            #for elements higher than 50 degrees.(Norbert)
    return stats
        
def dataPlot(data,filteredData):
    # dataPlot loads the data filtered by dataLoad and filteredData, and uses them to make a bar plot and scatter plot
    # made by Sara
    dataSet = filteredData

    Box1 = []       # empty lists(boxes) are made where we can sort our different bacteria types into
    Box2 = []
    Box3 = []
    Box4 = []
    Boxes = [Box1, Box2, Box3, Box4] # we make a list containing our (currently) empty boxes so we can check them later

    for row in dataSet: # a loop checks our each row of our data and sorts those rows into their respective box depending
        if row[2] == 1:     # on the value in their third column that characterises which bacteria type the data is for
            Box1.append(row)
        if row[2] == 2:
            Box2.append(row)
        if row[2] == 3:
            Box3.append(row)
        if row[2] == 4:
            Box4.append(row)
               
    for b in Boxes:     # this loop stacks the rows we've gathered in our respective boxes
        if Box1 == []:  # if the box is an empty list, it stays as an empty list
            Type1 = []
        else:
            Type1 = np.stack(Box1)
        if Box2 == []:
            Type2 = []
        else:
            Type2 = np.stack(Box2)
        if Box3 == []:
            Type3 = []
        else:
            Type3 = np.stack(Box3)
        if Box4 == []:
            Type4 = []
        else:
            Type4 = np.stack(Box4)
                  
    Types = [Type1, Type2, Type3, Type4]    # this list now contains either matrices with stacked rows or empty lists

    for t in Types:     # this loop checks our list(Types) for empty lists and gives them the value 0, 
        if Type1 == []:     # otherwise it finds the number of rows of data in the matrices
            Block1 = 0      # in our list so that we can plot them as values in a bar plot
        else:
            Block1 = len(Type1)
        if Type2 == []:
            Block2 = 0
        else:
            Block2 = len(Type2)
        if Type3 == []:
            Block3 = 0
        else:
            Block3 = len(Type3)
        if Type4 == []:
            Block4 = 0
        else:
            Block4 = len(Type4)

    BacType = ['Salmonella','Bacillus','Listeria','Brochothrix']   
    BacNumber = [Block1, Block2, Block3, Block4] 
     # we define our plottable data as the data we get from the previous loop
     # we define the names of the bacteria that corresponds to our data in BacType
     # we define BacNumber as our plottable data that we got from the previous loop
     # then we plot BacType and BacNumber in a bar plot, selecting the colors we want to use,
     # adding a black edge to the bars in the bar plot and grid lines
    plt.bar(BacType, BacNumber, color = ['magenta','cyan','green','blue'], edgecolor = ['black']) 
    plt.grid(True)
    for i in range(len(BacType)):       # this piece of code adds the value of the bar in the bar plot on top of the bar
        plt.annotate(BacNumber[i], (-0.1 + i, BacNumber[i] + 0.2))  # i found out how to do that from this website: 
                                    # https://towardsdatascience.com/mastering-the-bar-plot-in-python-4c987b459053
    plt.title('Number of Different Bacteria')       # the name of our graph
    plt.xlabel('Bacteria Type')                     # the name of our x values
    plt.ylabel('Number of Data Sets')               # the name of our y values
    plt.show()
    
    
    for x in Types:  # this loop checks our list(Types) for empty lists and gives them them x and y values equal to 0 
        if Type1 == []: # so that we can plot them later. If the list is not empty and contains a row/rows then the first 
            x1 = 0      # column of the row(s) becomes x values, while the second column becomes y values
            y1 = 0
        else:
            x1 = (Type1[:,0])
            y1 = (Type1[:,1])
        if Type2 == []:
            x2 = 0
            y2 = 0
        else:
            x2 = (Type2[:,0])
            y2 = (Type2[:,1])
        if Type3 == []:
            x3 = 0
            y3 = 0
        else:
            x3 = (Type3[:,0])
            y3 = (Type3[:,1])
        if Type4 == []:
            x4 = 0
            y4 = 0
        else:
            x4 = (Type4[:,0])
            y4 = (Type4[:,1])
    
    # We plot the x and y values we got from the previous loop into a scatter plot, giving the x and y values of the different 
    # list each their own color and label for clarity. We also add grid lines, a title for the plot, x and y labels, a legend, 
    # and finally we limit our x axis to be between 10 and 60, and our y axis to be between 0 and 1
    
    plt.plot(x1,y1, "m*", label = 'Salmonella')
    plt.plot(x2,y2, "c*", label = 'Bacillus')
    plt.plot(x3,y3, "g*", label = 'Listeria')
    plt.plot(x4,y4, "b*", label = 'Brochothrix')
    plt.grid(True)
    plt.title("Growth Rate by Temperature")
    plt.xlabel("Temperature(°C)") 
    plt.ylim([0, 1])
    plt.ylabel("Growth Rate")
    plt.legend()
    plt.xlim([10, 60])
    plt.show()
    plots = plt.show()          # we call both our bar plot and scatter plot 'plots' and return them
    return plots