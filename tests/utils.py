def ParseUsers(data):
    Users = {}
    for line in data.split('\n'):
        line = line.strip()
        number, name = line.split(',')
        name, number = name.strip(), int(number.strip())
        user = User(name=name, number=number)
        Users[number] = user
    return Users

def GetSecretWords(amount):
    return random.sample(WORDS, amount)

def KillerKilledTarget(killer, target):
    killer.target = target.target
    UsersKilled[target.number] = target
    del Users[target.number]
    for i, suser in enumerate(ShuffledUsers):
        if suser.number == target.number:
            del ShuffledUsers[i]

    message = "you've been removed from the game.. sucker."
    sendSMS(target.number, message)

    if len(Users.keys()) > 2:
        sendSMS(killer.number, getPartialCongrats() + "Your new target is: " + killer.target_name)

    else:
        endGame()

def EndGame():
    global Users
    Users = {}
    winners = ''
    for user in Users.values():
        sendSMS(user.number, "You freakin WON! Now you have the flower powers.")
        winners += user.name + ' '
    for user in UsersKilled.values():
        sendSMS(user.number, "Loser. Congratulate these bad boys: " + winners)


def getPartialCongrats():
    possibleMsgs = ["Nice kill. ",
                    "Great hunt. ",
                    "Get more blood on those hands. ",
                    "Headshot. ",
                    "MOFO is dead. ",
                    "Dead. ",
                    "Good work you beast. "]

    return random.choice(possibleMsgs) 


def sendSMS(to, text):
    logging.warn('sending a message to %s with content: %s' % (to,  text))
    client.sms.messages.create(to=to,
                               from_=os.environ['TWILIO_NUMBER'],
                               body=text)

def sendRulesSMS(to):
    sendSMS(to, "the fuck broah. follow the rules")

def gaming():
    return bool(Users)
