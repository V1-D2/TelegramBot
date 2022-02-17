import telebot
from telebot import types

import telebot
from telebot import types
from main import bot

userdata = {}
class User:

    number = ""
    name = ""

    def __init__(self, number, name):
        self.number = number
        self.name = name

    def setName(self, name):
        self.name = name
    def setNumber(self, number):
        self.number = number
    def getName(self):
        return self.name
    def getNumber(self):
        return self.number

@bot.message_handler(commands=['start'])
def get_name(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id, "Введите ваше имя пожалуйста:", reply_markup=markup)
    bot.register_next_step_handler(msg, get_number)
def get_number(message):
    user_id = message.from_user.id
    userdata[user_id] = User(message.text)
    msg = bot.send_message(message.chat.id, "Введите ваш телефон пожалуйста: ")
    bot.register_next_step_handler(msg, last_process)
def last_process(message):
    user_id = message.from_user.id
    user = userdata[user_id]
    user.number = message.text
    bot.send_message(message.chat.id, "Вы успешно зарегистрированы.")
