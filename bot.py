import os
import requests
import json
from flask import Flask, render_template, request, jsonify
import telebot
import datetime

REGISTER_KEY = "Register"
INFO_KEY = "Info"
COR_DATA_KEY = "cor_data"
NEXT_YEAR_KEY = "next_year"
PREV_YEAR_KEY = "prev_year"
COR_DATA_NAME = 'Корешок'
BACK_TO_LIST_KEY = 'back_to_list'
URL = "http://94.158.52.112:8080/UDN/hs/telegram/"
TOKEN = '1643817918:AAHUPAqxhS6sMQY5MjpuEdY_4p-sqj5TMkQ'

app = Flask(__name__)
bot = telebot.TeleBot(TOKEN)


@app.route('/', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        r = request.get_json()
        if ('callback_query' in r):
            chatid = r['callback_query']['from']['id']
            messageid = r['callback_query']['message']['message_id']
            inline_id = r['callback_query']['id']
            callbackquery_data = r['callback_query']['data']
            if (callbackquery_data == REGISTER_KEY):
                registering(chatid)
            elif (callbackquery_data == INFO_KEY):
                bot.send_message(chatid, 'Help info')
#             elif (callbackquery_data == COR_DATA_KEY):
#                 year = 2020
#                 fillFromYear(chatid, inline_id, messageid, r, year)
#             elif (callbackquery_data == PREV_YEAR_KEY):
#                 year = int(r['callback_query']['message']['text']) - 1
#                 fillFromYear(chatid, inline_id, messageid, r, year)
#             elif (callbackquery_data == NEXT_YEAR_KEY):
#                 year = int(r['callback_query']['message']['text']) + 1
#                 fillFromYear(chatid, inline_id, messageid, r, year)
#             elif (callbackquery_data == BACK_TO_LIST_KEY):
#                 backToList(chatid, inline_id, messageid)
#             elif (str(callbackquery_data)[0:3] == 'my_'):
#                 arr = str(callbackquery_data).split('_')
#                 text = 'Корешок за ' + getMounthName(str(arr[1])) + '.' + str(arr[2]) + '\n'
#                 rr = requests.get(
#                     URL + 'corData?id=' + str(chatid) + '&year=' + str(arr[2]) + '&month=' + str(
#                         arr[1]) + '&updateid=' + str(r['update_id']))
#                 bot.edit_message_text(text + str(rr.text), chatid, messageid, inline_id)
            else:
                bot.send_message(chatid, 'text:\n' + str(r))
        elif ('contact' in r['message']):
#             chatid = r['message']['from']['id']
#             phoneNumber = r['message']['contact']['phone_number']
#             removeKeyboard = telebot.types.ReplyKeyboardRemove(selective=None)
#             rr = requests.get(URL + 'register?id=' + str(chatid) + '&phonenumber=' + str(phoneNumber))
#             if (str(rr.text) == "Успешно"):
#                 bot.send_message(chatid, 'Вы успешно зарегистрированы', reply_markup=removeKeyboard)
#                 markup = telebot.types.InlineKeyboardMarkup(row_width=2)
#                 getMenu(markup)
#                 bot.send_message(chatid, 'Выберите ', reply_markup=markup)
#             else:
#                 bot.send_message(chatid, 'Сбой системы. Обратитесь к администратору', reply_markup=removeKeyboard)
        else:
#             chatid = r['message']['chat']['id']
#             message = r['message']['text']
#             hour = datetime.datetime.now().hour
#             if (message == '/start'):
#                 if(hour<5 or hour>16):
#                     bot.send_message(chatid,'Бот доступен с 10:00 по 22:00')
#                 else:
#                     startBot(chatid, r)
#             elif (message == '/help'):
#                 bot.send_message(chatid, 'Help info')
#             else:
#                 if(hour<5 or hour>16):
#                     bot.send_message(chatid,'Бот доступен с 10:00 по 22:00')
#                 else:
#                     markup = telebot.types.InlineKeyboardMarkup(row_width=2)
#                     markup = getMenu(markup)
#                     bot.send_message(chatid, 'Выберите', reply_markup=markup)
#                     # rr = requests.get(URL+''+str(request.data))
        return jsonify(r)
    else:
        r = request.get_json()
        bot.send_message('500324557', 'text:\n' + str(r))
        return '<a href=\'login/\'>/login/</a><br> <a href=\'auth/\'>/auth/</a><br><a href=\'users/\'>/users/</a><br>'


def fillFromYear(chatid, inline_id, messageid, r, year):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    getMounth(chatid, markup, r, year)
    uiPrevYear = telebot.types.InlineKeyboardButton('<', callback_data=PREV_YEAR_KEY)
    uiNextYear = telebot.types.InlineKeyboardButton('>', callback_data=NEXT_YEAR_KEY)
    markup.add(uiPrevYear, uiNextYear)
    uiData = telebot.types.InlineKeyboardButton('Назад', callback_data=BACK_TO_LIST_KEY)
    markup.add(uiData)
    bot.edit_message_text(str(year), chatid, messageid, inline_id, reply_markup=markup)


def getMenu(markup):
    uiData = telebot.types.InlineKeyboardButton(COR_DATA_NAME, callback_data=COR_DATA_KEY)
    markup.add(uiData)
    return markup


def getMounth(chatid, markup, r, year):
    rr = requests.get(
        URL + 'getMounths?id=' + str(chatid) + '&year=' + str(year) + '&updateid=' + str(r['update_id']))
    mounth = str(rr.text).split('_')
    if (mounth[0] == ''):
        return
    uiAdvance = ''
    if (len(mounth) % 2 == 1):
        lenarr = (len(mounth)) - 2
        uiAdvance = telebot.types.InlineKeyboardButton(
            getMounthName(mounth[mounth.__len__() - 1]) + ' ' + str(year),
            callback_data='my_' + str(mounth.__len__()) + '_' + str(year))
    else:
        lenarr = (len(mounth)) - 1
    countName = 1
    count = 0
    while (count <= lenarr):
        uiFirst = telebot.types.InlineKeyboardButton(getMounthName(mounth[count]) + ' ' + str(year),
                                                     callback_data='my_' + str(countName) + '_' + str(year))
        uiSecond = telebot.types.InlineKeyboardButton(getMounthName(mounth[count + 1]) + ' ' + str(year),
                                                      callback_data='my_' + str(countName + 1) + '_' + str(year))
        markup.add(uiFirst, uiSecond)
        count += 2
        countName += 2
    if (uiAdvance != ''):
        markup.add(uiAdvance)


def backToList(chatid, inline_id, messageid):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    markup = getMenu(markup)
    bot.edit_message_text('Выберите', chatid, messageid, inline_id, reply_markup=markup)


def get_info(chatid):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    uiCoreData = telebot.types.InlineKeyboardButton('Корешок', callback_data='cor_data')
    markup.add(uiCoreData)
    bot.send_message(chatid, 'Info', reply_markup=markup)


def registering(chatid):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    keyContact = telebot.types.KeyboardButton('Отправить контакт', request_contact=True)
    keyboard.add(keyContact)
    bot.send_message(chatid, 'Регистрация', reply_markup=keyboard)


def startBot(chatid, r):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    rr = requests.get(URL + 'auth?id=' + str(chatid) + '&updateid=' + str(r['update_id']))
    if (str(rr.text) == "False"):
        uiReg = telebot.types.InlineKeyboardButton('Регистрация', callback_data=REGISTER_KEY)
        uiInfo = telebot.types.InlineKeyboardButton('Информация', callback_data=INFO_KEY)
        markup.add(uiReg, uiInfo)
    else:
        uiCoreData = telebot.types.InlineKeyboardButton(COR_DATA_NAME, callback_data=COR_DATA_KEY)
        markup.add(uiCoreData)
    bot.send_message(chatid, 'Выберите', reply_markup=markup)


def getMounthName(item):
    if (str(item) == '1'):
        return "Январь"
    elif (str(item) == '2'):
        return "Февраль"
    elif (str(item) == '3'):
        return "Март"
    elif (str(item) == '4'):
        return "Апрель"
    elif (str(item) == '5'):
        return "Май"
    elif (str(item) == '6'):
        return "Июнь"
    elif (str(item) == '7'):
        return "Июль"
    elif (str(item) == '8'):
        return "Август"
    elif (str(item) == '9'):
        return "Сентябрь"
    elif (str(item) == '10'):
        return "Октябрь"
    elif (str(item) == '11'):
        return "Ноябрь"
    elif (str(item) == '12'):
        return "Декабрь"
    else:
        return "default"

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
