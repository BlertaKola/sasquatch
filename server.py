from flask_app import app

#import controllers
from flask_app.controllers import users
from flask_app.controllers import sightings


if __name__ == "__main__":
    app.run(debug = True)