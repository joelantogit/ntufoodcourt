import time 
currtime = time.gmtime()
print (time.ctime(time.time()))
print ("year", currtime.tm_year)
print ("month", currtime.tm_mon)
print ("weekday", currtime.tm_wday)

