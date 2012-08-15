import unittest
from mockito import when, verify, mock, unstub
from models import *

class usersTest(unittest.TestCase):

    def tearDown(self):
        unstub()

    def testSerialize(self):
        user = User('huan', 123, 'bar')
        target = User('joe', 321, 'car')
        user.target = target
        user.serialize()

if __name__ == '__main__':
    unittest.main()
