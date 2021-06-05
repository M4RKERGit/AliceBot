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


def sendTopByTimer():
    localBase = databaseFunc.getDatabase()
    for i in range(0, len(localBase["userList"])):
        print(localBase["userList"][i]["chatId"])
        for j in range(0, len(localBase["userList"][i]["boardsList"])):
            buf = api.getBoardTop(localBase["userList"][i]["boardsList"][j])
            if len(buf) > 0:
                for k in range(0, len(buf)):
                    bot.send_message(localBase["userList"][i]["chatId"], buf[k])
    timerTop = threading.Timer(3600.0, sendTopByTimer)
    timerTop.start()


def sendTagByTimer():
    localBase = databaseFunc.getDatabase()
    for i in range(0, len(localBase["userList"])):
        print(localBase["userList"][i]["chatId"])
        tags = "✉️✉️✉️Рассылка по твоим меткам: "
        for j in range (0, len(localBase["userList"][i]["tagsList"])):
            tags += (localBase["userList"][i]["tagsList"][j] + ", ")
        tags = tags.rstrip(', ') + '✉️✉️✉️'
        bot.send_message(localBase["userList"][i]["chatId"], tags)
        for j in range(0, len(localBase["userList"][i]["boardsList"])):
            buf = api.getBoardWithTags(localBase["userList"][i]["boardsList"][j], localBase["userList"][i]["tagsList"])
            if len(buf) > 0:
                for k in range(0, len(buf)):
                    bot.send_message(localBase["userList"][i]["chatId"], buf[k])
    timerTag = threading.Timer(1800.0, sendTagByTimer)
    timerTag.start()


timerTop = threading.Timer(3600.0, sendTopByTimer)
timerTop.start()
timerTag = threading.Timer(1800.0, sendTagByTimer)
timerTag.start()
bot.polling(none_stop=True)