import telebot
import re
import threading
from dvachFunc import Dvach_Functions
from databaseFunc import Database

#bot = telebot.TeleBot('1680017281:AAE-LqGo8fgDb1hR9KTjz9fdaVxT1athJwE')
bot = telebot.TeleBot('1883639644:AAFdX5EUYHdSYpYaQIEb75OeVM8nlenXP6Y')
api = Dvach_Functions()
database = Database()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.from_user.id, f"Привет, я Алиса - бот, избавляющий тебя от нужды скроллить двач вручную\n\nМогу выдать тебе топ 3 треда с любой борды - напиши *Топ* + борду(b, zog, vg)\nМожно получить несколько топов за одно сообщение, просто указывай борды через пробел\n⚡️⚡️⚡️\nКроме того, доступна рассылка каждые полчаса по твоим настройкам - напиши *Рассылка*\nПосле этого будет создан твой профиль настроек, который можно посмотреть с помощью команды *Профиль*\n⚡️⚡️⚡️\nБорда + название: добавит или уберёт указанную борду из твоего списка\n⚡️⚡️⚡️\nТег + название: добавит или уберёт указанный тег из твоего списка\n\nПриятного пользования!")

@bot.message_handler(commands=['base'])
def send_welcome(message):
    database.getDatabase()
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
    if re.match(r'профиль', message.text.lower()):
        bot.send_message(message.from_user.id, database.sendProfile(message.chat.id))
    if re.match(r'борда', message.text.lower()):
        wordList = message.text.split(' ')
        for i in range(1, len(wordList)):
            bot.send_message(message.from_user.id, database.reloadUser(message.chat.id, 'board', wordList[i]))
    if re.match(r'тег', message.text.lower()):
        wordList = message.text.split(' ')
        for i in range(1, len(wordList)):
            bot.send_message(message.from_user.id, database.reloadUser(message.chat.id, 'tag', wordList[i]))


def sendTopByTimer():
    database = Database()
    for i in range(0, len(database.userList)):
        print(database.userList[i].chatId)
        for j in range(0, len(database.userList[i].boardsList)):
            buf = api.getBoardTop(database.userList[i].boardsList[j])
            if len(buf) > 0:
                for k in range(0, len(buf)):
                    bot.send_message(database.userList[i].chatId, buf[k])
    timerTag = threading.Timer(3600.0, sendTagByTimer)
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
    timerTop = threading.Timer(3600.0, sendTopByTimer)
    timerTop.start()


sendTopByTimer()
#sendTagByTimer()
bot.polling(none_stop=True)