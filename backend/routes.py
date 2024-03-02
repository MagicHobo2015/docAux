#------------------------------------------------------------------------------#
#   DocAux - This File will handel routing, now its kinda like a main.
#
#------------------------------------------------------------------------------#
import os
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from models import db


def load_env_variables():
    # For security.
    try:
        # load environment variables.
        load_dotenv(".env")
    # Catch no .env file.
    except FileNotFoundError:
        print("Oops! env file missing. ")

def initialize_()-> Flask:    
    # initialize the app. We use this for everything so it needs to be returned.
    docAux_backend = Flask(__name__)

    # just to make it clear this is coming from the environment.
    database_uri = os.environ['SQLALCHEMY_DATABASE_URI']
    track_modifications = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']

    # So the orm can find the db
    docAux_backend.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    docAux_backend.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = track_modifications
    return docAux_backend

def main():
    DEBUG = True
    # First load the vars.
    load_env_variables()

    # Configure everything now that the top secret vars are in place.
    docAux_api = initialize_()

    docAux_api.run(debug=True) # can add address or port here if needed.
    
    # This connects the database to the app.
    db.init_app(docAux_api)


    if DEBUG:
        with docAux_api.app_context():
            try:
                db.create_all()
                # just to check if anything will work.
                db.session.execute(text('SELECT 1'))
                print('Connection successful !')
            # This lets us know what the error was, for whack-a-mole.
            except Exception as e:
                print('Connection failed ! ERROR : ', e)




    # Routing starts here.
    @docAux_api.route('/')
    # this is the function called when the above route is hit.
    def home():
        pass

<<<<<<< 1f99f6140ab5d7f471584613f37573f94912195b
=======
    # we can talk about what the actual urls end up being.
    @docAux_api.route('/create_user', methods=['POST'])
    def create_user():
        data = request.get_json()
        username = data.get('username')
        email = data.get('eamil')

        # need these to create a user, there is more just not yet.
        if not username or not email:               
                                # TODO: make these error codes mean something
            return jsonify({'message': 'Username and email are required'}), 400
        
        # Now make sure that the user doesnt already exist.
        user_check = User.query.filter_by(username=username).first()
        if user_check:
                                # TODO: make these error codes mean something
            return jsonify({'message': 'Username already exists'}), 400
        
        email_check = User.query.filter_by(email=email).first()
        if email_check:
            return jsonify({'message': 'User With That Email Adress Already\
                             exists'}), 400
        
        # here we have everything confirmed, its time to add the user
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        
        message = f'User {username} with Email address {email}, Created\
            succesfully!'
        return jsonify({'message': message})

>>>>>>> Not many changes just updating the branch cause we have class today, most work has been done to backend database connection

if __name__ == '__main__':
    main()