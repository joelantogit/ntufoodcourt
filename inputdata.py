import json


#day, store, item, fromt, tillt, price = ("Sunday","Mcd","Fish Burger","","",0)
#print(day,end="\n")

# the sequence to input data is first weekday ---> store --> item --> available time --> price 




def user_input(arg): #to ask user and return data to fill in the json

	possible_days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
	items = ["Mcspicy","Fish Burger","McBreakfast"]
	count = 0
	
#to get the weekday
	while (arg == 'day'):
		count = count+1
		try:
			pointer = input("Please enter the day in full format eg; Sunday,Monday or enter 'X' to return :")
			for x in possible_days:
				if (x == pointer ):
					return pointer
				elif (pointer == 'X'):
					return 'exit'
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
	
	item = input("enter the food item - Fish Burger, Mcspicy, Mbreakfast, Nasi Lemak, fried rice, Chicken rice, Paratha, dosa, Chapathi : ")
	fromt = input("enter food item available from time in format : 9am,12pm : ")
	tillt = input("enter food item available till time in format : 9am,12pm : ")
	price = input("enter the price of the food item : ")



def input_to_json():
	#opening file to read
	file_handle = open ("test.json", mode="r", encoding="utf-8")
	file = json.load(file_handle)
	file_handle.close()
	#closed file

	#####declaring variables
	count = 0 #local count to use inside loops
	global stores
	stores = []
	for wday, jstore in file.items():
		for keys, info in jstore.items():
			stores.append(keys)
	print(stores)
	print (file)
	option = {
				1: 'wait_time',
				2: 'working_hrs',
				3: 'item_info'
				}



	global day
	day = user_input('day')
	if (day == 'exit'):
		exit()
	global store
	store = user_input('store')
	if (store =='exit'):
		exit()
	len_of_items = len(file[day]) #to identify if the foor loop is iterated throughthou the avaialable keys


	for wday, jstore in file.items():
		if(wday==day):
			print (day,end="\n")
			for keys, info in jstore.items():
				if(keys==store):
					print(store,end="\n")
				else:
					count = count+1
					continue
			if(count == len_of_items):
				file[wday][store] = {}
				stores.append(store)

		else:
			continue

			
	'''		
	wait_time = user_input('wait_time')
	if(wait_time == 'exit'):
		exit()
	else:
		file[wday][store]["Waiting Time"] = wait_time

			
		try:
			choice = input("Enter      \n1 -  for updating waiting time\n 2 - for updating working hrs \n 3 - for updating item info\n")
			if(choice.isdigit):
				for selection in option:
					if (choice == option):
								user_input(option[selection])
	'''
	#opening file to write
	file_handle = open ("test.json", mode="w", encoding="utf-8")
	json.dump(file, file_handle, indent=4 )
	file_handle.close()
	#closed the file



input_to_json()



