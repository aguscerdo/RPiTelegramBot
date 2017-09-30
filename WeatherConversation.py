from TeleFunctions import *
import requests
from tinydb import TinyDB, Query
from telegram.ext import Handler, CommandHandler, MessageHandler, CallbackQueryHandler, RegexHandler, ConversationHandler, Filters
import telegram


CHOOSING, CITY, API = range(3)

def retrieveAPIKey():
    try:
        db = TinyDB('data.json')
        Q = Query()
        key = db.get(Q.name == 'weather')
        if key:

            return key['value']
        else:
            return 0
    except Exception as e:
        print(e)
        return 0


def requestAPI(bot, update):
    update.message.reply_text("Enter WUnderground API:\n"
                              "Send /cancel to cancel change.",
                              reply_markup=telegram.ReplyKeyboardRemove())
    return API


def setAPIKey(bot, update):
    message = update.message.text.strip()
    if message.lower() == '/cancel':
        update.message.reply_text('API change cancelled.', reply_markup=telegram.ReplyKeyboardRemove())
        return ConversationHandler.END
    db = TinyDB('data.json')
    Q = Query()
    try:
        if db.contains(Q.name == 'weather'):
            db.update({'value': message}, Q.name == 'weather')
        else:
            db.insert({'name': 'weather', 'value':message})
        update.message.reply_text('API key updated to %s' % message)
        return ConversationHandler.END

    except Exception as e:
        print(e)
        update.message.reply_text('Error: %s' % e)
        return ConversationHandler.END



def localWeather(bot, update):
    key = retrieveAPIKey()
    if not key:
        update.message.reply_text("There is no WUnderground API Key.\n"
                                  "The WUnderground API key can be changed in /weather 'Settings'",
                                  reply_markup=telegram.ReplyKeyboardRemove())
        return ConversationHandler.END

    latitude = update.message.location.latitude
    longitude = update.message.location.longitude
    urlForecast = "http://api.wunderground.com/api/%s/conditions/forecast/q/%f,%f.json" % (key, latitude, longitude)
    urlWeather = "http://api.wunderground.com/api/%s/conditions/geolookup/conditions/q/%f,%f.json" % (key, latitude, longitude)
    try:
        forecast = requests.get(urlForecast).json()['forecast']['simpleforecast']['forecastday'][0]
        weather = requests.get(urlWeather).json()
    except Exception as e:
        update.message.reply_text('Error: %s' % e)
        update.message.reply_text("Unable to obtain weather conditions.\n"
                                  "The WUnderground API key can be changed in /weather 'API' ", reply_markup=telegram.ReplyKeyboardRemove())
        return ConversationHandler.END

    currentTemp = weather['current_observation']['temp_c']
    dayForecast = [forecast['conditions'], forecast['high']['celsius'], forecast['low']['celsius'], forecast['pop']]    #Max, Min, Conditions, Rain % prob

    response = "Weather\n%s\nTemperature: %d C\nMax: %d C\nMin: %d C" % \
               (dayForecast[0], int(currentTemp), int(dayForecast[1]), int(dayForecast[2]))
    if dayForecast[3] > 25:
        response += '\n%d% chance of rain' % int(dayForecast[3])


    update.message.reply_text(response, reply_markup=telegram.ReplyKeyboardRemove())
    return ConversationHandler.END


def requestCity(bot, update):
    update.message.reply_text('Send the city and country/state.\n'
                              '[city], [country]',
                              reply_markup=telegram.ReplyKeyboardRemove())
    return CITY

def cityWeather(bot, update):
    try:
        key = retrieveAPIKey()
        if not key:
            update.message.reply_text("There is no WUnderground API Key.\n"
                                      "The WUnderground API key can be changed in /weather 'Settings'")
            return ConversationHandler.END

        message = update.message.text.strip()
        message = message.split(', ')
        try:
            city = message[0].replace(' ', '_')
            country = message[1].replace(' ', '_')
        except:
            update.message.reply_text("Format must be [city], [contry/state]")
            return ConversationHandler.END

        urlForecast = "http://api.wunderground.com/api/%s/forecast/q/%s/%s.json" % (key, country, city)
        urlWeater = "http://api.wunderground.com/api/%s/conditions/q/%s/%s.json" % (key, country, city)

        try:
            forecast = requests.get(urlForecast).json()['forecast']['simpleforecast']['forecastday'][0]
            weather = requests.get(urlWeater).json()
        except Exception as e:
            print(e)
            update.message.reply_text("Unable to obtain weather conditions.\n"
                                      "The WUnderground API key can be changed in /weather 'API' ")
            return ConversationHandler.END

        currentTemp = weather['current_observation']['temp_c']
        dayForecast = [forecast['conditions'], forecast['high']['celsius'], forecast['low']['celsius'],
                       forecast['pop']]  # Max, Min, Conditions, Rain % prob

        response = "Weather\n%s\nTemperature: %d C\nMax: %d C\nMin: %d C" % (
            dayForecast[0], int(currentTemp), int(dayForecast[1]), int(dayForecast[2]))
        if dayForecast[3] > 25:
            response += '\n%d% chance of rain' % int(dayForecast[3])

        try:
            update.message.reply_text(response, reply_markup=telegram.ReplyKeyboardRemove())
        except:
            update.message.reply_text(response)
        return ConversationHandler.END
    except Exception as e:
        print(e)



def cancelWeather(bot, update):
    update.message.reply_text('Weather call canceled.',reply_markup=telegram.ReplyKeyboardRemove())
    return ConversationHandler.END

def startWeather(bot, update):
    try:
        keyboard = [[telegram.KeyboardButton('Location', request_location=True)],
                    [telegram.KeyboardButton('Enter City'),
                    telegram.KeyboardButton('API'),
                    telegram.KeyboardButton('Cancel')]]
        markup = telegram.ReplyKeyboardMarkup(keyboard)

        update.message.reply_text("Choose an option:\n"
                                  "Location: Weather based on current location.\n"
                                  "Enter City: Selected city's weather.\n"
                                  "API: Enter WUnderground API key or default city.",
                                  reply_markup=markup)
    except Exception as e:
        print(e)

    return CHOOSING

def test(bot, update):
    print("I'm an ironman")
    return ConversationHandler.END


weatherHandler = ConversationHandler(
    entry_points=[CommandHandler('weather', startWeather)],
    states={
        CHOOSING: [RegexHandler('^(Location)$', localWeather),
                   RegexHandler('^(Enter City)$', requestCity),
                   RegexHandler('^(API)$', requestAPI),
                   RegexHandler('^(Cancel)$', cancelWeather)],
        CITY: [MessageHandler(Filters.text, cityWeather)],
        API: [MessageHandler(Filters.text | Filters.command, setAPIKey)]
    },
    fallbacks=[Handler(cancelWeather)],
    allow_reentry=True)