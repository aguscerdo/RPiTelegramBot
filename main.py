import TeleFunctions
import TeleBotObj
import WeatherConversation
from commands import *

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
from telegram.error import NetworkError, Unauthorized
import random
import ShowsConversation
import tinydb

def test(bot, update):
    print ("I'm an ironman")

def start(bot, update):
    update.message.reply_text("Hello there! I'm a RaspiBot with some functionalities.\n"
                              "My current functions are:\n"
                              "/randlist: choose a random item from a list (a b c d).\n"
                              "/random: random number from 1 to N (default 10).\n"
                              "/coin: flip a coin, first to 3 wins.\n"
                              "Send a LOCATION and I'll tell you the weather.\n")

def main():
    Telebot = TeleBotObj.TeleBot()
    updater = Updater(Telebot.retToken())
    commander = updater.dispatcher

    #Command Handlers
    commander.add_handler(CommandHandler('dice1', dice1))
    commander.add_handler(CommandHandler('dice2', dice2))
    commander.add_handler(CommandHandler('start', start))
    commander.add_handler(CommandHandler('rlist', randList))
    commander.add_handler(CommandHandler('random', randNum))
    commander.add_handler(CommandHandler('coin', flipCoin))
    commander.add_handler(CommandHandler('tts', TTS))
    commander.add_handler(CommandHandler('ttses', TTSEs))
    print('Command Handlers loaded.')

    #Message Handlers
    commander.add_handler(MessageHandler(Filters.location, WeatherConversation.localWeather))
    print('Message Handlers loaded.')

    #Conversation Handlers
    commander.add_handler(WeatherConversation.weatherHandler)
    commander.add_handler(ShowsConversation.showsHandler)
    print('Conversation Handlers loaded.')

    updater.start_polling()
    print('Telegram Bot running.')
    updater.idle()

#Main routine
main()