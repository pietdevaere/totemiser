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
from flask import Flask, url_for, redirect, render_template, request
from os import listdir
app = Flask(__name__)

def read_adjectives(inputFile):            
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
    f = open(result_path+name, 'w')
    for answer in answers:
        f.write(answer+'\n')

def readin(name = None):
    answers = set()
    if name == None:
        return anwers
    try:
        f = open(result_path+name)
    except:
        return answers
    for line in f:
        line = str(line.strip())
        answers.add(line)
    return answers

def list_users():
    return listdir(result_path)

@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        users = list_users()
        return render_template('login.html', users=users)

    if request.method == 'POST':
        return redirect(url_for('userpage', username=request.form['username']))
    

@app.route('/<username>', methods=['POST', 'GET'])
def userpage(username):
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
number_of_totems = 396  
frequencies = [[i,0,0,0] for i in range(number_of_totems+1)]
result_path = 'results/'


adjectives = read_adjectives('adjectievenlijst.txt')
sorted_adjectives = sorted(adjectives.keys())
app.debug = True
app.run()
