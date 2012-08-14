from unittest import TestCase
from mockito import when, verify, mock, verify_all
from models import *

class usersTest(TestCase):

    def tearDown(self):
        unstub()

    def testSerialize(self):
        user = User('huan', 123, 'bar')
        target = User('joe', 321, 'car')
        user.target = target
        
        cereal = user.serialize()
        self.assertTrue(isinstance(cereal, dict))
        self.assertNotContains(cereal, 'name')
        self.assertNotContains(cereal, 'target_name')
        self.assertNotContains(cereal, 'color')

        cereal = user.serialize(anon=False)
        self.assertTrue(isinstance(cereal, dict))
        self.assertContains(cereal, 'name')
        self.assertContains(cereal, 'target_name')
        self.assertContains(cereal, 'color')
