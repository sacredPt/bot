import secrets
from utils import read_json

config = read_json()

def referal_system_lang(bot, name):
    txt = str(config['lang']['referal_system_lang']).replace('{0}', name).replace('{1}', bot).replace('{2}', str(secrets.token_hex(8)))
    return txt

def top_users_lang(user):
    txt = str(config['lang']['top_users_lang']).replace('{0}', user)
    return txt