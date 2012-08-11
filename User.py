class User(object):
    # Users = []

    def __init__(self, name, number, target_number=None):
        self.name = name
        self.number = int(number)
        self.target_number = target_number

    def serialize(self):
        return dict(name=self.name, 
                    number=self.number, 
                    target_number=self.target_number)
