from PyQt5 import QtCore, QtGui, QtWidgets
from test import Ui_MainWindow
import random
import sys
import time

class myWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # Setup items here
        super(myWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # End setup

        # todo save___

        file = self.File()
        self.ui.WidgetManager.setCurrentIndex(0)

        # Actions for buttons. ALL BUTTONS MUST BE WRITTEN HERE
        # Main Menu New Game button
        self.ui.newGame_Button.clicked.connect(lambda: self.ui.WidgetManager.setCurrentIndex(1))  # go to faction sel

        # Faction selection button actions
        self.ui.galacticArmy_Button.clicked.connect(lambda: self.map_Display(file))  # go to map
        self.ui.rebellion_Button.clicked.connect(lambda: self.map_Display(file))  # go to map

        # Map Planet based button actions
        self.ui.rhenVar_Button.clicked.connect(lambda: self.movement_Display(file, "Rhen Var"))  # Select planet
        self.ui.mygeeto_Button.clicked.connect(lambda: self.movement_Display(file, "Mygeeto"))  # Select planet
        self.ui.mustafar_Button.clicked.connect(lambda: self.movement_Display(file, "Mustafar"))  # Select planet
        self.ui.geonosis_Button.clicked.connect(lambda: self.movement_Display(file, "Geonosis"))  # Select planet
        self.ui.kamino_Button.clicked.connect(lambda: self.movement_Display(file, "Kamino"))  # Select planet

        # Map toolbar actions for buttons
        self.ui.army_Button.clicked.connect(lambda: self.army_Display(file))
        self.ui.armyCancel_Button.clicked.connect(lambda: self.army_Cancel(file))

        # Movement screen button actions
        self.ui.fromTo_Cancel.clicked.connect(lambda: self.movement_Cancel(file))
        self.ui.fromTo_Send.clicked.connect(lambda: self.combat_Selector(file))

        # Army Display actions
        self.ui.armyCalculate_Button.clicked.connect(lambda: self.army_Calculate(file))
        self.ui.armyOrder_Button.clicked.connect(lambda: self.army_Order(file))

        # Economy Display actions
        self.ui.economy_Button.clicked.connect(lambda: self.economy_Display(file))
        self.ui.economyCancel_Button.clicked.connect(lambda:  self.economy_Cancel(file))

        # Economy numpad Display actions
        self.ui.economy0_Button.clicked.connect(lambda: self.numpad(file, "0"))
        self.ui.economy1_Button.clicked.connect(lambda: self.numpad(file, "1"))
        self.ui.economy2_Button.clicked.connect(lambda: self.numpad(file, "2"))
        self.ui.economy3_Button.clicked.connect(lambda: self.numpad(file, "3"))
        self.ui.economy4_Button.clicked.connect(lambda: self.numpad(file, "4"))
        self.ui.economy5_Button.clicked.connect(lambda: self.numpad(file, "5"))
        self.ui.economy6_Button.clicked.connect(lambda: self.numpad(file, "6"))
        self.ui.economy7_Button.clicked.connect(lambda: self.numpad(file, "7"))
        self.ui.economy8_Button.clicked.connect(lambda: self.numpad(file, "8"))
        self.ui.economy9_Button.clicked.connect(lambda: self.numpad(file, "9"))
        self.ui.economyE_Button.clicked.connect(lambda: self.numpad(file, "E"))  # Needs to be given a real function, otherwise this numpad will only be usable for the economy page
        self.ui.economyC_Button.clicked.connect(lambda: self.numpad(file, "C"))




        self.ui.endTurn_Button.clicked.connect(lambda: self.endTurn(file))










    # Start logic functions

    # Responsible for ensuring all labels are updated with the correct data
    # Initialized by picking a faction, or by hitting "Cancel" in any of the in game menus
    def map_Display(self, file):
        self.ui.rhenVarFaction_Label.setText(file.planet_dictionary["Rhen Var"].faction)
        self.ui.kaminoFaction_Label.setText(file.planet_dictionary["Kamino"].faction)
        self.ui.mygeetoFaction_Label.setText(file.planet_dictionary["Mygeeto"].faction)
        self.ui.mustafarFactio_Label.setText(file.planet_dictionary["Mustafar"].faction)
        self.ui.geonosisFaction_Label.setText(file.planet_dictionary["Geonosis"].faction)
        self.ui.Faction_Label.setText(file.player1.faction)
        self.ui.creditCount_Label.setText(str(file.player1.credits))

        self.ui.WidgetManager.setCurrentIndex(2)

    # Responsible for displaying the movement screen for the player to allocate troops for their movement
    # initiated by clicking any of the planets on the map
    def movement_Display(self, file, name):
        file.movement_ToFromCheck = not (file.movement_ToFromCheck)  # Toggles the check
        if file.movement_ToFromCheck == False:  # First click on a planet. Update the "From Information" here that you want on the trans page
            file.movement_Origin = name
            self.ui.fromPlanet_Label.setText(name)
            self.ui.fromTroops_Label.setText(str(file.planet_dictionary[name].troops))
            file.movement_Origin = file.planet_dictionary[name]  # FROM PLANET OBJECT
            self.ui.planetSelected_Label.setText("Planet Selected: " + name)


        else:  # Second Click

            file.movement_Destination = file.planet_dictionary[name]  # TO PLANET OBJECT

            # IMPORTANT: INITIALIZE and EDIT labels for all planets to show accurately


            print(1)
            self.ui.toTroops_Label.setText(str(file.movement_Destination.troops))
            self.ui.fromTroops_Label.setText(str(file.movement_Origin.troops))
            print(2)
            self.ui.toFaction_Label.setText(file.movement_Destination.faction)
            self.ui.fromFaction_Label.setText(file.movement_Origin.faction)
            self.ui.toFaction_Label.setAlignment(QtCore.Qt.AlignCenter)
            self.ui.fromFaction_Label.setAlignment(QtCore.Qt.AlignCenter)

            # End set up labels for planets

            if (file.movement_Origin.name == file.movement_Destination.name):  # Unacceptable planet selection criteria include not selecting the same planet, or a planet you do not control
                print("Check")  # Nothing happens if it violates  the rules
                self.ui.planetSelected_Label.setText("Planet Selected: ")
                # todo add a label to show which planet is currently selected

            elif not file.movement_Origin.faction == file.player1.faction:
                print("Check2")  # Nothing happens if planet selection violates rules
                self.ui.planetSelected_Label.setText("Planet Selected: ")
                print(file.movement_ToFromCheck)

            else:  # Planet selection is good, now do the following the prepare for the movement screen
                if file.movement_Destination.faction == "Neutral":
                    file.movement_Type = "Occupy"
                elif file.movement_Origin.faction == file.movement_Destination.faction:
                    file.movement_Type = "Reinforce"
                else:
                    file.movement_Type = "Assault"

                # Update the "To Information" here that you want on the trans page
                print(file.movement_Type)
                self.ui.toPlanet_Label.setText(name)
                self.ui.toTroops_Label.setText(str(file.planet_dictionary[name].troops))
                self.ui.movementStatus_Label.setText(file.movement_Type)
                # Now that all calculations are done, SHOW the actual movement screen with the correct labels
                self.ui.WidgetManager.setCurrentIndex(3)

    def combat_Selector(self, file):
        if int(self.ui.fromToInput_LineEdit.text()) > int(self.ui.fromTroops_Label.text()):
            self.ui.fromToInput_LineEdit.setText("")
        elif file.movement_Type == "Reinforce":  # Actions to take if the unit is reinforcing
            self.combat_Reinforce(file)
        else:  # Actions to take if unit is attacking/occupying
            self.combat_Basic(file)

    def combat_Reinforce(self, file):
        from_Troops = int(self.ui.fromTroops_Label.text())
        to_Troops = int(self.ui.toTroops_Label.text())
        sent_Troops = int(self.ui.fromToInput_LineEdit.text())

        file.planet_dictionary[self.ui.fromPlanet_Label.text()].troops = from_Troops - sent_Troops
        file.planet_dictionary[self.ui.toPlanet_Label.text()].troops = to_Troops + sent_Troops

        # Update labels for new Soldier amounts
        self.ui.toTroops_Label.setText(str(to_Troops + sent_Troops))  # How many attackers survived
        self.ui.fromTroops_Label.setText(str(from_Troops - sent_Troops))  # original amount - what you sent to attack

        self.ui.fromToInput_LineEdit.setText("")

    # Function generates battle and determines outcome dependent on what the player chose to send. Needs editing to be more complex/accurate
    # Uses input from the "Movement Display" func
    # initiated by the "Send" Button in movement display
    def combat_Basic(self, file):
        from_Troops = int(self.ui.fromTroops_Label.text())
        to_Troops = int(self.ui.toTroops_Label.text())
        sent_Troops = int(self.ui.fromToInput_LineEdit.text())
        count_from = 0
        self.ui.fromToInput_LineEdit.setText("")
        for i in range(sent_Troops):
            if to_Troops > 0:
                # BATTLE FORMULA GOES HERE!!!!!
                if random.randint(0,10) * file.player1.combatMultiplier < 3:  # Actions if "attacking" Soldier is successful
                    print(i)
                    count_from = count_from + 1
                    to_Troops = to_Troops - 1
                else:  # Actions if a Soldier is unsuccessful
                    print("")
                    # Do not count them
            else:  # Actions to take after enemy troops are all defeated
                count_from = count_from + 1  # Count the remaining Soldiers who didn't need to fight
                self.ui.movementStatus_Label.setText("Reinforce")  # Indicates moving here would actually reinforce instead of assault

        print("Soldiers Survived: " + str(count_from) + " Defenders survived: " + str(to_Troops))
        file.planet_dictionary[self.ui.fromPlanet_Label.text()].troops = from_Troops - sent_Troops + count_from
        self.ui.fromTroops_Label.setText(str(from_Troops - sent_Troops + count_from))
        file.planet_dictionary[self.ui.toPlanet_Label.text()].troops = to_Troops
        self.ui.toTroops_Label.setText(str(to_Troops))
        if to_Troops == 0:  # If you won the battle, do these actions
            # Update the proper troop counts per planet
            file.planet_dictionary[self.ui.toPlanet_Label.text()].troops = count_from
            file.planet_dictionary[self.ui.fromPlanet_Label.text()].troops = from_Troops - sent_Troops
            file.planet_dictionary[self.ui.toPlanet_Label.text()].faction = file.player1.faction  # Updates the planet to be player controlled

            # Update labels for new Soldier amounts
            self.ui.toTroops_Label.setText(str(count_from))  # How many attackers survived
            self.ui.fromTroops_Label.setText(str(from_Troops - sent_Troops))  # original amount - what you sent to attack

            # self.WidgetManager.setCurrentIndex(2)
            self.ui.fromToInput_LineEdit.setText("")
            self.ui.toFaction_Label.setText(file.player1.faction)

            # END BATTLE FORMULA

    # Responsible for returning from the movement screen back to the map and clearing the "Planet Selected" Field
    # initiated by clicking the cancel button on the movement display
    def movement_Cancel(self, file):
        self.ui.planetSelected_Label.setText("Planet Selected: ")
        self.map_Display(file)

    # Responsible for taking input from player to add Soldiers to the Army
    # Function must check input to ensure it is actually valid and can be added into the player's army at the location they want
    # initiated by clicking Army on the map
    def army_Display(self, file):
        # Add all planets the player controls to the combo selector. Happens each time you open the "Army" page
        faction = file.player1.faction
        for i in file.planet_dictionary:  # iterates through each planet in the game to check if they belong to the player
            if faction == file.planet_dictionary[i].faction:
                self.ui.armyPlanetSelection_Combo.addItem(file.planet_dictionary[i].name)
        self.ui.armyCredits_Label.setText("Credits: " + str(file.player1.credits))
        # Page is setup and can function
        self.ui.WidgetManager.setCurrentIndex(4)

    # Responsible for calculating the expected cost and upkeep of the Soldiers that you choose to order
    # initiated by clicking the "calculate" button on the Army page
    # Enables and disables the "Order" button on the page to be used based on if the order is larger than you can afford
    def army_Calculate(self, file):
        order = self.ui.armyInput_Entry.text()
        if order.isnumeric():  # input must be a number
            order = int(order)
            cost = order * file.soldier_Cost
            upkeep = order * file.soldier_Upkeep
            self.ui.armyCost_Label.setText("Cost: " + str(cost))
            self.ui.armyUpkeep_Label.setText("Upkeep: " + str(upkeep))
            if cost <= file.player1.credits:  # Sets the "Order" button to be enabled or not based on if you have enough money to actually purchase the order
                self.ui.armyOrder_Button.setEnabled(True)
            else:
                self.ui.armyOrder_Button.setEnabled(False)

    # Responsible for actually ordering and updating the Soldier count on the respective planet, and the new credit amount for the player
    def army_Order(self, file):
        order = int(self.ui.armyInput_Entry.text())
        for i in file.planet_dictionary:
            if self.ui.armyPlanetSelection_Combo.currentText() == file.planet_dictionary[i].name:
                file.planet_dictionary[i].troops = file.planet_dictionary[i].troops + order
        file.player1.credits = file.player1.credits - (order * file.soldier_Cost)
        self.ui.armyCredits_Label.setText("Credits: " + str(file.player1.credits))
        self.ui.creditCount_Label.setText(str(file.player1.credits))
        self.ui.armyOrder_Button.setEnabled(False)
        self.ui.armyInput_Entry.setText("")

    # Properly shuts out the Army window and clears the combo box
    # initiated by clicking the cancel button on the army page
    def army_Cancel(self, file):
        self.ui.armyPlanetSelection_Combo.clear()
        self.ui.armyOrder_Button.setEnabled(False)
        self.map_Display(file)

    def economy_Display(self, file):
        self.ui.economyCredits_Label.setText(str(file.player1.credits))
        self.ui.economyCreditsTurn_Label.setText(str(file.player1.creditsTurn))

        self.ui.economyIncome_Label.setText(str(file.player1.income))
        self.ui.economyTaxes_Label.setText(str(file.player1.taxes))
        self.ui.economyBonds_Label.setText(str(file.player1.bonds))

        self.ui.economyUpkeep_Label.setText(str(file.player1.upkeep))
        # self.ui.economyExpenses_Label.setText(str(file.player1.expenses))

        self.ui.WidgetManager.setCurrentIndex(5)


    def economy_Cancel(self, file):
        self.ui.economyTaxesOutput_Label.setText("")
        self.ui.WidgetManager.setCurrentIndex(2)



    # Used for unviersal purposes to input numbers into the game
    # Initiated anytime the player presses a key on a numpad
    # Takes one input single digit number, and outputs it when the "E" button is pressed
    def numpad(self, file, input):
        # Add a condition if the input is just legit too big
        if input.isnumeric():
            file.numpad = file.numpad + input
            self.ui.economyTaxesOutput_Label.setText(file.numpad)
        elif input == "C":
            file.numpad = ""
            self.ui.economyTaxesOutput_Label.setText(file.numpad)
        else:  # Actions to take when the numerical amount is properly entered. CHANGE this so the numpad works with other things
            self.ui.economyTaxes_Label.setText(file.numpad)

    # Responsible for actions taken when the player ends their turn
    # Initiated when the player elects to end the turn
    def endTurn(self, file):
        self.AI(file)  # Activate the AI to conduct their actions (See the AI function)
        file.player1.credits = file.player1.credits + file.player1.creditsTurn
        time.sleep(.5)
        self.map_Display(file)






    # Responsible for hosting the AI's decision making. Very complex part of the code
    # Initiated by the player ending their turn
    def AI(self, file):
        # Analyze self strength
        rankedSelf_Array = []
        AI_PlanetCount = 0  # Counts the number of planets the AI actively controls
        for i in file.planet_dictionary:
            if file.planet_dictionary[i].faction == file.player2.faction:
                rankedSelf_Array.append(file.planet_dictionary[i].troops)
                AI_PlanetCount = AI_PlanetCount + 1  # Counts the number of planets the AI actively controls
        print("AI Planet Count: " + str(AI_PlanetCount))
        print("Self planet strength determination complete")
        # Analyze enemy (player) self strength
        rankedEnemy_Array = []
        for i in file.planet_dictionary:
            if file.planet_dictionary[i].faction == file.player1.faction:
                rankedEnemy_Array.append(file.planet_dictionary[i].troops)
        print("Enemy strength determination complete")
        # Compare self strength to opponent by planet
        outmatch_Array1 = []
        outmatch_Array2 = []
        for i in file.planet_dictionary:  # AI planets
            for j in file.planet_dictionary:  # Opponent planets
                if file.planet_dictionary[i].faction == file.player2.faction:  # Inspect only player2 planets against...
                    if file.planet_dictionary[j].faction == file.player1.faction:  # Only player1 planets
                        if file.planet_dictionary[i].troops > file.planet_dictionary[j].troops:
                            outmatch_Array1.append(file.planet_dictionary[i])  # Record planet the AI outnumbers the player
                            outmatch_Array2.append(file.planet_dictionary[j])  # Record planet player is outmatched by the player

        print("Comparison with enemy complete")


        if len(outmatch_Array1) == 0:
            print("Soldier Buildup required")


        # Make an attacking decision to assault weaker player planets
        attackDecision = False
        if random.randint(0,9)  >= 4 and len(outmatch_Array1) != 0:  # 50/50 chance of the AI attacking
            attack = True
        else:
            attack = False
            print("NOT ATTACKING!")
        if attack == True:
            count_from = 0  # Count for player2 Soldiers surviving
            selectedPlanet = random.randrange(0, len(outmatch_Array1))  # Pick a random outmatch planet based on number of outmatches
            print(outmatch_Array2[selectedPlanet].troops)
            to_Troops = outmatch_Array2[selectedPlanet].troops  # Calculate the troops on the planet the AI intends to outmatch
            print(len(range(outmatch_Array1[selectedPlanet].troops)))
            for i in range(outmatch_Array1[selectedPlanet].troops):  # Begin the actual attack phase here
                if to_Troops <= 0:
                    count_from = count_from + 1
                elif random.randrange(0, 10) * file.player2.combatMultiplier < 3:
                    count_from = count_from + 1
                    to_Troops = to_Troops - 1
            if to_Troops <= 0:
                file.planet_dictionary[outmatch_Array2[selectedPlanet].name].faction = file.player2.faction
                file.planet_dictionary[outmatch_Array1[selectedPlanet].name].troops = 0  # Must change to reflect if AI decides not to send all of its Soldiers

            # Must figure out a way so AI doesn't send all their Soldiers
            file.planet_dictionary[outmatch_Array2[selectedPlanet].name].troops = count_from
            print("Surviving AI: " + str(count_from) + " Surviving Player: " + str(to_Troops))

        # Need to add in a plan for the AI to purchase Soldiers
        AI_TroopCount = 0
        for i in file.planet_dictionary:  # Totals up the number of Soldiers the AI has
            if file.planet_dictionary[i].faction == file.player1.faction:
                AI_TroopCount = file.planet_dictionary[i].troops + AI_TroopCount

        print(AI_TroopCount)
        for i in file.planet_dictionary:  # Determines if any planet is below a certain threshold of security
            if file.planet_dictionary[i].faction == file.player2.faction:
                if file.planet_dictionary[i].troops <= 1.3* AI_TroopCount:  # if there are less than a third of the total troops on the planet, prepare to purchase more
                    print("Purchase necessary")
                    if file.player2.credits > file.soldier_Cost * 10:
                        file.planet_dictionary[i].troops = file.planet_dictionary[i].troops + 10
                        print("purchase made")


        file.player2.credits = file.player2.credits + file.player2.creditsTurn

            # if len(outmatch_Array1) == 0 :



    class File():

        # Class to initialize each player in the game
        # This includes the player's name and the faction they play for
        class player():
            def __init__(self, name, faction):
                self.name = name
                self.faction = faction

                # Economy Variables
                self.credits = 600


                self.taxes = 100
                self.bonds = 50

                self.upkeep = 0

                self.expenses = self.upkeep  # add any other expenses here

                self.income = self.taxes + self.bonds  # Add other sources of income here
                self.creditsTurn = self.income - self.expenses  # The net of in/outflow




                # Combat variables
                self.combatMultiplier = .5

        # Class to initialize each planet in the game
        # Includes name, faction, number of troops present on the planet
        class planet():
            def __init__(self, name, troops, faction):
                self.name = name
                self.troops = troops
                self.faction = faction

        faction0 = "Neutral"
        faction1 = "Galactic Army"
        faction2 = "Rebellion"

        Player1 = player("1", "Galactic Army")
        Player2 = player("2", "Rebellion")


        rhenVar = planet("Rhen Var", 50, faction1)
        mygeeto = planet("Mygeeto", 70, faction1)
        mustafar = planet("Mustafar", 5, faction2)
        geonosis = planet("Geonosis", 32, faction2)
        kamino = planet("Kamino", 100, faction1)

        # faction 0 = neutral. 1 = GA, 2 = rebellion

        # "file" Initializes its global variables here to be carried through the entire script
        def __init__(self):
            self.index = 2  # Used for selecting the correct page

            self.player1 = self.Player1
            self.player2 = self.Player2


            self.movement_Origin = ""
            self.movement_Destination = ""
            self.movement_ToFromCheck = True
            self.movement_Type = ""

            self.planet_dictionary = {
                "Rhen Var": self.rhenVar,
                "Mygeeto": self.mygeeto,
                "Kamino": self.kamino,
                "Geonosis": self.geonosis,
                "Mustafar": self.mustafar,
            }

            self.soldier_Cost = 5
            self.soldier_Upkeep = 0


            self.numpad = ""

    # todo save






app = QtWidgets.QApplication(sys.argv)
application = myWindow()
application.show()
sys.exit(app.exec_())
