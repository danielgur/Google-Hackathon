from unittest import TestCase
from mockito import when, verify, mock, verify_all
from models import *

class gamesTest(TestCase):

    def tearDown(self):
        unstub()

    def testCreate(self):
        game = Game()

    def testAddUser(self):
        game = Game()
        user = User('a', 1)
        game.addUser(User('a', 1))

        self.assertEquals(user.getGame(), game)
        self.assertEquals(game.usersByNumber[user.number], user)

    def testAssignTargets(self):
        game = Game()
        users = User('a', 0), User('b', 1), User('c', 2)

        for user in users:
            game.addUser(user)

        self.assertEquals(game.getKillList, None)

        game.assignTargets()
        self.assertEquals(len(game.getKillList()), 3)
        
        user0, user1, user2 = game.getKillList()
        self.assertTrue(user0.target == user1)
        self.assertTrue(user1.target == user2)
        self.assertTrue(user2.target == user3)

        self.assertRaises(AssertionError, game.assignTargets)
        
    def testAssignWords(self):
        game = Game()
        users = User('a', 0), User('b', 1), User('c', 2)

        for user in users:
            game.addUser(user)
        
        for user in users:
            self.assertEquals(user.secret_word, None)
            
        game.assignWords()
        for user in users:
            self.assertTrue(isinstance(user.secret_word, str))
        
    def testKillUser(self):
        game = Game()
        users = User('a', 0), User('b', 1), User('c', 2)

        for user in users:
            game.addUser(user)
            
        game.assignTargets()
        
        killList = game.getKillList()
        killer = killList[0]
        target = killer.target

        self.assertEquals(len(killList), 3)
        self.assertContains(target.number, Game.GamesByUserNumber)
        self.assertEmpty(game.deadUsers())

        killer.kills(target)

        self.assertEquals(len(killList), 2)
        self.assertNotContains(target, killList)
        self.assertNotContains(target.number, Game.GamesByUserNumber)
        self.assertContains(target, game.deadUsers())
        
        user0, user1 = game.getKillList()
        self.assertEquals(user0.target, user1.target)
        self.assertEquals(user1.target, user0.target)
        
