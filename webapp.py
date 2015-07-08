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

result_path = 'results/'
number_of_totems = 396  



def process_answers(user, answers):
    for adjective in user.adjectives.keys():
        if adjective in answers:
            for number in user.adjectives[adjective]:
                user.frequencies[number][1] += 1

def parse_questionaire(user):
    answers = set()
    for item in user.sorted_adjectives:
        try:
            request.form[item]
        except:
            pass
        else:
            answers.add(item)
    return answers
    
def calc_relative_freq(user):
    for ii in range((len(user.frequencies))):
        try:
            user.frequencies[ii][3] = round(100 * user.frequencies[ii][1] / user.frequencies[ii][2])
        except ZeroDivisionError:
            user.frequencies[ii][3] = 0
    freq_sorted = user.frequencies[1:] ## remove first entry
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

class User():
    
    def __init__(self):
        ## Nummerlijst aanmaken
        ## formaat: [nummer, absolute frequentie, maximum, relative frequentie]
        self.frequencies = [[i,0,0,0] for i in range(number_of_totems+1)]
        self.adjectives = self.read_adjectives('adjectievenlijst.txt')
        self.sorted_adjectives = sorted(self.adjectives.keys())

    def read_adjectives(self, inputFile):            
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
                    self.frequencies[number][2] += 1
                    numbers.append(number)
                adjectives[adjective] = numbers
        return adjectives

@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        users = list_users()
        return render_template('login.html', users=users)

    if request.method == 'POST':
        return redirect(url_for('userpage', username=request.form['username']))
    

@app.route('/<username>', methods=['POST', 'GET'])
def userpage(username):
    user = User()
    if request.method == 'POST':
        answers = parse_questionaire(user)
        process_answers(user, answers)
        writeout(answers, username)
        freq_sorted = calc_relative_freq(user)
        return render_template('results.html', results=freq_sorted)
        
    if request.method == 'GET':
        answers = readin(username)
        return render_template('questionaire.html', answers=answers,  adjectives=user.sorted_adjectives)

app.debug = True
app.run()
