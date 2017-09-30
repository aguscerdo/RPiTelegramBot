from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.error import NetworkError, Unauthorized
import os
import telegram
import random
from tinydb import TinyDB, Query
from time import sleep
class TeleBot:  #Checks validity of token and chatID
    """
    #
    #   Returners
    #
    """
    def retToken(self):
        return self.token

    def retChatID(self):
        return self.chatID


    def __init__(self):
        self.db = TinyDB("data.json")
        try:
            sett = Query()
            token = self.db.get(sett.name == 'token')
            if token:
                self.token = token['value']
            else:
                self.setToken()
        except Exception as e:
            print(e)
            return

        self.bot = telegram.Bot(self.token)
        try:  # Send a start message to ensure correct work
            self.bot.get_updates(timeout=5)
        except telegram.error.NetworkError or telegram.error.TimedOut:
            print("Connection failed. Retrying...")
            self.reconnect()
        except telegram.error.InvalidToken:
            print("Invalid Token")
            self.setToken()
        except Exception as e:
            print(e)
            print("Something wen wrong. Want to re-obtain token? (y/n)")
            while 1:
                response = str(raw_input())
                if response == 'y':
                    self.setToken()
                    break
                elif response == 'n':
                    print('Exiting program')
                    raise SystemExit
            self.setToken()
        print('Bot object loaded succesfully.')

    def reconnect(self):
        i = 30
        while i:
            try:  # Send a start message to ensure correct work
                self.bot.get_updates(timeout=5)
                return
            except telegram.error.NetworkError or telegram.error.TimedOut:
                print("Connection failed. Retrying... %d" % i)
                i -= 1
                sleep(1)
                continue
            except:
                print("Token is not correct")
                self.setToken()
                return
        print("Connection could not be established. Exiting.")
        raise SystemExit


    def setToken(self):
        self.token = str(input("Enter Telegram bot token: "))
        try:  # Send a start message to ensure correct work
            self.bot = telegram.Bot(self.token)
            self.bot.get_updates(timeout=5)
            Q = Query()
            if self.db.contains(Q.name == 'token'):
                self.db.update({'value':self.token}, Q.name == 'token')
            else:
                self.db.insert({'name':'token', 'value':self.token})
        except telegram.error.NetworkError or telegram.error.TimedOut:
            print("Connection failed. Retrying...")
            self.reconnect()
        except telegram.error.InvalidToken:
            print("Invalid Token")
            self.setToken()
        except Exception as e:
            print('Miscellaneous Error')
            print(e)
            self.setToken()