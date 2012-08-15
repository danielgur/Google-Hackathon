import os
import unittest

from mockito import when, verify, mock, unstub
from utils import *

class utilsTest(unittest.TestCase):

    def tearDown(self):
        unstub()

    def testSendSMS(self):
        to, body = mock(), mock()
        when(client.sms.messages).create(
            to=to,
            from_=os.environ['TWILIO_NUMBER'],
            body=body).thenReturn(None)

        sendSMS(to, body)
        verify(client.sms.messages).create(
            to=to,
            from_=os.environ['TWILIO_NUMBER'],
            body=body)


    def testSendSMSRules(self):
        to = mock()
        body = "the fuck broah. follow the rules"
        when(client.sms.messages).create(
            to=to,
            from_=os.environ['TWILIO_NUMBER'],
            body=body).thenReturn(None)

        sendRulesSMS(to)
        verify(client.sms.messages).create(
            to=to,
            from_=os.environ['TWILIO_NUMBER'],
            body=body)


    def testParseUsers(self):
        Users = parseUsers('8,huan\n' '9,daniel')
        self.assertEquals(len(Users), 2)

    def testGetPartialCongrats(self):
        self.assertIsInstance(getPartialCongrats(), str)

if __name__ == '__main__':
    unittest.main()
