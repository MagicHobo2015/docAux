#------------------------------------------------------------------------------#
#   DocAux - This File will handel routing, now its kinda like a main.
#
#------------------------------------------------------------------------------#
import os
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

def load_env_variables():
    # For security.
    try:
        # load environment variables.
        load_dotenv(".env")
    # Catch no .env file.
    except FileNotFoundError:
        print("Oops! env file missing. ")

database_uri = os.environ['SQLALCHEMY_DATABASE_URI']
track_modifications = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']

def initialize_()-> Flask:    
    # initialize the app.
    docAux_backend = Flask(__name__)
    # So the orm can find the db
    docAux_backend.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    docAux_backend.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = track_modifications
    return docAux_backend



def main():
    # First load the vars.
    load_env_variables()

    # Configure everything now that the top secret vars are in place.
    docAux_api = initialize_()

    docAux_api.run(debug=True) # can add address or port here if needed.

    # Routing starts here.
    @docAux_api.route('/')
    # this is the function called when the above route is hit.
    def home():
        pass


if __name__ == '__main__':
    main()