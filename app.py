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

from flask import Flask

app = Flask(__name__)
app.debug = True


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
