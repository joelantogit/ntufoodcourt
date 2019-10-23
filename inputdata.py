import json




def input_to_json():
	file_handle = open ("json.json", "r", encoding="utf-8")
	file = json.load(file_handle)
	print (file)

input_to_json()


