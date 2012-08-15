import random
import utils

class Game(object):
    # Game by game name
    GamesByGameName = {}

    # Should we allow users to be in more than one game?
    GamesByUserNumber = {}
        
    def __init__(self, name=None):
        # TODO(doboy): make sure the name is unique
        self.name = name or random.choice(utils.WORDS)
        self.password = random.choice(utils.WORDS)
        self.usersByNumber = {}
        self._deadUsers = set()
        self._shuffledUsers = None
        self.GamesByGameName[self.name] = self

    def delete(self):
        for number, user in self.usersByNumber.iteritems():
            del Game.GamesByUserNumber[number]
        del Game.GamesByGameName[self.name]

    def deadUsers(self):
        return self._deadUsers
        
    @classmethod
    def flushAllGames(cls):
        Game.GamesByGameName = {}
        Game.GamesByUserNumber = {}

    @staticmethod
    def getGame(name):
        return self.Games.get(name)

    def addUser(self, user):
        self.usersByNumber[user.number] = user
        self.GamesByUserNumber[user.number] = self

    def deleteUser(self, user):
        del self.usersByNumber[user.number]
        del self.GamesByUserNumber[user.number]
        del self._shuffledUsers[self._shuffledUsers.index(user)]
        self._deadUsers.add(user)

    def assignTargetsAndWords(self):
        assert self._shuffledUsers is None, "Users are already shuffled!"
        self._shuffledUsers = self.usersByNumber.values()
        random.shuffle(self._shuffledUsers)
        sample = random.sample(utils.WORDS, len(self.usersByNumber))
        for i, (user, word) in enumerate(zip(self._shuffledUsers, sample)):
            user.secret_word = word
            user.target = self._shuffledUsers[(i+1) % len(self._shuffledUsers)]

    def getKillList(self):
        return self._shuffledUsers

    def getUsersByNumber(self):
        return self.usersByNumber

    def getDeadUsersByNumber(self):
        return self.deadUsersByNumber


class User(object):
    
    def __init__(self, name, number, secret_word=None, target=None):
        self.name = name
        self.number = int(number)
        self.secret_word = secret_word
        self.target = target
        self.game_name = None

    def serialize(self, anon=True):
        return dict(name=self.name,
                    number=self.number,
                    secret_word=self.secret_word,
                    target_number=self.target.number,
                    target_name=self.target.number)

    def kills(killer, target):
        killer.target = target.target
        target.delete()

    def getGame(self):
        return Game.GamesByUserNumber[self.number]

    def delete(self):
        self.getGame().deleteUser(self)
