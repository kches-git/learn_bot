import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings
import ephem

logging.basicConfig(filename="bot.log", level=logging.INFO, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def greet_user(update, context):
    print("Вызван /start")
    print(update)
    update.message.reply_text("Привет, пользователь!")

def planet(update, context):
    planet_name = update.message.text.split()[1].lower().capitalize()
    try:
        planet = getattr(ephem, planet_name)()
        planet.compute()
        update.message.reply_text(ephem.constellation(planet))
    except AttributeError:
        update.message.reply_text('Введите корректное название планеты на латинице')

def talk_to_me(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)

def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", planet))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))    

    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()
