import telebot
import re
import threading
from dvachFunc import Dvach_Functions
from databaseFunc import Database

bot = telebot.TeleBot('TOKEN')
api = Dvach_Functions()
database = Database()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Привет, я Алиса - бот, избавляющий тебя от нужды скроллить двач вручную")

@bot.message_handler(commands=['base'])
def send_welcome(message):
    bot.send_message(message.from_user.id, database.convertDBtostr(database.compileToModel()))


@bot.message_handler(content_types=['text'])
def answer_all(message):
    if re.match(r'топ', message.text.lower()):
        wordList = message.text.split(' ')
        for i in range(1, len(wordList)):
            buf = api.getBoardTop(wordList[i])
            for j in range(0, len(buf)):
                bot.send_message(message.from_user.id, buf[j])
    if re.match(r'рассылка', message.text.lower()):
        newUser = Database.User(message.chat.first_name + ' ' + message.chat.last_name, message.chat.id, ["b"], ["голова"])
        bot.send_message(message.from_user.id, database.addUser(newUser))
    if re.match(r'борда', message.text.lower()):
        print('void')
    if re.match(r'тег', message.text.lower()):
        print('void')


def sendTopByTimer():
    database = Database()
    for i in range(0, len(database.userList)):
        print(database.userList[i].chatId)
        for j in range(0, len(database.userList[i].boardsList)):
            buf = api.getBoardTop(database.userList[i].boardsList[j])
            if len(buf) > 0:
                for k in range(0, len(buf)):
                    bot.send_message(database.userList[i].chatId, buf[k])
    timerTag = threading.Timer(1800.0, sendTagByTimer)
    timerTag.start()


def sendTagByTimer():
    database = Database()
    for i in range(0, len(database.userList)):
        print(database.userList[i].chatId)
        tags = "✉️Рассылка по твоим меткам: "
        for j in range (0, len(database.userList[i].tagsList)):
            tags += (database.userList[i].tagsList[j] + ", ")
        tags = tags.rstrip(', ') + '✉️'
        bot.send_message(database.userList[i].chatId, tags)
        for j in range(0, len(database.userList[i].boardsList)):
            buf = api.getBoardWithTags(database.userList[i].boardsList[j], database.userList[i].tagsList)
            if len(buf) > 0:
                for k in range(0, len(buf)):
                    bot.send_message(database.userList[i].chatId, buf[k])
    timerTop = threading.Timer(1800.0, sendTopByTimer)
    timerTop.start()


#sendTopByTimer()
#sendTagByTimer()
bot.polling(none_stop=True)