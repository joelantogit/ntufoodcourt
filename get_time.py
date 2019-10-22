import time 
currtime = time.gmtime()
print (time.ctime(time.time()))
print ("year", currtime.tm_year)
print ("month", currtime.tm_mon)
print ("weekday", currtime.tm_wday)
wday = currtime.tm_wday

weekday = {
			0: 'Monday',
			1: 'Tuesday',
			2: 'Wednesday',
			3: 'Thurday',
			4: 'Friday',
			5: 'Saturday',
			6: 'Sunday'
		  }

for day in weekday:
	if (day == wday):
		print ("day of the week is :", weekday[day])
	else:
		continue