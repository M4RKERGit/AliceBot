import telebot
import re
import threading
from dvachFunc import Dvach_Functions
import databaseFunc

bot = telebot.TeleBot('1680017281:AAHoT0r9rBoNcvrL_nDahdEY-7cyB6Nlydw')
api = Dvach_Functions()
database = databaseFunc.getDatabase()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Привет, я Алиса - бот, избавляющий тебя от нужды скроллить двач вручную")


@bot.message_handler(content_types=['text'])
def answer_all(message):
    if re.match(r'Борда', message.text):
        wordList = message.text.split(' ')
        for i in range(1, len(wordList)):
            bot.send_message(message.from_user.id, api.getBoardTop(wordList[i]))


def sendTopByTimer():
    localBase = databaseFunc.getDatabase()
    for i in range(0, localBase["totalUsers"]):
        print(localBase["userList"][i]["chatId"])
        for j in range(0, len(localBase["userList"][i]["boardsList"])):
            bot.send_message(localBase["userList"][i]["chatId"], api.getBoardTop(localBase["userList"][i]["boardsList"][j]))


def sendTagByTimer():
    localBase = databaseFunc.getDatabase()
    for i in range(0, localBase["totalUsers"]):
        print(localBase["userList"][i]["chatId"])
        for j in range(0, len(localBase["userList"][i]["boardsList"])):
            buf = api.getBoardWithTags(localBase["userList"][i]["boardsList"][j], localBase["userList"][i]["tagsList"])
            if len(buf) > 0:
                bot.send_message(localBase["userList"][i]["chatId"], buf)


timerTop = threading.Timer(3600.0, sendTopByTimer)
timerTop.start()
timerTag = threading.Timer(10.0, sendTagByTimer)
timerTag.start()
bot.polling(none_stop=True)