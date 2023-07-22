import time

def IsNeedStartPooling(delayMinutes: int):
    isTimeToPooling = False
    
    timeNow = time.localtime()
    weekNow = timeNow.tm_wday #dia da semana segunda é 0, domingo é 6
    hourNow = timeNow.tm_hour
    minuteNow = timeNow.tm_min

    #resultados PTM e PT
    if (hourNow == 11 or hourNow == 14) and (minuteNow > (25) and minuteNow < (30+delayMinutes)):
        isTimeToPooling = True
    #resultados PTV
    if (hourNow == 16 or hourNow == 21) and weekNow != 6 and (minuteNow > (25) and minuteNow < (30+delayMinutes)):
        isTimeToPooling = True
    #resultados PTN
    if hourNow == 18 and weekNow != 2 and weekNow < 5 and (minuteNow > (25) and minuteNow < (30+delayMinutes)):
        isTimeToPooling = True
    #resultados FED
    if hourNow == 19 and minuteNow > 25 and minuteNow < (30+delayMinutes) and (weekNow == 2 or weekNow == 5):
        isTimeToPooling = True
    
    return isTimeToPooling