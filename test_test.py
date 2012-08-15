import os
import unittest

from mockito import when, verify, mock, unstub
from utils import *

class utilsTest(unittest.TestCase):

    def tearDown(self):
        unstub()


if __name__ == '__main__':
    unittest.main()
