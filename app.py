from flask import Flask, request

import os
import twilio.twiml

from twilio.rest import TwilioRestClient

client = TwilioRestClient()

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET', 'POST'])
def hello():
    body = request.values.get('Body', '')
    resp = twilio.twiml.Response()
    message = "Hello, Mobile Monkey.. you just sent: " + body
    resp.sms(message)

    return str(resp)

def sendSMS(phone_num, text):
    message = client.sms.messages.create(to=phone_num, from_="+14155992671",
                                     body=text)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
