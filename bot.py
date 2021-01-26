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
        chatid = r['message']['chat']['id']
        message = r['message']['text']
        hour = datetime.datetime.now().hour
        if (message == '/start'):
            if(hour<5 or hour>16):
                bot.send_message(chatid,'Бот доступен с 10:00 по 22:00')
            else:
                startBot(chatid, r)
        elif (message == '/help'):
            bot.send_message(chatid, 'Help info')
        else:
            if(hour<5 or hour>16):
                bot.send_message(chatid,'Бот доступен с 10:00 по 22:00')
            else:
                markup = telebot.types.InlineKeyboardMarkup(row_width=2)
                markup = getMenu(markup)
                bot.send_message(chatid, 'Выберите', reply_markup=markup)
                # rr = requests.get(URL+''+str(request.data))
        return jsonify(r)
    else:
        r = request.get_json()
        bot.send_message('500324557', 'text:\n' + str(r))
        return '<a href=\'login/\'>/login/</a><br> <a href=\'auth/\'>/auth/</a><br><a href=\'users/\'>/users/</a><br>'

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
