from ast import Delete
import bcrypt
import logging
import random

logger = logging.getLogger(__name__)

from basic_auth.models import User as UserModel

session_id_to_user_dict = {}

def _generate_session_id():
    return random.randint(1, 2**16) << 32

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


def login(email_id, password):
    try:
        user_df = UserModel.objects.get(email=email_id)
    except UserModel.DoesNotExist:
        logger.warning('No user exists with email {}'.format(email_id))
        return False, "Incorrect email or password"

    hashed_password = user_df.hashed_password.encode('utf-8')
    password = password.encode('utf-8')

    if not bcrypt.checkpw(password, hashed_password):
        logger.warning('Incorrect password for user {}'.format(email_id))
        return False, "Incorrect email or password"

    user_obj = User(user_df.id, user_df.name, user_df.email)
    session_id = _generate_session_id()
    while session_id in session_id_to_user_dict:
        session_id = _generate_session_id()
    session_id_to_user_dict[session_id] = user_obj
    return True, session_id


def logout(session_id):
    if session_id not in session_id_to_user_dict:
        return False
    del session_id_to_user_dict[session_id]
    return True

def register(name, email_id, password):
    user_df = UserModel.objects.filter(email=email_id).all()
    if user_df:
        logger.warning('User already exist {}'.format(email_id))
        return False, "User already exist"
    
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    user = UserModel(name=name, email=email_id, hashed_password=hash)
    user.save()
    return True, ""

def get_user(session_id):
    if session_id in session_id_to_user_dict:
        return session_id_to_user_dict[session_id]
    return None