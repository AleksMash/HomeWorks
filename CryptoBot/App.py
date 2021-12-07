import telebot
from extensions import *


#инициализируем взаимодействие с ботом
bot = telebot.TeleBot(BOT_TOKEN)

#ответ на команды /start  и /help
@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = '''Чтобы начать работу введите команду в следующем формате, разделяя пробелами:\n <валюта, цену которой хотите узнать> \
<валюта, в которой надо узнать цену первой валюты> \
<количество первой валюты>
Обозначение валюты задавать трехбуквенной аббревиатурой.
 Для того, чтобы увидеть список всех доступных валют введите команду /values'''
    bot.reply_to(message, text)


#ответ на команду /values
@bot.message_handler(commands=['values'])
def show_values(message: telebot.types.Message):
    try:
        d: dict = API_Connector.get_values()
    except APIException as e:
        bot.reply_to(message, e.description)
    else:
        s = ''
        for k, v in d.items():
            s = s + k + " (" + v + ")" + '\n'
        text = f'В данный момент доступно {len(d)} валют.\n\nДоступные валюты:\n\n' + s
        bot.reply_to(message, text)


#ответ на текстовые сообщения
@bot.message_handler()
def get_rate(message: telebot.types.Message):
    if message.text == 'привет':
        bot.reply_to(message, 'И Вам не хворать!')
        return
    args = message.text.upper().split()
    if len(args)<3:
        bot.reply_to(message, 'введите команду в следующем формате, разделяя пробелами:\n <валюта, цену которой хотите узнать> \
<валюта, в которой надо узнать цену первой валюты> \
<количество первой валюты>\nВсе три параметра - обязательны')
        return
    try:
        rate = API_Connector.get_price(args[0],args[1],args[2])
    except APIException as e:
        bot.reply_to(message, e.description)
    else:
        bot.reply_to(message, str(rate))

bot.polling()

