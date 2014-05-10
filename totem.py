#####################################################
## Programma om een geschikte totemnaam te vinden
## Geschreven door Piet De Vaere
## Piet@devae.re
##
## This work is licensed under a
## Creative Commons Attribution 3.0 Unported License.
#####################################################

from datetime import datetime
from random import random
## Constante variables
aantal_totems = 396  

## Adjectievenlijst aanmaken
## formaat: [nummer, absolute frequentie, maximum, relative frequentie]
frequenties = [[i,0,0,0] for i in range(aantal_totems+1)]

def user_feedback(adjectief):
    """vraagt de gebruiker of een adjectief van toepassing is"""
    for i in range(5):
        respons = str(input("{}? ".format(adjectief)))
        if respons in {"yes", "y", "ja", "j", "1"}:
            return True
        elif respons in {"no", "n", "nee", "0"}:
            return False
        else:
            print("antwoorden met 'ja', 'nee', '0' of '1'")

## gebruiker vragen om naam
naam = str(input("Echte naam van de totemloze: "))

## gebruiken vragen welke adjectieven passen
adjectievenlijst = open("adjectievenlijst.txt", "r")
logfile = open("./logs/{} {}.txt".format(naam, str(datetime.now())), 'w')
print("Heeft {} de volgende eigenschappen?".format(naam))
for line in adjectievenlijst:

    ## Kijken of de lijn een opmerking is
    if line[0] == "#":
        pass

    ## Lijn parsen, en user input vragen
    else:
        line = line.strip()
        line = line.split(":")
        adjectief = line[0].strip()
        nummers = line[1].split(",")
      ##  feedback = user_feedback(adjectief)
        feedback = round(random())
        if feedback == True:
            logfile.write("{}: 1 \n".format(adjectief))
        else: 
            logfile.write("{}: 0\n".format(adjectief))
        for nummer in nummers:
            nummer = (int(nummer.strip()))
            frequenties[nummer][2] += 1
            if feedback == True:
                frequenties[nummer][1] += 1
adjectievenlijst.close()

## Resultaten verwerken
## relatieve frequenties aanmaken
for i in range(len(frequenties)):
    if frequenties[i][2] != 0:
        frequenties[i][3] = 100 * frequenties[i][1] // frequenties[i][2]
frequenties_gesorteerd = frequenties[1:] ## de [0,0] vooraan de lijst wegsmijten
frequenties_gesorteerd.sort(key = lambda x:  x[3], reverse = True)


## User feedback geven, en logfile aanvullen
print("")
logfile.write("################################\n")
print("{0:6} {1:9} {2}".format("Nummer", "Abs freq", "Rel freq (%)"))
logfile.write("{0:6} {1:9} {2}\n".format("Nummer", "Abs freq", "Rel freq (%)"))
for nummer in frequenties_gesorteerd:
    if nummer[1] > 0:
        print("{0:6} {1:9} {2}".format(str(nummer[0]), str(nummer[1]),str(nummer[3])))
        logfile.write("{0:6} {1:9} {2}\n".format(str(nummer[0]), str(nummer[1]),str(nummer[3])))

logfile.close()

