import telebot
import re
from dvachFunc import Dvach_Functions

bot = telebot.TeleBot('TOKEN')
api = Dvach_Functions()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Привет, я Алиса - бот, избавляющий тебя от нужды скроллить двач вручную")


@bot.message_handler(content_types=['text'])
def answer_all(message):
    if re.match(r'Борда', message.text):
        wordList = message.text.split(' ')
        for i in range(1, len(wordList)):
            bot.send_message(message.from_user.id, api.getBoard(wordList[i]))


bot.polling(none_stop=True)