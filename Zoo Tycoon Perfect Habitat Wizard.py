#******************************************************************************
# Program: Zoo Tycoon Perfect Habitat Wizard
# Programmer: Taylor Reed
# Created with data from the Zoo Tycoon Guide by Steven W. Carter
# https://gamefaqs.gamespot.com/pc/472139-zoo-tycoon-2001/faqs/19545
#******************************************************************************

import ZTclass
import csv

#***************************************
# Create habitat instances
#***************************************

allAnimals = []
animal = {}

with open('ZTdata.csv') as csvFile:
    csv_reader = csv.reader(csvFile)

    for line in csv_reader: 
        allAnimals.append(line[0])
        animal[line[0]] = ZTclass.Habitat(*line[0:6])
        x = 6
        while x != len(line) and line[x]:
            animal[line[0]].addTerrain(line[x], float(line[x+1]))
            x += 2

#******************************************************************************
#                       MAIN MENU
#******************************************************************************

#***************************************
# dispMenu()
# Main display menu
#***************************************

def dispMenu():
    print()
    print("\tMain Menu")
    print("------------------------")
    print("1. Display all animals")
    print("2. Calculate cage size")
    print("3. Calculate cage capacity")
    print("4. Calculate terrain requirements")
    print("5. About this program")
    print("0. Exit")
    while True:
        try:
            menuSelect = int(input("Select a menu option by number: "))
            if menuSelect < 0 or menuSelect > 5:
                raise ValueError()
        except ValueError:
            print("Error: Enter a number from the list")
        except Exception as detail:
            print("Error:", detail)
        else:
            return menuSelect

#******************************************************************************
#                           OPTION 1
# printAll()
# Prints full list of animals
#******************************************************************************

def printAll():
    print()
    for element in allAnimals: 
        print(f"{element.title()}")
    print()
    exit = input("Hit any key to return to main menu.")
    return


#******************************************************************************
#                          OPTION 2
# getMinCageSize()
# Calculates the minimum cage size needed for the given number of animals
#
# Uses helper functions: selectAnimal(), isYN()
#******************************************************************************

def getMinCageSize():
    userAnimal = selectAnimal()
    while True: 
        try:
            numAnimals = int(input(f"How many {userAnimal.title()}s? "))
            if numAnimals <= 0 or numAnimals > 25:
                raise ValueError()
        except ValueError:
            print("Error: Quantity must be an integer between 1 and 25")
        except Exception as detail:
            print("Error:", detail)
        else:
            break
    minCageSize = animal[userAnimal].getCageSize(numAnimals)
    print(f"For {numAnimals} {userAnimal.title()}s, you need a cage that is at least {minCageSize} tiles.")
    
    verify = input("Would you like to calculate another cage size? (y/n) ")
    if isYN(verify):
        getCageCapacity()
    else: 
        return

#******************************************************************************
#                          OPTION 3
# getCageCapacity()
# Calculates how many of the selected animals can live in the given cage size. If the 
# cage is too small, the minimum size for one animal is calculated. 
#
# Uses helper functions: selectAnimal(), setCageSize(), isYN()
#******************************************************************************

def getCageCapacity():
    userAnimal = selectAnimal()
    cageSize = setCageSize()
    if cageSize == 0:
        return
    elif isValidCageSize(userAnimal, cageSize):
        cageCapacity = int(cageSize/animal[userAnimal].getCageSize(1))
        print(f"Your cage can hold up to {cageCapacity} {userAnimal.title()}s.")
    else:     
        print("Error: Your cage is too small.")
        print(f"A cage size of at least {animal[userAnimal].getCageSize(1)} is required for one {userAnimal.title()}.")

    verify = input("Would you like to find the capacity for another cage? (y/n) ")
    if isYN(verify):
        getCageCapacity()
    else: 
        return
    
#******************************************************************************
#                          OPTION 4
# getCageEnvironment()
# Prints the ideal environment requirements for the given animal and cage size
#
# Uses helper functions: selectAnimal(), setCageSize(), isValidCageSize(), isYN
#******************************************************************************

def getCageEnvironment(): 
    userAnimal = selectAnimal()
    cageSize = setCageSize()
    if cageSize == 0: 
        return

    if not isValidCageSize(userAnimal, cageSize):
        print("WARNING: Your cage is too small for this animal.")
    
    details = animal[userAnimal].getTerrainDetails(cageSize)

    print("To create the idea environment in this cage you will need:")
    for detail in details: 
        print(detail)
    
    verify = input("Would you like to see environment details for another habitat? (y/n) ")
    if isYN(verify):
        getCageEnvironment()
    else: 
        return

