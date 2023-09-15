from ast import Delete
import bcrypt
import logging
import random

logger = logging.getLogger(__name__)    # logger object to log the errors, but why?

from basic_auth.models import User as UserModel # import the User model, call it UserModel to avoid confusion with User class

session_id_to_user_dict = {}    # dictionary to store session_id as key and user object as value

# to generate a session_id
def _generate_session_id():
    return random.randint(1, 2**16) << 32   # generate a random number between 1 and 2^16 and left shift it by 32 bits

class User:
    def __init__(self, id, name, email):
        self._id = id
        self._name = name
        self._email = email
    
    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_email(self):
        return self._email

# this method is called by login view which passes email_id, password
# and this method returns True, session_id if login is successful else False, error message
def login(email_id, password):
    user_df = UserModel.objects.filter(email=email_id).all()    # get the user with the given email_id
    # if no user with the given email_id log the error and return False
    if not user_df:                                     
        logger.warning('No user exist {}'.format(email_id))
        return False, "Incorrect email_id or password"

    user_df = user_df.values().first()  # get the first user from the user_df
    hashed_password = user_df['hashed_password'][2:-1]  # get the hashed password from the user_df
    hashed_password = hashed_password.encode('utf-8')   # encode the hashed password
    password = password.encode('utf-8')                 # encode the password
    
    if bcrypt.hashpw(password, hashed_password) != hashed_password: # if the encoded password and hashed password don't match
        logger.warning('Incorrect password from user {}'.format(email_id))  
        return False, "Incorrect email_id or password"

    user_obj = User(user_df['id'], user_df['name'], user_df['email'])   # create a user object with the user_df values
    session_id = _generate_session_id()
    while session_id in session_id_to_user_dict:    # if we get a duplicate session_id, generate a new one
        session_id = _generate_session_id()
    session_id_to_user_dict[session_id] = user_obj  # map the session_id to the user object
    return True, session_id

# called by logout view
def logout(session_id):
    if session_id not in session_id_to_user_dict:   # if its not a valid session_id, return False
        return False
    del session_id_to_user_dict[session_id] # delete the session_id from the dictionary and return True
    return True

# called by the register_user view
def register(name, email_id, password):
    user_df = UserModel.objects.filter(email=email_id).all()    
    if user_df:                                                    # if a user with given email exists
        logger.warning('User already exist {}'.format(email_id))   # log the error and return False
        return False, "User already exist"
    
    bytes = password.encode('utf-8')               # encode the password
    salt = bcrypt.gensalt()                        # generate a salt                           
    hash = bcrypt.hashpw(bytes, salt)              # hash the password with the salt
    user = UserModel(name=name, email=email_id, hashed_password=hash)   # create an instance of the User model
    user.save()                                         # save the instance to the database (write to db)
    return True, "" 

# used to get the user object from the session_id
def get_user(session_id):
    if session_id in session_id_to_user_dict:
        return session_id_to_user_dict[session_id]
    return None