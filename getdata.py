
import json

day, store, item, fromt, tillt, price = ("Sunday","Mcd","Fish Burger","","",0)
#print(day,end="\n")





def fill_variables():
	global day,store,item,fromt,tillt,price
	day = input("enter the day in full format eg; Sunday,Monday : ")
	store = input("enter the store name - Mcd,Malay,Indian : ")
	item = input("enter the food item - Fish Burger, Mcspicy, Mbreakfast, Nasi Lemak, fried rice, Chicken rice, Paratha, dosa, Chapathi : ")
	fromt = input("enter food item available from time in format : 9am,12pm : ")
	tillt = input("enter food item available till time in format : 9am,12pm : ")
	price = input("enter the price of the food item : ")

def input_to_json():
	file_handle = open ("test.json", mode="r+", encoding="utf-8")
	file = json.load(file_handle)
	#print (file)
	#print (day,store,item,fromt,tillt,price)

	for wday, jstore in file.items():
		if(wday==day):
			print (day,end="\n")
			for keys, info in jstore.items():	
				if(keys==store):
					print(store,end="\n")
					for items, details in info.items():
						if(items==item):
							print(item,file[wday][keys][items])
						else:
							continue
				else:
					continue
		else:
			continue

fill_variables()
	



input_to_json()