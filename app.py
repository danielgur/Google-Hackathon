# Copyright 2012. Team Flower Power.
# Google Intern Hackathon
# 
# Team:
#	Daniel Gur
#	Elissa Wolf
#	Enrique Sada
# 	Huan Do
#

import json
import logging
import os
import random
import twilio.twiml

from flask import Flask, request, render_template
from User import User
from twilio.rest import TwilioRestClient

client = TwilioRestClient()

app = Flask(__name__)
app.debug = True

Users = {}

UsersKilled = {}

ShuffledUsers = []

@app.route('/kill', methods=['GET', 'POST'])
def receiveSMS():
    # Get info of received SMS
    text_received = request.values.get('Body', '')
    sender_number = int(request.values.get('From', ''))

    # If user died, make necessary updates
    if text_received.strip().lower() == 'dead':
        dead_user = Users[sender_number]
        updateTarget(dead_user)
        
        # Add dead user to UsersKilled
        # Delete dead user from current players
        UsersKilled[sender_number] = dead_user 
        del Users[sender_number]
        del ShuffledUsers[sender_number]
        message = "you've been removed from the game.. sucker."
        sendSMS(sender_number, message)
    else:
        sendSMS(sender_number, "the fuck broah. follow the rules")

    # End game if there are two or less users
    if len(Users) <= 2:
      winners = ''
      for user in Users.values():
        sendSMS(user.number, "You freakin WON! Now you have the flower powers.")
        winners += user.name + ' '
      for user in UsersKilled.values():
        sendSMS(user.number, "Loser. Congratulate these bad boys: " + winners)

    return 'ok' 

def updateTarget(user_killed):
    for user in Users.values():
        if user.target_number == user_killed.number:
            user.target_number = user_killed.target_number  
            user.target_name = user_killed.target_name
            sendSMS(user.number, "Nice kill. Your new target is: " + user.target_name)
            break

def sendSMS(phone_num, text):
    from_="+19492163884"
    logging.warn('sending a message from %s to %s with content: %s' % (
            from_, phone_num,  text))
            
    message = client.sms.messages.create(to=phone_num, from_=from_,
                                         body=text)
    return message

def gaming():
    return bool(Users)

@app.route('/fake', methods=['GET'])
def fake():
    # this is just to initialize fake users,
    # so we can test without texting
    global Users
    Users = {
        17144175062: User(**{
                "target_name": "daniel gur",
                "target_number": 12169705010,
                "number": 17144175062,
                "name": "Huan"
                }),
        12169705010: User(**{
                "target_name": "Elissa",
                "target_number": 12165482911,
                "number": 12169705010,
                "name": "daniel gur"
                }),
        12165482911: User(**{
                "target_name": "Huan",
                "target_number": 17144175062,
            "number": 12165482911,
                "name": "Elissa"
                }),
        14822887950: User(**{
                "target_name": "Huan #2",
                "target_number": 12165482911,
                "number": 14822887950,
                "name": "daniel diaz"
                }),
        }
    return 'ok'


@app.route('/', methods=['GET'])
def index():
    if not gaming():
        return render_template('form.html')
    else:
        return render_template('dashboard.html')

@app.route('/startgame', methods=['POST'])
def poststartgame():
    data = request.values['data']

    global Users
    global ShuffledUsers
    Users = {}
    for line in data.split('\n'):
        line = line.strip()
        if not line:
            continue
        number, name = line.split(',')
        name, number = name.strip(), int(number.strip())
        user = User(name=name, number=number)
        Users[number] = user

    users_list = list(Users.values())
    for user in users_list[:]:
        try:
            sendSMS(user.number,
                   "Get ready. It's about to get real. Your target will be sent shortly.")
        except: 
            logging.warn("Catching exception for " + str(user.number) + " bout to delete...")
            del Users[user.number]
	    del ShuffledUsers[user.number]
            users_list.remove(user)
   
    random.shuffle(users_list)
    ShuffledUsers = users_list
    for i, user in enumerate(users_list):
        user.target_number = users_list[ (i + 1) % len(users_list)].number
        user.target_name = users_list[ (i + 1) % len(users_list)].name

    for i, user in enumerate(users_list):
        sendSMS(user.number,
                "Welcome to the game, your target is: " + Users[user.target_number].name)
        

    return 'ok'


@app.route('/gamestatus', methods=['GET'])
def gamestatus():
    global ShufflesUsers
    users = [user.serialize() for user in ShuffledUsers]
    return json.dumps(users)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
