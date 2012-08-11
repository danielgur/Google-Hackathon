class User(object):
    # Users = []

    def __init__(self, name, number, target_name=None, target_number=None, secret_word=None):
        self.name = name
        self.number = int(number)

        self.target_name = target_name
        self.target_number = target_number
        self.secret_word = secret_word

    def serialize(self):
        return dict(name=self.name, 
                    number=self.number, 
                    target_number=self.target_number,
		              target_name=self.target_name,
                    secret_word=self.secret_word)
