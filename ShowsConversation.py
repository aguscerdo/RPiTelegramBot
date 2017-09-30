from TeleFunctions import *
from ShowTimeObj import *
import requests
from tinydb import TinyDB, Query
from telegram.ext import Handler, CommandHandler, MessageHandler, CallbackQueryHandler, RegexHandler, ConversationHandler, Filters
import telegram


CHOOSING, ADD, REMOVE, SELECT = range(4)

def test(bot, update):
    print("I'm an ironman")
    return ConversationHandler.END


def startShows(bot, update):
    keyboard = [[telegram.KeyboardButton('Shows')],
                [telegram.KeyboardButton('Add'),
                 telegram.KeyboardButton('Remove'),
                 telegram.KeyboardButton('Cancel')]]
    markup = telegram.ReplyKeyboardMarkup(keyboard)

    update.message.reply_text('Choose an option:\n'
                              'Shows: Returns time left for a show.\n'
                              'Add: Add or Update a show.\n'
                              'Remove: Remove a show.',
                              reply_markup=markup)
    return CHOOSING


def cancelShows(bot, update):
    update.message.reply_text('Shows call cancelled.',
                              reply_markup=telegram.ReplyKeyboardRemove())
    return ConversationHandler.END


def requestAddShow(bot, update):
    update.message.reply_text('Enter a show name and time.\n'
                              '[Name] [HH]:[MM] [Day of Week]\n'
                              'Press /cancel to, well, cancel.',
                              reply_markup=telegram.ReplyKeyboardRemove())
    return ADD

def addShow(bot, update):    #Replaces/adds shows to the file
    message = update.message.text.strip()
    db = TinyDB('data.json')
    Q = Query()
    try:
        show = ShowTime()
        incorrectTime = show.parseMessage(message)  #Load message into the object
        if incorrectTime:
            update.message.reply_text('Incorrect format: %s' % incorrectTime)
            return ConversationHandler.END

        table = db.table(str(update.message.chat_id))
        showName = show.returnName()

        if table.contains(Q.name == showName):   #Update
            table.update({'time': show.returnTimeList()}, Q.name == showName)
            update.message.reply_text('Updated %s in your show list.' % showName)
        else:#Add New
            table.insert({'name':showName, 'time':show.returnTimeList()})
            update.message.reply_text('Added %s to your show list.' % showName)
        
        return ConversationHandler.END

    except Exception as e:
        print("Error: %s" % e)
        update.message.reply_text('Error: %s' % e)
        return ConversationHandler.END

def retCurrentShows(ID, perRow = 3):
    db = TinyDB('data.json')
    showTable = db.table(str(ID))
    allShows  = showTable.all()
    if not allShows:
        
        return 0

    listOfShows = []
    listOfNames = ''
    i = 0
    for show in allShows:
        if not i % perRow:
            listOfShows.append([])
        listOfShows[int(i/perRow)].append(telegram.KeyboardButton(show['name']))
        listOfNames += show['name'] + '\n'
        i += 1
    listOfShows.append([telegram.KeyboardButton('Cancel')])
    # 
    return [listOfShows, listOfNames]


def requestRemoveShow(bot, update):
    try:
        allShows = retCurrentShows(str(update.message.chat_id))
        if not allShows: #Empty, end immediately
            update.message.reply_text("There are no shows stored.", reply_markup=telegram.ReplyKeyboardRemove())
            return ConversationHandler.END
        update.message.reply_text('Choose a show to delete:', reply_markup=telegram.ReplyKeyboardMarkup(allShows[0]))
        return REMOVE
    except Exception as e:
        print("Error: %s" % e)
        update.message.reply_text('Error: %s' % e)
        return ConversationHandler.END


def removeShow(bot, update):
    db = TinyDB('data.json')
    table = db.table(str(update.message.chat_id))
    Q = Query()
    try:
        table.remove(Q.name == update.message.text)
        update.message.reply_text('"%s" has been removed.' % update.message.text, reply_markup=telegram.ReplyKeyboardRemove())
        
        return ConversationHandler.END
    except Exception as e:
        print('Error: %s' % e)
        update.message.reply_text("Can't delete what does not exist, but OK...", reply_markup=telegram.ReplyKeyboardRemove())
        
        return ConversationHandler.END


def requestSelectShow(bot, update):
    try:
        allShows = retCurrentShows(str(update.message.chat_id))
        if not allShows:
            update.message.reply_text('There are no shows stored.', reply_markup=telegram.ReplyKeyboardRemove())
            return ConversationHandler.END
        update.message.reply_text('Select a show:', reply_markup=telegram.ReplyKeyboardMarkup(allShows[0]))
        return SELECT
    except Exception as e:
        print("Error: %s" % e)
        update.message.reply_text('Error: %s' % e, reply_markup=telegram.ReplyKeyboardRemove())
        return ConversationHandler.END


def selectShow(bot, update):
    db = TinyDB('data.json')
    table = db.table(str(update.message.chat_id))
    Q = Query()
    try:
        show = table.get(Q.name == update.message.text)
        timeTuple = show['time']
        showTime = ShowTime()
        errorLoadingTimes = showTime.loadTimes(timeTuple)
        if  errorLoadingTimes:
            update.message.reply_text('Times do not work out. Error: %s \n'
                                      'Remove %s from show list.' % (goodLoadTime, update.message.text),
                                      reply_markup=telegram.ReplyKeyboardRemove())
            
            return ConversationHandler.END

        timeDiff = showTime.timeDifference()
        update.message.reply_text(timeDiff, reply_markup=telegram.ReplyKeyboardRemove())
        return ConversationHandler.END

    except Exception as e:
        update.message.reply_text('Error: %s' % e, reply_markup=telegram.ReplyKeyboardRemove())
        return ConversationHandler.END



showsHandler = ConversationHandler(
    entry_points=[CommandHandler('shows', startShows)],
    states={
        CHOOSING: [RegexHandler('^(Shows)$', requestSelectShow),
                   RegexHandler('^(Add)$', requestAddShow),
                   RegexHandler('^(Remove)$', requestRemoveShow),
                   RegexHandler('^(Cancel)$', cancelShows)],
        ADD: [MessageHandler(Filters.text, addShow),
              CommandHandler('cancel', cancelShows)],
        REMOVE: [MessageHandler(Filters.text, removeShow),
                 RegexHandler('^(Cancel)', cancelShows)],
        SELECT: [MessageHandler(Filters.text, selectShow),
                 RegexHandler('^(Cancel)$', cancelShows)]
    },
    fallbacks=[Handler(cancelShows)],
    allow_reentry=True)