#******************************************************************************
#                          OPTION 5
# dispInfo()
# Displays information about the game
#******************************************************************************

def dispInfo():
    print()
    print("This program is a tool you can use while building habitats in the "
            "2001 PC game Zoo Tycoon")
    print("It is designed as a companion to the Zoo Tycoon Guide "  
            "by Steven W. Carter, which can be found here:\n"
            "https://gamefaqs.gamespot.com/pc/472139-zoo-tycoon-2001/faqs/19545")
    print("Please refer to this excellent guide for details such as preferred "
            "foliage and special instructions as you are building habitats.")
    print()
    print("In future updates I plan to add Dinosaur Digs and Marine Mania animals, "
            "as well as add functionlity to calculate foliage and rocks for exhibits")
    print("I wrote this program because I was tired of calculating cage sizes "  
            "and habitat requirements manually. I hope it helps you too!")
    print("-Taylor Reed")
    print("2022")
    print()
    exit = input("Hit any key to return to main menu.")
    return


#******************************************************************************
#                       HELPER FUNCTIONS
#******************************************************************************

#***************************************
# # selectAnimal()
# Finds the animal that matches user
# search term. Returns an error if no match
# is found. If multiple possible matches are 
# found the narrowSearch function is called
#***************************************

def selectAnimal():
    while True: 
        try:
            searchTerm = input("Which animal are you building the cage for? ")
        except Exception as detail:
            print("Error:", detail)
        else:
            searchResults = []
            for animal in allAnimals:
                if searchTerm.lower() in animal:
                    searchResults.append(animal)
            if not searchResults:
                print("Error : No animals match this entry")
                while True: 
                    try:
                        verify = input("Would you like to view list of all animals? (y/n) ")
                    except Exception as detail:
                        print("Error:", detail)
                    else:
                        if isYN(verify):
                            printAll()
                        break
            elif len(searchResults) == 1: 
                while True:
                    try:
                        verify = input(f"Would you like to choose {searchResults[0].title()}? (y/n) ")
                    except Exception as detail:
                        print("Error:", detail)
                    else:
                        if isYN(verify):
                            return searchResults[0]
                        break
            else:
                userAnimal = narrowSearch(searchResults)
                return userAnimal
            

#***************************************
# narrowSearch(searchResults)
# Called by selectAnimal function if the
# user search input matches multiple
# animals. Prints list of all matches
# and prompts user to select the animal
#***************************************

def narrowSearch(searchResults):
    for i in range(len(searchResults)):
        print(f"{i+1}. {searchResults[i].title()}")
    print()
    while True:
        try:
            menuSelect = int(input("Choose an animal by number: "))
            if menuSelect < 1 or menuSelect > len(searchResults):
                    raise ValueError()
        except ValueError:
            print("Error: Enter a number from the list")
        except Exception as detail:
            print("Error:", detail)
        else:
            while True:
                try:
                    verify = input(f"Would you like to choose {searchResults[menuSelect - 1].title()}? (y/n) ")
                except Exception as detail:
                    print("Error:", detail)
                else:
                    if isYN(verify):
                        return searchResults[menuSelect -1]
                    break
                    
#***************************************
# isValidCageSize(userAnimal, cageSize)
# returns True if cage size is big enough,
# else returns False
#***************************************

def isValidCageSize(userAnimal, cageSize):
    minCageSize = animal[userAnimal].getCageSize(1)
    if minCageSize > cageSize:
        return False
    else:
        return True

#***************************************
# isYN(verify)
# Verification of input for y/n questions
#***************************************
def isYN(verify):
    while True: 
        if verify.lower() == "y":
            return True

        elif verify.lower() == "n":
            return False
        
        else: 
            verify = input("Answer y or n: ")
            
#***************************************
# setCageSize()
# Verifies user cage size input
#***************************************
def setCageSize(): 
    while True: 
        try:
            cageSize = int(input("Enter cage size as number of tiles "
                                    "or 0 to exit to main menu: "))
            if cageSize < 0: 
                raise ValueError()
        except ValueError:
            print("Error: Please enter a positive integer")
        except Exception as detail:
            print("Error:", detail)
        else:
            return cageSize

#******************************************************************************
#                       DRIVER
#******************************************************************************

print("\t\tZoo Tycoon Perfect Habitat Wizard")

while True: 
    menuSelect = dispMenu()
    if menuSelect == 1:
        printAll()
    elif menuSelect == 2:
        getMinCageSize()
    elif menuSelect == 3:
        getCageCapacity()
    elif menuSelect == 4: 
        getCageEnvironment()
    elif menuSelect == 5: 
        dispInfo()
    else: 
        print("See you next time!")
        break