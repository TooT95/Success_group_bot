import logging
import os
import telebot
import urllib.request
import json
from telebot import types

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackQueryHandler

bot_cur = telebot.TeleBot("1643817918:AAHUPAqxhS6sMQY5MjpuEdY_4p-sqj5TMkQ")


def start(bot, update):
    weburl = urllib.request.urlopen('https://javohirmr.pythonanywhere.com/auth/?chatid='+str(update.effective_message.chat_id))
    data = json.loads(weburl.read())
    result = data[0]['result']
    if(result=='not registered'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_request_contact = types.KeyboardButton('Отправить номер телефона',request_contact=True)
        markup.add(item_request_contact)
        strcur = "Здравствуйте. вы хотите учавствовать в нашем розыгрыше, если да тогда отправьте номер телефона, или нажмите на кнопку"
        bot_cur.send_message(update.effective_message.chat_id,strcur,reply_markup=markup)
    else:
        strcur = 'Приветсвую участник нашего розыгрыша'
        bot_cur.send_message(update.effective_message.chat_id,strcur)

def get_id(bot, update):
    update.effective_message.reply_text(update.effective_message.chat_id)

def echo(bot, update):
    update.effective_message.reply_text(update.effective_message.text)

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def getcallback(bot, update):
#     update.effective_message.reply_text(str(update['message']['contact']['phone_number']))
#      update.effective_message.reply_text("https://t.me/Success_group_bot")
    phone_number = str(update['message']['contact']['phone_number'])
    chat_id = str(update.effective_message.chat_id)
    markup = types.ReplyKeyboardRemove()
    weburl = urllib.request.urlopen('https://javohirmr.pythonanywhere.com/registerbot?chatid='+chat_id+'&phonenumber='+phone_number)
    data = json.loads(weburl.read())
    result = data[0]['result']
    if(result=='ok'):
        messagestr = data[1]['id']
        bot_cur.send_message(update.effective_message.chat_id, messagestr,reply_markup=markup)
    else:
        bot_cur.send_message(update.effective_message.chat_id, "При регистрации произошла ошибка, обратитесь к администратору",reply_markup=markup)

if __name__ == "__main__":
    # Set these variable to the appropriate values
    TOKEN = "1643817918:AAHUPAqxhS6sMQY5MjpuEdY_4p-sqj5TMkQ"
    NAME = "successgroupbot"

    # Port is given by Heroku
    PORT = os.environ.get('PORT')

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Set up the Updater
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    # Add handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('getid', get_id))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.contact, getcallback))
    dp.add_error_handler(error)

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    updater.idle()
