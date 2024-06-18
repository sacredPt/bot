from telebot import types
from utils import read_json

config = read_json()

def start_keyboard():
    markup = types.InlineKeyboardMarkup()
    itembtn0 = types.InlineKeyboardButton(config['keyboard']['claimnote_button'], callback_data=f'claimnote_button')
    itembtn1 = types.InlineKeyboardButton(config['keyboard']['referalsystem_button'], callback_data=f'referalsystem_button')
    itembtn3 = types.InlineKeyboardButton(config['keyboard']['topuser_button'], callback_data=f'topuser_button')
    itembtn4 = types.InlineKeyboardButton(config['keyboard']['connectwallet_button'], callback_data=f'connectwallet_button')
    itembtn6 = types.InlineKeyboardButton(config['keyboard']['web_app_text_1'], web_app=types.WebAppInfo(config['domain_url']))
    
    markup.add(itembtn0, itembtn1)
    markup.add(itembtn3, itembtn4)
    markup.add(itembtn6)
    return markup

def claimnotcoin_keyboard():
    markup = types.InlineKeyboardMarkup()
    itembtn6 = types.InlineKeyboardButton(config['keyboard']['claimnotcoin_button'], web_app=types.WebAppInfo(config['domain_url']))
    markup.add(itembtn6)
    return markup

def admin_keyboard():
    markup = types.InlineKeyboardMarkup()
    itembtn0 = types.InlineKeyboardButton('💬 Broadcast', callback_data=f'admin_text_mailing')
    itembtn2 = types.InlineKeyboardButton('📊 Update Statistics', callback_data=f'admin_update_stats')
    markup.add(itembtn0, itembtn2)
    return markup