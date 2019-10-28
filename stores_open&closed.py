#to return available open and closed stores strings from the database from the input data of date and time.

import time  #importing time module.

localdate = "28/10/2019" #format of date to be recieved for function w_day
localtime = "15:41 PM"  #format of time to be recieved for function w_day


def current_time(): #to get the current date and time as strings in the format 28/10/2019 and 15:41 PM
	currtime = time.localtime()
	#print (currtime)
	global localdate 
	localdate = time.strftime("%d/%m/%Y",time.localtime()) # formatting time struct using builtin function strftime - %(str(currtime.tm_mday) + "/" + str(currtime.tm_mon) + "/" + str(currtime.tm_year)) 
	global localtime 
	localtime = time.strftime("%H:%M %p",time.localtime()) # formatting time struct using builtin function strftime - (str(currtime.tm_hour) + ":" + str(currtime.tm_min))
	return (localdate,localtime)

def w_day(localdate): #function to get the week of the day
	#print (localdate)
	day, month, year = (int(x) for x in localdate.split('/'))
	w_day = (year,month,day,0,0,0,0,0,0)
	weekday = time.strftime("%A", w_day)
	return (weekday)


#(localdate,localtime) = current_time()
weekday = w_day(localdate)

print (localdate,localtime,weekday)