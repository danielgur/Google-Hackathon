id = 0

class User(object):

    def __init__(self, name, number, targetid=None):
        global id
        id += 1
        self.id = id
        self.name = name
        self.number = number
        self.targetid = targetid

    def serialize(self):
        return self.id, self.name, self.number, self.targetid
