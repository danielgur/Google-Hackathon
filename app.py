from flask import Flask, request, render_template
from User import User
import json
import os
import twilio.twiml

from twilio.rest import TwilioRestClient

client = TwilioRestClient()

app = Flask(__name__)
# app.debug = True

Users = []

@app.route('/', methods=['GET', 'POST'])
def hello():
    body = request.values.get('Body', '')
    resp = twilio.twiml.Response()
    message = "Hello, Mobile Monkey.. you just sent: " + body
    resp.sms(message)

    return str(resp)

def sendSMS(phone_num, text):
    message = client.sms.messages.create(to=phone_num, from_="+19492163884",
                                     body=text)

@app.route('/startgame', methods=['GET'])
def getstartgame():
    return render_template('form.html')

@app.route('/startgame', methods=['POST'])
def poststartgame():
    data = request.values['data']

    global Users
    Users = []
    for line in data.split('\n'):
        name, number = line.split(',')
        name, number = name.strip(), number.strip()
        user = User(name=name, number=number)
        Users.append(user)

    return 'ok'

@app.route('/gamestatus', methods=['GET'])
def gamestatus():
    return json.dumps([user.serialize() 
                       for user in Users])

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
