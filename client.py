from twilio.rest import TwilioRestClient
import models

client = TwilioRestClient()

old_create = client.sms.messages.create

def new_create(to, from_, body):
    if int(to) <= 0:
        message = 'Server: ' + body
        models.User.getUser(number=to).messages.append(message)
        return message
    else:
        return old_create(to=to, from_=from_, body=body)

client.sms.messages.create = new_create
