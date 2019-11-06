#to return available open and closed stores strings from the database from the input data of date and time.

import time  #importing time module.
import json
import datetime

file_handle = open ("store_item.json", mode="r", encoding="utf-8") #to read in the json file "store_item.json" from the current directory.
store_item = json.load(file_handle)
file_handle.close()
file_handle = open ("storeinfo.json", mode="r", encoding="utf-8") #to read in the json file "store_item.json" from the current directory.
storeinfo = json.load(file_handle)
file_handle.close()



localdate = "08/11/2019" #format of date to be recieved for function w_day
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
	x = datetime.date(year,month,day)
	weekday = x.strftime("%A")
	return (weekday)

def timejsonto24hr(formattedtime): #gets a formatted time like "03PM" then converts it to 24 hr int.
	x = formattedtime[0:2]
	y = formattedtime[2:4]
	z = x+":"+y
	t = time.strptime(z,"%I:%p" )
	return time.strftime("%H", t)



def time24hr(localtime): #the input would the correct format of localtime "15:41 PM" that the module accept and the return would be of format "0341PM" 
	ltime,amorpm = localtime.split(' ')
	t = time.strptime(ltime,"%H:%M" )
	return time.strftime("%I%M%p", t)


#(localdate,localtime) = current_time()
weekday = w_day(localdate)

formatted_time = localtime[0:2]
print ("formatted time is " +formatted_time)
print ("weekday is "+ weekday + "\ntime frame  is " + formatted_time, end ="\n")


#need to check with two files one from the storeinfo.json and also from the store_item.json
def openorclosed(weekday,formatted_time):
	global open_stores 
	open_stores= [] #store a list of open stores for the parameters provided ['Mcd', 'Subway', 'Indian', 'Noodle Shop'] 
	global closed_stores 
	closed_stores= [] #stores a list of closed stores for the parameters provided ['Malay']

	#to check if the variable "weekday" is corresponding to what storeinfo.json
	key = {
				"Sunday": "Sunday",
	            "Saturday":"Saturday",
	            "Monday": "Weekday",
	            "Tuesday": "Weekday",
	            "Wednesday": "Weekday",
	            "Thursday": "Weekday",
	            "Friday": "Friday"
			}

	for items in key:
		if(weekday == items):
			wday_storeinfo = key[weekday]
		else:
			continue
	#print (wday_storeinfo)

	global storelist
	storelist = [] #list of details of open hrs for each outlet #[('Mcd', '09am-09pm'), ('Subway', '09am-11pm'), ('Indian', '08am-09pm'), ('Noodle Shop', '09am-09pm'), ('Malay', '09am-09pm')]
	for store, item in storeinfo.items():
		for openhrs, others in item.items():
			if (openhrs == 'Open hrs'):
				for wday, details in others.items():
					if(wday == wday_storeinfo):
						storelist.append((store,storeinfo[store][openhrs][wday_storeinfo]))

	upper = 0 #variable that carry store close time
	lower = 0 #variable that carry store open time
	for store, opentime in storelist:
		x,y = opentime.split("-")
		lower = timejsonto24hr(x.lower())
		upper = timejsonto24hr(y.lower())
		#print (lower,upper)
		if (int(lower)<=int(formatted_time)<=int(upper)): #checking if the store is open 
			open_stores.append(store)
		else:
			closed_stores.append(store)




openorclosed(weekday,formatted_time)
print (open_stores,closed_stores)

#print(storelist)



#rint (open_hrs)