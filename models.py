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

    def __del__(self):
        for number, user in self.userByNumber.iteritems():
            del GameByUserNumber[number]
        del GamesByGameName[game.name]

    def deadUsers(self):
        return self._deadUsers
        
    @staticmethod
    def getGame(name):
        return self.Games.get(name)

    def addUser(self, user):
        self.usersByNumber[user.number] = user
        self.GamesByUserNumber[user.number] = self

    def deleteUser(self, user):
        del self.usersByNumber[user.number]
        del self.GamesByUserNumber[user.number]

    def assignTargets(self):
        assert self._shuffledUsers is None, "Users are already shuffled!"
        self._shuffledUsers = random.shuffle(self.usersByNumber.values())
        for i, user in enumerate(self._shuffledUsers):
            user.target = self._shuffledUsers[(i+1) % len(self._shuffledUsers)]

    def assignWords(self):
        sample = random.sample(utils.WORDS, len(self.usersByNumber))
        for user, word in zip(self._shuffledUsers, sample):
            user.secret_word = word

    def getKillList(self):
        return self._shuffledUsers

    def getUsersByNumber(self):
        return self.usersByNumber

    def getDeadUsersByNumber(self):
        return self.deadUsersByNumber


class User(object):
    
    def __init__(self, name, number, secret_word=None, target=None):
        self.name = name
        self.color = utils.generateColor()
        self.kill_count = 0
        self.number = int(number)
        self.secret_word = secret_word
        self.target = target
        self.game_name = None

    def serialize(self, anon=True):
        if anon:
            return dict(kill_count=self.kill_count,
                        color=self.color)
        else:
            return dict(name=self.name,
                        number=self.number,
                        secret_word=self.secret_word,
                        target_number=self.target.number,
                        target_name=self.target.number,
                        kill_count=self.kill_count)

    def kills(killer, target):
        kill.target = target.target
        del target

    def getGame(self):
        return Games.GamesByUserNumber[self.number]

    def __del__(self):
        self.getGame().deleteUser(self)
    
