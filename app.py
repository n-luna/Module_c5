import telebot
from config import keys, TOKEN
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)

# При вводе команды /start или /help пользователю выводятся инструкции по применению бота

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Что бы начать работу, введите введите команду боту в следующем формате: \n \
<Имя  валюты> <в какую валюту перевести> <количество переводимой валюты>\n \
Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

# При вводе команды /values должна выводиться информация о всех доступных валютах в читаемом виде.

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Не правильно заданы параметры')

        quote, base, amount = values
        total_base = Converter.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} : {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)

