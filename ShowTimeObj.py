import datetime


class ShowTime: #Transforms a string of time-day
    def parseMessage(self, message):
        try:
            spaced = message.replace(':', ' ').replace('-', ' ')
            block = spaced.split(' ')  #Split message into [name] [hour] [minute] [day]
            hour = int(block[1])
            minute = int(block[2])
            if  0 <= hour < 24:
                self.hour = hour
            else:
                return "Invalid Hour"
            if 0 <= minute < 60:
                self.minute = minute
            else:
                return "Invalid Minute"
            block[3] = self.dayToInt(block[3])
            if block[3]:
                self.day = block[3]
            else:
                return 'Invalid Day'
            self.name = block[0]
            return 0    #Succesfully read
        except Exception as e:
            return "Error: %s" % e


    def returnTimeList(self):
        return [self.hour, self.minute, self.day]


    def loadTimes(self, timeList):
        if  0 <= timeList[0] < 24:
            self.hour = timeList[0]
        else:
            return "Invalid Hour"
        if 0 <= timeList[1] < 60:
            self.minute = timeList[1]
        else:
            return "Invalid Minute"
        if 1 <= timeList[2] <= 7:
            self.day = timeList[2]
        else:
            return 'Invalid Day'
        return 0    #Succesfully read

    def returnName(self):
        return self.name

    def dateToString(self):
        ret = str(self.hour) + ':'
        if self.minute < 10:
            ret += '0'
        ret += str(self.minute) + ' ' + self.day
        return ret

    def timeDifference(self):
        now = datetime.datetime.now()  # Get current time
        current = datetime.datetime.timetuple(now)
        cDay = datetime.datetime.isoweekday(now)
        weekday = self.day
        dMin = self.minute - current[4]  # Calculate time difference
        if dMin < 0:
            dMin += 60
            self.hour -= 1
        dHour = self.hour - current[3]
        if dHour < 0:
            dHour += 24
            weekday -= 1
        dDay = weekday - cDay
        if dDay < 0:
            dDay += 7

        ret = str(dDay) + ' day'  # Format string, differentiating between ones and multis
        if dDay != 1:
            ret += 's'
        ret += ', '
        ret += str(dHour) + ' hour'
        if dHour != 1:
            ret += 's'
        ret += ' and '
        ret += str(dMin) + ' minute'
        if dMin != 1:
            ret += 's'
        ret += ' remaining'
        return ret

    @staticmethod   #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!FIX
    def dayToInt(s):
        weekday = s.lower()
        if weekday == 'friday':
            weekday = 5
        elif weekday == 'saturday':
            weekday = 6
        elif weekday == 'sunday':
            weekday = 7
        elif weekday == 'monday':
            weekday = 1
        elif weekday == 'tuesday':
            weekday = 2
        elif weekday == 'wednesday':
            weekday = 3
        elif weekday == 'thursday':
            weekday = 4
        else:
            weekday = 0
        return weekday

    @staticmethod
    def intToDay(s):
        if 0 < int(s) <= 7:
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            return days[int(s)]
        return 0