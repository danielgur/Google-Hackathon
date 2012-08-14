from twilio.rest import TwilioRestClient
import models
client = TwilioRestClient()

WORDS = {"blue", "robust", "scalable", "dynamic", "red", "amigo", "respect", "alfred", "beast",
         "welissa", "yoyo", "quique", "trivial", "regina", "sad", "day", "pedrophile", "insanity",
         "dig", "hendo", "boy", "bru", "shelton", "harvey", "g4lint", "omg", "potter", "harry",
         "dumbledore", "gatsby", "google", "bigtable", "megastore", "git", "sweet", "cheese",
         "gouda", "ferr", "china"}

PARTIAL_CONGRATS = {"Nice kill", "Great hunt", "Get more blood on those hands", "Headshot",
                    "MOFO is dead", "Dead", "Good work you beast"}

def getPartialCongrats():
    return random.choice(PARTIAL_CONGRATS)

def sendSMS(to, text):
    text = "\n\n" + text
    from_="+19492163884"
    logging.warn('sending a message to %s with content: %s' % (to, text))
    message = client.sms.messages.create(to=to, from_=from_, body=text)
    return message

def sendRulesSMS(to):
    return sendSMS(to, "the fuck broah. follow the rules")

def parseUsers(string):
    users = set()
    for line in string:
        number, name = line.split()
        user = models.User(name=name, number=number)
        users.add(user)
    return users

def generateColor():
    return (random.randint(0, 255), 
            random.randint(0, 255), 
            random.randint(0, 255))
