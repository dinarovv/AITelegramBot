from user import User
from logger import Logger
from _private_info import _password, _token
from interface import admin_panel, models_list, hello_message, help_message

import telebot
import datetime
import threading
import os
import signal


bot = telebot.TeleBot(_token)

logger = Logger()
logger.start_log()

_password = _password

user_sessions = {}

def get_user_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = User(logger)
    return user_sessions[user_id]

def except_errors(message, error_text, _ex):
    bot.send_message(message.chat.id, 'Error!')
    text = f'{error_text}{_ex}'
    logger.write(text)
    print(text)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, hello_message, parse_mode='html')

@bot.message_handler(commands=['help'])
def show_help(message):
    bot.send_message(message.chat.id, help_message, parse_mode='html')

@bot.message_handler(commands=['admin'])
def admin(message):
    def process():
        try:

            user = get_user_session(message.from_user.id)
            user.username = message.from_user.username

            if not user.password_is_true:
                admin_check(message, user)
            elif user.password_is_true and not user.admin_rules:
                user.admin_rules = True
                bot.send_message(message.chat.id,
                                 'Success! You have admin rules right now!\nType /admin_shell to use your new features')
                logger.write(f'User {user.username} pretend to be an admin: Success')
            else:
                bot.send_message(message.chat.id,'You are already have admin rules')

        except Exception as _ex:
            except_errors(message, 'Error when user pretend to reach admin rules:', _ex)

    threading.Thread(target=process).start()

def admin_check(message, user):
    if _password == '':
        user.admin_rules = True
        bot.send_message(message.chat.id, 'Success! You have admin rules right now!\nType /admin_shell to use your new features')
        logger.write(f'User {user.username} pretend to be an admin: Success')
    else:
        wait_msg_1 = bot.send_message(message.chat.id, 'Please, enter a password..')
        bot.register_next_step_handler(
            wait_msg_1,
            lambda msg: process_admin_password(msg, user, wait_msg_1)
        )

def process_admin_password(message, user, wait_msg_1):
    bot.delete_message(chat_id=message.chat.id, message_id=wait_msg_1.message_id)
    user.user_input_password = message.text
    new_msg = user.be_admin()
    if user.admin_rules:
        logger.write(f'User {user.username} pretend to be an admin: Success')
    else:
        logger.write(f'An attempt to become an administrator from {user.username}: Failure')
    bot.send_message(message.chat.id, new_msg)

@bot.message_handler(commands=['admin_shell'])
def admin_shell(message):
    def process():
        try:
            user = get_user_session(message.from_user.id)
            user.username = message.from_user.username

            if user.admin_rules:
                admin_panel_msg = bot.send_message(message.chat.id, admin_panel, parse_mode='html')
                bot.register_next_step_handler(
                    admin_panel_msg,
                    lambda msg: choice(msg, user, user.system))
            else:
                bot.send_message(message.chat.id, 'You dont have enough rules to use this command')
        except Exception as _ex:
            except_errors(message, 'Error when use admin shell:', _ex)

    threading.Thread(target=process).start()

def choice(message, user, system):
    key = message.text
    if key in ['1', '2', 'q', 'Q']:
        if key == '1':
            key1_msg = bot.send_message(message.chat.id, models_list(user), parse_mode='html')
            bot.register_next_step_handler(
                key1_msg,
                lambda msg_1: select_model(msg_1, user, system)
            )
        elif key == '2':
            bot.send_message(message.chat.id, "Bot shutdown successfully!\nBye!")
            logger.write(f'User {user.username} use: SHUTDOWN.')
            os.kill(os.getpid(), signal.SIGTERM)
        else:
            bot.send_message(message.chat.id, user.exit_admin())
            user.logs.write(f'User {user.username} leave admin rules now!')

    else:
        bot.send_message(message.chat.id, 'Wrong key!')
        admin_panel_msg = bot.send_message(message.chat.id, admin_panel, parse_mode='html')
        bot.register_next_step_handler(
            admin_panel_msg,
            lambda msg: choice(msg, user, system))

def select_model(message, user, system):
    key = message.text
    old_m = user.model
    if key in ['1', '2', '3', '4', '5', 'q', 'Q']:
        if key == '1':
            system.model = user.model = 'gemma3:latest'
        elif key == '2':
            system.model = user.model = 'deepseek-r1:1.5b'
        elif key == '3':
            system.model = user.model = 'nomic-embed-text:latest'
        elif key == '4':
            system.model = user.model = 'qwen2.5-coder:1.5b-base'
        elif key == '5':
            system.model = user.model = 'llama3.1:8b'
        else:
            pass
        bot.send_message(message.chat.id, f'Model changed successfully! Model now is {user.model}')
        logger.write(f'{user.username} changed model from {old_m} to {user.model}')
    else:
        bot.send_message(message.chat.id, 'Wrong key!')
        key1_msg = bot.send_message(message.chat.id, models_list(user), parse_mode='html')
        bot.register_next_step_handler(
            key1_msg,
            lambda msg_1: select_model(msg_1, user, system)
        )


@bot.message_handler(content_types=['text'])
def send_prompt(message):
    def process():
        try:

            bot.send_chat_action(message.chat.id, 'typing')
            wait_msg = bot.send_message(message.chat.id, 'Please, wait..', disable_notification=True)

            user = get_user_session(message.from_user.id)
            user.username = message.from_user.username

            msg = telebot.formatting.escape_markdown(user.system.make_question(message.text))
            response = [msg]
            while len(response[-1]) > 4000:
                response = response[:-1] + [response[-1][:4000], response[-1][4000:]]

            bot.delete_message(chat_id=message.chat.id, message_id=wait_msg.message_id)
            for i in range(len(response)):
                bot.send_message(message.chat.id, response[i], parse_mode='MarkdownV2')
                msgtime = datetime.datetime.fromtimestamp(message.date)
                user.logs.write_json({user.system.model : {f'{msgtime} | {message.from_user.username}' : {message.text : response}}})

        except Exception as _ex:
            bot.delete_message(chat_id=message.chat.id, message_id=wait_msg.message_id)
            except_errors(message, 'Error while prompt:', _ex)

    # Запускаем обработку в отдельном потоке, чтобы не блокировать других пользователей
    threading.Thread(target=process).start()

bot.polling(none_stop=True)