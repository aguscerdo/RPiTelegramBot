from TeleFunctions import *
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import random
import datetime
import requests
import gtts
import json
import os
# import cv2


"""
#
#   Basic Commands
#
"""


def randList(bot, update):
    message = stripMessage(update)
    if message:
        options = message.split(' ')
        random.seed()
        ret = random.choice(options).replace(',', '')
        update.message.reply_text(ret)
    else:
        update.message.reply_text('Give me something at least')


def randNum(bot, update):
    message = stripMessage(update)
    if message and message.isdigit():
        mx = int(message)
    else:
        mx = 10
    random.seed()
    update.message.reply_text(random.randint(1, mx))


def dice1(bot, update):
    update.message.reply_text(random.randint(1,6))


def dice2(bot, update):
    d1 = random.randint(1,6)
    d2 = random.randint(1,6)
    update.message.reply_text('%d |-| %d --> %d' % (d1, d2, d1+d2))


def flipCoin(bot, update):
    random.seed()
    rt = ''
    h = 0
    t = 0
    while h < 3 and t < 3:
        if random.randint(0, 1):
            h = h + 1
            rt += 'H'
        else:
            t = t + 1
            rt += 'T'
    if (h > t):
        rt += ' -> H'
    else:
        rt += ' -> T'
    update.message.reply_text(rt)


def TTS(bot, update):
    tts = gtts.gTTS(text=stripMessage(update), lang='en')
    update.message.audio(tts)


def TTSEs(bot, update):
    tts = gtts.gTTS(text=stripMessage(update), lang='es')
    update.message.audio(tts)


# def imageAnalysis(bot, update):
#     try:
#         IDPath = folderID(filePath(), update.message.chat_id)
#         fileID = update.message.photo[-1].file_id
#         file = bot.getFile(fileID)
#         file.download(IDPath + 'EDGERaw.jpg')
#         print('Small Tits')
#         rawImg = cv2.imread('EDGERaw.jpg',0)
#         print('Medium Tits')
#         grayScale = cv2.cvtColor(rawImg, cv2.COLOR_BGR2GRAY)
#         print('Big Tits')
#         # gBlur = cv2.GaussianBlur(grayScale, (5,5), 0)
#         edge = cv2.Canny(grayScale, 100, 200)
#         print('Kate Upton')
#         update.message.reply_photo(edge)
#     except Exception as e:
#         print(e)


