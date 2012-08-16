import unittest
from mockito import when, verify, mock, unstub
from models import *

class gamesTest(unittest.TestCase):

    def tearDown(self):
        Game.flushAllGames()
        unstub()

    def testCreate(self):
        game = Game()

    def testAddUser(self):
        game = Game()
        user = TestUser('a', -1)
        game.addUser(user)

        self.assertEquals(user.getGame(), game)
        self.assertEquals(game.usersByNumber[user.number], user)

    def testAssignTargets(self):
        game = Game()
        users = TestUser('a', 0), TestUser('b', -1), TestUser('c', -2)

        for user in users:
            game.addUser(user)

        self.assertEquals(game.getKillList(), None)

        game.assignTargetsAndWords()
        self.assertEquals(len(game.getKillList()), 3)
        
        user0, user1, user2 = game.getKillList()
        self.assertTrue(user0.target == user1)
        self.assertTrue(user1.target == user2)
        self.assertTrue(user2.target == user0)

        self.assertRaises(AssertionError, game.assignTargetsAndWords)
        
    def testAssignWords(self):
        game = Game()
        users = TestUser('a', 0), TestUser('b', -1), TestUser('c', -2)

        for user in users:
            game.addUser(user)
        
        for user in users:
            self.assertEquals(user.secret_word, None)
            
        game.assignTargetsAndWords()
        for user in users:
            self.assertIsInstance(user.secret_word, str)
        
    def testKillUser(self):
        game = Game()
        users = TestUser('a', 0), TestUser('b', -1), TestUser('c', -2)

        for user in users:
            game.addUser(user)

        game.assignTargetsAndWords()

        killList = game.getKillList()
        killer = killList[0]
        target = killer.target

        killer.kills(target)

        self.assertEquals(len(killList), 2)
        self.assertNotIn(target, killList)
        self.assertNotIn(target.number, Game.GamesByUserNumber)
        self.assertIn(target, game.deadUsers())
        
        user0, user1 = game.getKillList()
        self.assertEquals(user0.target, user1)
        self.assertEquals(user1.target, user0)
        
if __name__ == '__main__':
    unittest.main()
