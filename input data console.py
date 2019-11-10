import json
import pprint
pp= pprint.PrettyPrinter(indent = 4)
#day, store, item, fromt, tillt, price = ("Sunday","Mcd","Fish Burger","","",0)
#print(day,end="\n")

# the sequence to input data is first weekday ---> store --> item --> available time --> price 




def user_input(arg): #to ask user and return data to fill in the json

	possible_days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
	count = 0
	
#to get the weekday
	while (arg == 'day'):
		count = count+1
		try:
			pointer = input("Please enter the day in full format eg; Sunday,Monday or enter 'X' to return or N for new day entry :")
			for x in possible_days:
				if (x == pointer ):
					return pointer
				elif (pointer == 'X'):
					return 'exit'
				elif (pointer == 'N'):
					pointer = input("Please enter the name of the new day ")
					stores.append(pointer)
					return pointer
			if(count >2):
				return 'exit'
			else:
			 continue
				
		except:
			continue
#to get store

	while (arg == 'store'):
		count = count +1
		try:
			pointer = input("Please enter the store name - Mcd,Malay,Indian or 'X' to return or N for new entry: ")
			for x in stores:
				if(x == pointer):
					return pointer
				elif (pointer == 'X'):
					return 'exit'
				elif (pointer == 'N'):
					pointer = input("Please enter the name of the new store")
					stores.append(pointer)
					return pointer
			if(count >2):
				return 'exit'
			else:
				continue
		except:
			continue
	while (arg == 'wait_time'):
		count = count +1
		try:
			pointer = input("Please enter the waiting time for store" + store + "or 'X' to return : ")
			if(pointer.isdigit()):
				return pointer
			elif(count >2):
				return 'exit'
			else:
				continue
		except:
			continue
	while(arg == 'food_item'):
		pointer = input("Please enter the food item name - :")
		return pointer
				


	while(arg == 'fromtime'):
		count = count +1
		try:
			pointer = input("Please enter the from time of item 09am,12pm - :")
			x = pointer[0:2]
			z=int(x)
			y = pointer[2:4]
			if x.isdigit() == True:
				if(y=='am' or  y=='pm' and (0<=z<=12) ):
					return pointer
			else:
				print ("Please enter in correct format")
		except:
			continue

	while(arg == 'totime'):
		count = count +1
		try:
			pointer = input("Please enter the to time of item 09am,12pm - :")
			x = pointer[0:2]
			z=int(x)
			y = pointer[2:4]
			if x.isdigit() == True:
				if(y=='am' or  y=='pm' and (0<=z<=12) ):
					return pointer
			else:
				print ("Please enter in correct format")
		except:
			continue
	while(arg == 'price'):
		count = count +1
		try:
			pointer = input("Please enter price  ")
			x,y = pointer.split(".")
			if ((x.isdigit() == True) and (y.isdigit() == True)):
				z= float(pointer)
				return z
			else:
				print ("Please enter price in correct format")
		except:
			continue
	


	fromt = input("enter food item available from time in format : 9am,12pm : ")
	tillt = input("enter food item available till time in format : 9am,12pm : ")
	price = input("enter the price of the food item : ")



def input_to_json():
	#opening file to read
	file_handle = open ("store_item.json", mode="r", encoding="utf-8")
	global file
	file = json.load(file_handle)
	file_handle.close()
	#closed file

	#####declaring variables
	stcount = 1 #local count to use inside loops
	global stores
	global food_items
	food_items = []
	
	stores = []
	for wday, jstore in file.items():
		for keys, info in jstore.items():
			stores.append(keys)
	print(stores)
	pp.pprint(file)
	#option = {
	#			1: 'wait_time',
	#			2: 'working_hrs',
	#			3: 'item_info'
	#			}


	#start input for day
	global day
	day = user_input('day')
	if (day == 'exit'):
		exit()
	global store
	
	 #to identify if the foor loop is iterated throughthou the avaialable keys
	cofday = 1
	lofday = len(file)
	print ("number of days inside json " + "{}".format(lofday), end="\n")
	for wday, jstore in file.items():
		if(wday==day):
			store = user_input('store')
			if (store =='exit'):
				exit()
			len_of_days = (len(file[day]))
			print (day,end="\n")

			for keys, info in jstore.items():
				if(keys==store):
					#print (file[day][store][item])
					#food_items = None
					#item = 'item'
					#food_items = file[day][store][item].keys()							
					#print (food_items)

					#fooditem = user_input('food_item')
					#if (store =='exit'):
					#	exit()
					#lofitem = (len(file[day][keys]["item"]))
					continue
	
				else:
					stcount = stcount+1
					continue

		else:
			cofday=cofday +1
			continue
			
	if (cofday > lofday):
		file[day]={}
		print("new day created " + day, end="\n")
		write_to_file(file)
	pp.pprint(file)
	if(stcount > len_of_days):
		file[day][store] = {}
		stores.append(store)
		write_to_file(file)
	pp.pprint(file)
	#start inputting for fitem
	fooditem = user_input('food_item')
	if (fooditem =='exit'):
		exit()
	fromtime = user_input('fromtime')
	if (fromtime =='exit'):
		exit()
	totime = user_input('totime')
	if (totime =='exit'):
		exit()
	price = user_input('price')

	file[day][store][fooditem] = {}
	file[day][store][fooditem]["from"] = fromtime
	file[day][store][fooditem]["till"] = totime
	file[day][store][fooditem]["price"] = price
	pp.pprint(file)
	write_to_file(file)
	input_to_json()


	

def write_to_file(file):
	file_handle = open ("store_item.json", mode="w", encoding="utf-8")
	json.dump(file, file_handle, indent=4 )
	file_handle.close()
	file_handle = open ("store_item.json", mode="r", encoding="utf-8")
	file = json.load(file_handle)
	file_handle.close()

	#closed the file



input_to_json()



