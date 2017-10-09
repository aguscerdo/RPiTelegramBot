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
#   Raspi Functions
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


def deleteShow(bot, update):
    message = stripMessage(update)
    IDPath = folderID(filePath(), update.message.chat_id)
    if os.path.isfile(IDPath + "shows.json"): #If file exists
        shows = json.load(open(IDPath + 'shows.json'))    #Open it
        if message in shows:
            shows.pop(message)
            json.dump(shows, open(IDPath + 'shows.json', 'w'))
            update.message.reply_text("%s succesfully removed." % message)
        else:
            update.message.reply_text("No such name stored.")
    else:   #File doesn't exist, nothing to delete.
        update.message.reply_text("There are no shows stored.")


def timeToShow(bot, update):
    message = stripMessage(update)
    IDPath = folderID(filePath(), update.message.chat_id)
    if os.path.isfile(IDPath + "shows.json"):  # If file exists
        shows = json.load(open(IDPath + 'shows.json'))  # Open it
        STime = ShowTime
        confirmation = STime.loadTimes(shows[message])
        if not confirmation:
            update.message.reply_text(STime.timeDifference())
        else:
            update.message.reply_text('Not such show stored.')
    else:
        update.message.reply_text("There are no shows stored.")


def TTS(bot, update):
    try:
        message = stripMessage(update)
        tts = gtts.gTTS(text=message, lang='en')
        tts.save('/tmp/audio.wav')
        audio = open('/tmp/audio.wav', 'rb')
        update.message.reply_voice(audio)
    except Exception as e:
        print(e)
        update.message.reply_text("Error: %s" % e)


def TTSEs(bot, update):
    try:
        message = stripMessage(update)
        tts = gtts.gTTS(text=message, lang='es')
        tts.save('/tmp/audio.wav')
        audio = open('/tmp/audio.wav', 'rb')
        update.message.reply_voice(audio)
    except Exception as e:
        print(e)
        update.message.reply_text("Error: %s" % e)


# def imageAnalysis(bot, update):
#     try:
#         IDPath = folderID(filePath(), update.message.chat_id)
#         fileID = update.message.photo[-1].file_id
#         file = bot.getFile(fileID)
#         file.download(IDPath + 'EDGERaw.jpg')
#         rawImg = cv2.imread('EDGERaw.jpg',0)
#         grayScale = cv2.cvtColor(rawImg, cv2.COLOR_BGR2GRAY)
#         # gBlur = cv2.GaussianBlur(grayScale, (5,5), 0)
#         edge = cv2.Canny(grayScale, 100, 200)
#         update.message.reply_photo(edge)
#     except Exception as e:
#         print(e)