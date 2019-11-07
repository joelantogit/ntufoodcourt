#to return available open and closed stores strings from the database from the input data of date and time.

import time  #importing time module.
import json
import datetime
import pprint
pp= pprint.PrettyPrinter(indent = 4) #to print dictionaries with indent not necessary for the program
file_handle = open ("store_item.json", mode="r", encoding="utf-8") #to read in the json file "store_item.json" from the current directory.
store_item = json.load(file_handle)
file_handle.close()
file_handle = open ("storeinfo.json", mode="r", encoding="utf-8") #to read in the json file "store_item.json" from the current directory.
storeinfo = json.load(file_handle)
file_handle.close()



localdate = "04/11/2019" #format of date to be recieved for function w_day
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
						#print (storelist)

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

name_of_the_store = 'Subway'    #test store for the function get menu

def get_menu(name_of_the_store):

	global menu_items_available
	menu_items_available = []
	global menu_items_unavailable
	menu_items_unavailable =[]

	localitems = [] #list to store the buld data  of dictionary at first locally
	for day, stores  in store_item.items():
		if(day == weekday):
			for storename, fooditem in stores.items():
				if (storename == name_of_the_store):
					for fitem, details in fooditem.items():
						localitems.append((fitem,store_item[day][storename][fitem]['from'],store_item[day][storename][fitem]['till'],store_item[day][storename][fitem]['price']))
						#print(store_item[day][storename][fitem]['from'])

	for store,fromtime,tilltime, price in localitems:
		if(len(fromtime) == 3):
			fromtime = "0" + fromtime
		if(len(tilltime)==3):
			tilltime = "0" + tilltime
		upper =  timejsonto24hr(fromtime.lower())
		lower = timejsonto24hr(tilltime.lower())
		#print (upper, lower)
		if(int(upper)<=int(formatted_time)<=int(lower)):
			menu_items_available.append((store,price))
		else:
			menu_items_unavailable.append((store,price))

	#pp.pprint(localitems)
	print(menu_items_available,menu_items_unavailable)

get_menu(name_of_the_store)


def waitingtimecalc(name_of_the_store):
	global waiting_time
	waiting_time = 0

	for store, item in storeinfo.items():
		if(store == name_of_the_store):
			for waitime, others in item.items():
				if (waitime == 'Waiting Time'):
					waiting_time = storeinfo[store][waitime]


waitingtimecalc(name_of_the_store)

print("waiting time for " + name_of_the_store +":" + "{}".format(waiting_time))


def getopenhrs(name_of_the_store):
    global operating_hrs
    operating_hrs= []

    for store, item in storeinfo.items():
        if(store == name_of_the_store):
            for oprhrs, others in item.items():
                if (oprhrs == 'Open hrs'):
               		for day, openhr in others.items():
                   		operating_hrs.append((day,openhr))
                    
getopenhrs(name_of_the_store)


print (operating_hrs)
#print(storelist)



#rint (open_hrs)