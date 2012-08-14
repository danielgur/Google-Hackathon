from unittest import TestCase
from mockito import when, verify, mock, verify_all
from utils import *

class utilsTest(TestCase):

    def tearDown(self):
        unstub()

    def testSendSMS(self):
        to, body = mock(), mock()
        when(app.client.sms.messages).create(
            to=to,
            from_=os.environ['TWILIO_NUMBER'],
            body=body).thenReturn(None)

        sendSMS(to, body)
        verify_all()

    def testSendSMSRules(self):
        to = mock()
        body = "the fuck broah. follow the rules"
        when(app.client.sms.messages).create(
            to=to,
            from_=os.environ['TWILIO_NUMBER'],
            body=body).thenReturn(None)

        sendRulesSMS(to)
        verify_all()

    def testParseUsers(self):
        Users = parseUsers('8,huan\n' '9,daniel')
        self.assertEquals(Users[8], User('huan', 8))
        self.assertEquals(Users[9], User('daniel', 9))

    def testGetPartialCongrats(self):
        self.assertTrue(isinstance(getPartialCongrats(), str))

    def testGenerateColor(self):
        self.assertTrue(isinstance(generateColor(), str))
