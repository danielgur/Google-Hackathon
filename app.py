# Copyright 2012. Team Flower Power.
# Google Intern Hackathon
# 
# Team:
#	Daniel Gur
#	Elissa Wolf
#	Enrique Sada
# 	Huan Do
#

import os
import views
import models
import json

from flask import Flask
from flask import request, render_template, redirect, send_from_directory

app = Flask(__name__)
app.debug = True


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/kill/', methods=['GET', 'POST'])
def receiveSMS():
    word = request.values.get('Body', '').strip().lower()
    killers_number = int(request.values.get('From', ''))
    game = models.Game.GamesByUserNumber[killers_number]

    if word in utils.WORDS:
        users = game.getUsersByNumber
        killer = users[killers_number]
        target = kill.target
        if word == target.secret_word:
            killer.kills(target)
            if len(users) > 2:
                return sendSMS(killers_number, utils.getPartialCongrats() + 
                               "Your new target is: " + killer.target.name)
            else:
                for number, user in users:
                    sendSMS(number, "You freakin WON! Now you have the flower powers.")
                winners = ', '.join(users)
                for number, user in game.deadUsers:
                    sendSMS(user.number, "Loser. Congratulate these bad boys: " + winners)
                del game
                return 'ok'
        
    return sendRulesSMS(killers_number)


@app.route('/', methods=["GET"])
def createGame():
    return render_template('create_game.html')


@app.route('/startgame', methods=['POST'])
def startGame():
    game = models.Game()
    data = request.values['data']
    users = utils.parseUsers(data)
    bad_numbers = set()
    for user in users:
        if user.getGame() is not None:
            sendSMS(user.number, "Dude you are already in a game!")
            logging.warn("User: {0} {1} is already in a game!".format(
                    user.name, user.number))
            bad_numbers.add(user.number)
        else:
            try:
                sendSMS(user.number, "You have entered the gameroom: %s "
                        "Get ready. It's about to get real. "
                        "Your target will be sent shortly!" % game.name)
            except:
                logging.warn("User: {0} has an bad number: {1}".format(
                        user.name, user.number))
                bad_numbers.add(user.number)
    
    for bad_number in bad_numbers:
        del users[bad_number]

    if len(users) <= 2:
        for user in users:
            return sendSMS(user.number, "Sorry, there are not enough valid players. "
                           "the game cannot start.")
            
    else:
        for user in users:
            game.addUser(user)
        game.assignWords()
        game.assignTargets()
        for user in users:
            message = ("Welcome to the game, your target is: {0}. "
                       "Your secret word is: {1}".format(user.target.name, user.secret_word))
            sendSMS(user.number, message)
        return redirect("/games/" + game.name)


@app.route('/gamestatus', methods=['GET'])
def gameStatus():
    game_name = request.values['name']
    password = request.values.get('password')
    game = models.Game.getGame(game_name)
    anon = (game.password == password)
    return json.dumps([user.serialize(anon=anon) for user in 
                       models.Game.getGame(game_name).getKillList()])

@app.route('/games/<game_name>')
def dashboard(game_name):
    return render_template('dashboard.html', game_name=game_name)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
