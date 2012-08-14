from unittest import TestCase
from mockito import when, verify, mock
from models import User
import os
import app

class Test(TestCase):

    def testSendSMS(self):
        to, body = mock(), mock()
        messages = app.client.sms.messages = mock()
        app.sendSMS(to, body)
        verify(messages).create(to=to,
                                from_=os.environ['TWILIO_NUMBER'],
                                body=body)

    def testParseUsers(self):
        Users = app.parseUsers('8,huan\n'
                               '9,daniel')
        self.assertEquals(Users[8], User('huan', 8))
        self.assertEquals(Users[9], User('daniel', 9))

    def testGetSecretWords(self):
        self.assertEquals(len(app.getSecretWords(8)), 8)

    def testKillerKilledTarget(self):
        pass

    def testKillerKilledTargetEnd(self):
        Users = {8: User('huan', 8),
                 9: User('daniel', 9),
                 10: User('elissa', 10)}
        killer = Users[8]
        target = Users[9]
        app.killerKilledTarget(killer, target)
        

    def testEndGame(self):
        pass
