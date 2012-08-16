# Copyright 2012. Team Flower Power.
# Google Intern Hackathon
# 
# Team:
#	Daniel Gur
#	Elissa Wolf
#	Enrique Sada
# 	Huan Do
#

import json
import logging
import models
import os
import twilio
import utils

from flask import Flask
from flask import request, render_template, redirect, send_from_directory

games_to_delete = set()

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

    users = game.getUsersByNumber()
    killer = users[killers_number]
    killer.messages.append(killer.name + ": " + word)
    if word in utils.WORDS:
        target = killer.target
        if word == target.secret_word:
            killer.kills(target)
            if len(users) > 2:
                return utils.sendSMS(killers_number, utils.getPartialCongrats() + 
                               " Your new target is: " + killer.target.name)
            else:
                for number, user in users.iteritems():
                    utils.sendSMS(number, "You freakin WON! Now you have the flower powers.")
                winners = ', '.join(user.name for user in users.values())
                for user in game.deadUsers():
                    utils.sendSMS(user.number, "Loser. Congratulate these bad boys: " + winners)
                games_to_delete.add(game)
                return 'ok'
        
    return utils.sendRulesSMS(killers_number)


@app.route('/', methods=["GET"])
def createGame():
    return render_template('create_game.html', games=models.Game.GamesByGameName.values())


@app.route('/startgame', methods=['POST'])
def startGame():
    global games_to_delete
    for game in games_to_delete:
        game.delete()
    games_to_delete = set()
    game = models.Game()
    data = request.values['data']
    users = utils.parseUsers(data)
    bad_users = set()
    for user in users:
        if user.isInGame():
            utils.sendSMS(user.number, "Dude you are already in a game!")
            logging.warn("User: {0} {1} is already in a game!".format(
                    user.name, user.number))
            bad_users.add(user)
        else:
            try:
                utils.sendSMS(user.number, "Get ready. It's about to get real. "
                              "Your target will be sent shortly!")
            except twilio.TwilioRestException:
                logging.warn("User: {0} has an bad number: {1}".format(
                        user.name, user.number))
                bad_users.add(user)
    
    for bad_user in bad_users:
        users.remove(bad_user)

    if len(users) <= 2:
        message = "Sorry, there are not enough valid players. The game cannot start."
        for user in users:
            utils.sendSMS(user.number, message)
        return message

    else:
        for user in users:
            game.addUser(user)
        game.assignTargetsAndWords()
        for user in users:
            message = ("Welcome to the game, your target is: {0}. "
                       "Your secret word is: {1}".format(user.target.name, user.secret_word))
            utils.sendSMS(user.number, message)

        testing = any(user.number <= 0 for user in users)
        if testing:
            return "/test/" + game.name
        else:
            return "/games/" + game.name


@app.route('/gamestatus/<game_name>', methods=['GET'])
def gameStatus(game_name):
    game = models.Game.getGame(game_name)
    return json.dumps({'aliveUsers': [user.serialize() for user in 
                                      models.Game.getGame(game_name).getKillList()],
                       'deadUsers': [user.serialize() for user in
                                     models.Game.getGame(game_name).deadUsers()]})
                           
                           
                           
                           

@app.route('/games/<game_name>')
def dashboard(game_name):
    return render_template('dashboard.html', game_name=game_name)

@app.route('/test/<game_name>')
def test_dashboard(game_name):
    return render_template('testdashboard.html', game_name=game_name)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
