from flask import Flask, request, render_template
from User import User
import logging
import json
import os
import random
import twilio.twiml

from twilio.rest import TwilioRestClient

client = TwilioRestClient()

app = Flask(__name__)
app.debug = True

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
            })
    }
UsersKilled = {}

@app.route('/', methods=['GET', 'POST'])
def receiveSMS():
    text_received = request.values.get('Body', '')
    sender_number = request.values.get('From', '')

    if text_received.strip().lower() == 'dead':
        updateTarget(Users[int(sender_number)])
        del Users[int(sender_number)]
        message = "you've been removed from the game.. sucker."
        sendSMS(sender_number, message)
    else:
        sendSMS(sender_number, "the fuck broah. follow the rules")

    if len(Users) <= 2:
      winners = ''
      for user in Users:
        sendSMS(user.number, "You freakin WON! Now you have the flower powers.")
        winners += user.name + ' '
      for user in UsersKilled:
        sendSMS(user.number, "Loser.  Congratulate these bad boys: " + winners)
    return '' 

def updateTarget(user_killed):
    users = Users.values()
    for user in users:
        if user.target_number == user_killed.number:
            user.target_number = user_killed.target_number  
            user.target_name = user_killed.target_name
            sendSMS(user.number, "Your new target is: " + Users[user_killed.target_number].name)
            break
    

def sendSMS(phone_num, text):
    from_="+19492163884"
    logging.warn('sending a message from %s to %s with content: %s' % (
            from_, phone_num,  text))
            
    message = client.sms.messages.create(to=phone_num, from_=from_,
                                     body=text)
    return message

@app.route('/startgame', methods=['GET'])
def getstartgame():
    return render_template('form.html')

@app.route('/startgame', methods=['POST'])
def poststartgame():
    data = request.values['data']

    global Users
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
    random.shuffle(users_list)
    for i, user in enumerate(users_list):
        user.target_number = users_list[ (i + 1) % len(users_list)].number
        user.target_name = users_list[ (i + 1) % len(users_list)].name

    for i, user in enumerate(users_list):
        sendSMS(user.number,
                "Welcome to the game, your target is: " + Users[user.target_number].name)

    return 'ok'

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('status.html', **{'Users': Users.values()})

@app.route('/gamestatus', methods=['GET'])
def gamestatus():
    return json.dumps([user.serialize() 
                       for number, user in Users.items()])

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
