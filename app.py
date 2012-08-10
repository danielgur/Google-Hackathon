from flask import Flask, request

import os
import twilio.twiml

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET', 'POST'])
def hello():
    body = request.values.get('Body', '')
    resp = twilio.twiml.Response()
    message = "Hello, Mobile Monkey.. you just sent: " + body
    resp.sms(message)

    return str(resp)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
