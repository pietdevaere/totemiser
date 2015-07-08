###################################################
## Programma om een geschikte totemnaam te vinden
## Geschreven door Piet De Vaere
## Piet@devae.re
## This code was written quick and dirty
##
## This work is licensed under a
## Creative Commons Attribution 3.0 License.
#####################################################

from datetime import datetime
from random import random
from flask import Flask, render_template, request
app = Flask(__name__)

aantal_totems = 396  


## User feedback geven, en logfile aanvullen
def give_feedback(logfile, frequenties_gesorteerd):
    print("")
    logfile.write("---------------------------------------\n")
    print("{0:6} {1:9} {2}".format("Nummer", "Abs freq", "Rel freq (%)"))
    logfile.write("{0:6} {1:9} {2}\n".format("Nummer", "Abs freq", "Rel freq (%)"))
    for nummer in frequenties_gesorteerd:
        if nummer[1] > 0:
            print("{0:6} {1:9} {2}".format(str(nummer[0]), str(nummer[1]),str(nummer[3])))
            logfile.write("{0:6} {1:9} {2}\n".format(str(nummer[0]), str(nummer[1]),str(nummer[3])))
    print("{0:6} {1:9} {2}".format("Nummer", "Abs freq", "Rel freq (%)"))

def user_feedback(adjectief):
    """vraagt de gebruiker of een adjectief van toepassing is"""
    for i in range(5):
        respons = str(input("{}? ".format(adjectief)))
        if respons in {"yes", "y", "ja", "j", "1"}:
            return True
        elif respons in {"no", "n", "nee", "0"}:
            return False
        elif respons in {"quit", "q"}:
            exit()
        else:
            print("antwoorden met 'j','ja', 'n', 'nee', '0' of '1'")


        
def read_file(naam):
    answers = {}

    ## first skip through the first lines of the adjectievenfile
    ## coppy the first part of the logfile to the new logfile
    try:
        inputfile = open("./logs/{}.txt".format(naam), 'r') 
        inputlines = inputfile.readlines()
        inputfile.close()
    except FileNotFoundError:
        print("No previous test of {} found, starting new test".format(naam))
        return {}
    
    logfile = open("./logs/{}.txt".format(naam), 'w')  
    for line in inputlines:
        if line[0] == "-":
            break
  ##    logfile.write(line)
        line = line.strip()
        adjectief, answer = line.split(":")[0:2]
        answer = int(answer.strip())
        answers[adjectief] = answer
    
    return answers

def read_adjectives(inputFile):            
##  logfile = open("./logs/{}_{}.txt".format(naam, str(datetime.now())), 'w')
    ## Door alle adjectieven loopen
    adjectives = {}
    for line in open(inputFile, 'r'):
        ## Kijken of de lijn een opmerking is
        if line[0] == "#":
            pass
        else:
            line = line.strip()
            line = line.split(":")
            adjective = line[0].strip()
            text_numbers = line[1].strip().split(",")
            numbers = []
            for number in text_numbers:
                number = int(number)
                frequencies[number][2] += 1
                numbers.append(number)
            adjectives[adjective] = numbers
    return adjectives


def process_answers(answers):
    for adjective in adjectives.keys():
        if adjective in answers:
            for number in adjectives[adjective]:
                frequencies[number][1] += 1
    

def parse_questionaire():
    print(request.form)
    answers = set()
    for item in sorted_adjectives:
        try:
            request.form[item]
        except:
            pass
        else:
            answers.add(item)
    return answers
    
def calc_relative_freq():
    for ii in range((len(frequencies))):
        try:
            frequencies[ii][3] = round(100 * frequencies[ii][1] / frequencies[ii][2])
        except ZeroDivisionError:
            frequencies[ii][3] = 0
    freq_sorted = frequencies[1:] ## remove first entry
    freq_sorted.sort(key = lambda x:  x[3], reverse = True)
    return freq_sorted

def writeout(answers, name):
    path = 'results/'
    f = open(path+name, 'w')
    for answer in answers:
        f.write(answer+'\n')

def readin(name = None):
    path = 'results/'
    answers = set()
    if name == None:
        return anwers
    try:
        f = open(path+name)
    except:
        return answers
    for line in f:
        line = str(line.strip())
        answers.add(line)
    return answers



@app.route('/<username>', methods=['POST', 'GET'])
def index(username):
    if request.method == 'POST':
        answers = parse_questionaire()
        process_answers(answers)
        writeout(answers, username)
        freq_sorted = calc_relative_freq()
        return render_template('results.html', results=freq_sorted)
        
    if request.method == 'GET':
        answers = readin(username)
        return render_template('questionaire.html', answers=answers,  adjectives=sorted_adjectives)

## Adjectievenlijst aanmaken
## formaat: [nummer, absolute frequentie, maximum, relative frequentie]
frequencies = [[i,0,0,0] for i in range(aantal_totems+1)]

adjectives = read_adjectives('adjectievenlijst.txt')
sorted_adjectives = sorted(adjectives.keys())
app.debug = True
app.run()

## check what program to exexute    
##valid = 0
##while valid == 0:
##    task = str(input("[N]ew test, or [o]pen and old file? "))
##    if task in ("new", "NEW", "New", "N", "n", ""):
##        ## gebruiker vragen om naam
##        naam = str(input("Echte naam van de totemloze: "))
##        proces_list({}, naam)
##        valid = 1
##
##    elif task in ("open", "OPEN", "Open", "O", "o"):
##        ## gebruiker vragen om naam
##        naam = str(input("Echte naam van de totemloze: "))
##        answers = read_file(naam)
##        proces_list(answers, naam)
##        valid = 1
##
##    elif task in ("quit", "exit", "q"):
##        exit()
##
##input("Druk enter om af te sluiten")

