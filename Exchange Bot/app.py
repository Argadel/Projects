import telebot
from extensions import APIException, Convertor
from config import TOKEN, keys
import traceback

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = "I can help you to learn about currency exchange rate!(^˵◕ω◕˵^) \n \n " \
           "1. Enter <initial currency> \n " \
           "2. Enter <currency to exchange> \n " \
           "3. Enter <amount> \n \n " \
           "If you want to see available currency enter </values>"
    bot.send_message(message.chat.id, f"Hello, {message.chat.first_name}!")
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Available currency:"
    for cur in keys.keys():
        text = '\n'.join((text, cur))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('The number of attributes is wrong!')
        
        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Command error:\n{e}")
    #except Exception as e:
       # traceback.print_tb(e.__traceback__)
      #  bot.reply_to(message, f"Unknown error:\n{e}")
    else:
        bot.reply_to(message, answer)

bot.polling(none_stop=True)
