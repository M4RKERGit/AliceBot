import telebot
import re
import threading
from dvachFunc import Dvach_Functions
import databaseFunc

bot = telebot.TeleBot('TOKEN')
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


def sendByTimer():
    localBase = database
    for i in range(0, localBase["totalUsers"]):
        print(localBase["userList"][i]["chatId"])
        for j in range(0, len(localBase["userList"][i]["boardsList"])):
            bot.send_message(localBase["userList"][i]["chatId"], api.getBoardTop(localBase["userList"][i]["boardsList"][j]))
    

timer = threading.Timer(3600.0, sendByTimer)
timer.start()
bot.polling(none_stop=True)