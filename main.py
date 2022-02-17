import telebot

from telebot.types import KeyboardButton
from File_for_working_with_EXEL import monthNowTR, findTheFreeDays, findFreeTime, scheduleVisit, findNameAndNumber, \
    provideTheListOfProcedures, addName, checkPhone, provideTheCost, getProcedure, getTime
from icecream import ic
from telebot import types


listOfMonthsForVisit = {1:"Января", 2:"Февраль", 3:"Март", 4:"Апрель",
                    5:"Май", 6:"Июнь", 7:"Июль", 8:"Август",
                    9:"Сентябрь", 10:"Октябрь", 11:"Ноябрь", 12:"Декабрь"}

TOKEN = "2109775535:AAG7yT6mgFA3v4voqzCXLv9X2sbyUXSBUj8"
bot = telebot.TeleBot(TOKEN)
# Registration


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    visit = KeyboardButton("Назначить процедуру")
    cost = KeyboardButton("Узнать цены")
    education = KeyboardButton("Узнать об обучении")
    markup.add(visit, cost, education)
    bot.send_message(message.chat.id, "Привет, посмотри на кнопки ниже) Хочешь начать?", reply_markup=markup)
    bot.send_message(chat_id=message.chat.id, text='Я вижу что вы новый клиент, пожалуйста поделитесь вашим номером. Так вам будет удобней с нами работать.')

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    code = call.data
    if(code.isdigit()):
        code = int(code)
        if code in listOfMonthsForVisit.keys():
            listOfFreeDays = findTheFreeDays(code)
            markup = telebot.types.InlineKeyboardMarkup()
            for i in range(len(listOfFreeDays)):
                markup.add(telebot.types.InlineKeyboardButton(text=listOfFreeDays[i] - 1, callback_data=str(listOfFreeDays[i]) +":"+str(code)))
            bot.send_message(chat_id=call.message.chat.id,
                             text='Давайте я вам помогу. Какой денб вым подходит?',
                             reply_markup=markup)
    elif(code[:4] == "proc"):
        procedureNumber = int(code[4:])
        cost = provideTheCost(procedureNumber)
        procedure = getProcedure(procedureNumber)
        bot.send_message(chat_id=call.message.chat.id,
                         text=f'Цена {procedure} составляет {cost} гривен')

    elif code[0] != "V":
        dayAndMonth = [int(i) for i in code.split(":")]
        freeTime = findFreeTime(dayAndMonth[0], dayAndMonth[1])
        markup = telebot.types.InlineKeyboardMarkup()
        for i in range(len(freeTime)):
            codeForCallback = "V" + str(dayAndMonth[0]) + ":" + str(i+3)+":"+str(dayAndMonth[1])
            markup.add(telebot.types.InlineKeyboardButton(text=freeTime[i],
                                                          callback_data=codeForCallback))
        bot.send_message(chat_id=call.message.chat.id,
                         text='Давайте выберем время)',
                         reply_markup=markup)
    elif code[0] == "V":
        code = code[1:]
        dayTimeMonth = [int(i) for i in code.split(":")]
        userId = call.from_user.id
        nameAndNumber = findNameAndNumber(userId)
        #if(nameAndNumber == -1):
         #   get_name(call)
        scheduleVisit(dayTimeMonth[0], dayTimeMonth[1],dayTimeMonth[2], nameAndNumber)
        print(str(dayTimeMonth[0]) + " "+ str(dayTimeMonth[1]) + " " + str(dayTimeMonth[2]))
        timeOfVisiting = getTime(dayTimeMonth[1], dayTimeMonth[2])
        bot.send_message(chat_id=call.message.chat.id, text=f'Всё получилось) Вы зарегестрировались на {dayTimeMonth[0]-1}.{dayTimeMonth[2]} на {timeOfVisiting} Надеемся на скорый везит)')






@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    mail = message.text

    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    #Answers for the Keyboard buttons
    elif message.text == "Назначить процедуру":
        arrayOfMonthsNowAndNext = monthNowTR()
        markup = telebot.types.InlineKeyboardMarkup()

        monthNow = telebot.types.InlineKeyboardButton(text=arrayOfMonthsNowAndNext[1],
                                                      callback_data=arrayOfMonthsNowAndNext[0])
        monthNext = telebot.types.InlineKeyboardButton(text=arrayOfMonthsNowAndNext[3],
                                                       callback_data=arrayOfMonthsNowAndNext[2])
        markup.add(monthNow, monthNext)
        bot.send_message(message.chat.id, "Давайте выберем время)", reply_markup=markup)

    elif message.text == "Узнать цены":
        listOfProcedures = provideTheListOfProcedures()
        markup = telebot.types.InlineKeyboardMarkup()
        for i in range(len(listOfProcedures)):
            markup.add(telebot.types.InlineKeyboardButton(text=listOfProcedures[i][0],
                                                          callback_data="proc" + str(listOfProcedures[i][1])))
        bot.send_message(chat_id=message.chat.id,
                         text='Какая процедура вас интересует?',
                         reply_markup=markup)
    elif message.text == "Узнать об обучении":
        bot.send_message(chat_id= message.chat.id, text = "Свяжитесь с нашим преподователем Оксаной: @DVueh")
    # registration phone
    elif(checkPhone(message.text)):
        addName(message.text, message.from_user.id)
        bot.send_message(message.chat.id, text = "Спасибо за предоставленный номер, хорощего дня.")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Посмотри на кнопки ниже. Если у вас остались вопросы, напиши /help.")
bot.polling(none_stop=True, interval=2)



