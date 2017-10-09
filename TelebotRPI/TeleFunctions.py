import telegram


def stripMessage(update):
    ret = update.message.text.strip().split(' ', 1)
    if len(ret)> 1:
        return ret[1]
    else:
        return ''