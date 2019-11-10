import tkinter as tk
from tkinter import messagebox
import time
import datetime
from tkcalendar import Calendar
import json
from functools import partial
import pprint


pp= pprint.PrettyPrinter(indent = 4) #to print dictionaries with indent not necessary for the program
file_handle = open ("store_item.json", mode="r", encoding="utf-8") #to read in the json file "store_item.json" from the current directory.
store_item = json.load(file_handle)
file_handle.close()
file_handle = open ("storeinfo.json", mode="r", encoding="utf-8") #to read in the json file "store_item.json" from the current directory.
storeinfo = json.load(file_handle)
file_handle.close()

global waiting_time

localdate = "08/11/2019" #format of date to be recieved for function w_day
localtime = "15:41 PM"  #format of time to be recieved for function w_day

#BY JOEL
def current_time(): #to get the current date and time as strings in the format 28/10/2019 and 15:41 PM
    currtime = time.localtime()
    #print (currtime)
    global localdate 
    localdate = time.strftime("%d/%m/%Y",time.localtime()) # formatting time struct using builtin function strftime - %(str(currtime.tm_mday) + "/" + str(currtime.tm_mon) + "/" + str(currtime.tm_year)) 
    global localtime 
    localtime = time.strftime("%H:%M %p",time.localtime()) # formatting time struct using builtin function strftime - (str(currtime.tm_hour) + ":" + str(currtime.tm_min))
    return (localdate,localtime)
#BY JOEL
def w_day(localdate): #function to get the week of the day
    #print(localdate)
    day, month, year = (int(x) for x in localdate.split('/'))
    x = datetime.date(year,month,day)
    weekday = x.strftime("%A")
    return (weekday)
#BY JOEL
def timejsonto24hr(formattedtime): #gets a formatted time like "03PM" then converts it to 24 hr int.
    x = formattedtime[0:2]
    y = formattedtime[2:4]
    z = x+":"+y
    t = time.strptime(z,"%I:%p" )
    return time.strftime("%H", t)


#BY JOEL
def time24hr(localtime): #the input would the correct format of localtime "15:41 PM" that the module accept and the return would be of format "0341PM" 
    ltime,amorpm = localtime.split(' ')
    t = time.strptime(ltime,"%H:%M" )
    return time.strftime("%I%M%p", t)

#global date_time_selected

#localdate,localtime = current_time()
#weekday = w_day(localdate)

formatted_time = localtime[0:2]
#print ("formatted time is " +formatted_time)
#print ("weekday is "+ weekday + "\ntime frame  is " + formatted_time, end ="\n")

#BY JOEL
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




#openorclosed(weekday,formatted_time)
#print (open_stores,closed_stores)

#name_of_the_store = 'Malay'    #test store for the function get menu
#BYJOEL
def get_menu(name_of_the_store):

    global menu_items_available
    menu_items_available = []
    global menu_items_unavailable
    menu_items_unavailable =[]
    global weekday 
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

#get_menu(name_of_the_store)
 

#BY JOEL
def waitingtimecalc(name_of_the_store):
    global waiting_time
    waiting_time = 0

    for store, item in storeinfo.items():
        if(store == name_of_the_store):
            for waitime, others in item.items():
                if (waitime == 'Waiting Time'):
                    waiting_time = storeinfo[store][waitime]
#waitingtimecalc(name_of_the_store)
#print("waiting time for " + name_of_the_store + ":" + "{}".format(waiting_time))

#BY JOEL
def getopenhrs(name_of_the_store):
    global operating_hrs
    operating_hrs= []

    for store, item in storeinfo.items():
        if(store == name_of_the_store):
            for oprhrs, others in item.items():
                if (oprhrs == 'Open hrs'):
                    for day, openhr in others.items():
                        operating_hrs.append((day,openhr))


LARGE_FONT = ("Verdana", 15)
MEDIUM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 7)


date_time_selected = ""
restaurant_selected = ""

class Guiinterface(tk.Tk):
#Done by Jianhong 
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
    
        self.title("Menu Inteface")
        self.resizable(1, 1)
        self.container = tk.Frame(self)
        self.geometry("350x350")
        self.maxsize(350, 350)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree, menuPage, laterPage):
            frame = F(self.container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def show_menu_frame(self, cont):
        # global restaurant_selected
        # restaurant_selected = restaurant

        frame = menuPage(self.container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
    def show_later_frame(self, cont):
        # global restaurant_selected
        # restaurant_selected = restaurant

        frame = laterPage(self.container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def show_later_menu_frame(self, cont):
        # global restaurant_selected
        # restaurant_selected = restaurant

        frame = laterMenuFrame(self.container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
class StartPage(tk.Frame):
    """ First Page to Be shown"""
    #Done By Jianhong 

    def __init__(self, parent, controller):
        global localdate
        global localtime
        global weekday
        localdate,localtime = current_time()
        weekday = w_day(localdate)
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Welcome to \n Northspine FoodCourt \n Menu System", bg="yellow", font=LARGE_FONT)
        label.pack(pady=10, padx=10, fill="x")
        button = tk.Button(self, text="Today's Store",
                           command=lambda: controller.show_frame(PageOne))
        button.pack(fill="both", expand=1)
        button2 = tk.Button(self,
                            text="View Later Time",
                            command=lambda: controller.show_frame(PageTwo)).pack(fill="both", expand=1)
        button3 = tk.Button(self,
                            text="Quit",
                            command=lambda: controller.destroy()).pack(fill="x")


class PageOne(tk.Frame):
    """Today's Store page"""
    #Done By Jianhong and joel

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global date_time_selected
        #time1 = ''
        #clock = tk.Label(self, font=('times', 20, 'bold'), bg='green')
        #clock.pack(fill="both", expand=0)

        ''''def tick():
            # get the current local time from the PC
            time2 = time.strftime('%H:%M:%S')
            # if time string has changed, update it
            clock.config(text=time2)
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
            clock.after(200, tick)
        tick()'''

        label = tk.Label(self, text="Today's Store", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        def testing(restaurant):
            global restaurant_selected
            restaurant_selected = restaurant
            print('restaurant selected',restaurant_selected)
            controller.show_menu_frame(menuPage)

        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.config(height=1, width=18)
        button1.place(x=5,y=310)
        button2 = tk.Button(self, text="Quit",
                            command=lambda: controller.destroy())
        button2.config(height=1, width=16)
        button2.place(x=190,y=310)
        date_time_selected = datetime.datetime.now()
        global localdate
        global localtime

        localdate,localtime = current_time()
        
        weekday = w_day(localdate)

        formatted_time = localtime[0:2]

        openorclosed(weekday,formatted_time)
    #BY JOEL
        def printstore(intx):
            if(intx == 0):
                
                store1 = tk.Button(self, text=open_stores[0], command= partial(testing, restaurant=open_stores[0]))
                store1.config(height=2, width=36)
                store1.place(x=20, y=50)
            elif(intx == 1):
                store2 = tk.Button(self, text=open_stores[1], command=partial(testing, restaurant=open_stores[1]))
                store2.config(height=2, width=36)
                store2.place(x=20, y=100)
            elif(intx == 2):
                store3 = tk.Button(self, text=open_stores[2], command=partial(testing, restaurant=open_stores[2]))
                store3.config(height=2, width=36)
                store3.place(x=20, y=150)
            elif(intx == 3):
                store4 = tk.Button(self, text=open_stores[3], command=partial(testing, restaurant=open_stores[3]))
                store4.config(height=2, width=36)
                store4.place(x=20, y=200)
            elif(intx == 4):
                store5 = tk.Button(self, text=open_stores[4], command=partial(testing, restaurant=open_stores[4]))
                store5.config(height=2, width=36)
                store5.place(x=20, y=250)
        
        for intx, items in enumerate(open_stores):
                    if (items != None):
                        printstore(intx)

class laterPage(tk.Frame):
    """View Later Store page"""
    #Done by Jianhong and joel

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global date_time_selected  
        #date_time_selected = datetime.datetime.now()  #2019-11-07 00:00:00 format hh:mm:ss
        date_timestr = str(date_time_selected)
        print ("date time value inside laterpage" + date_timestr)
        a,b = date_timestr.split(" ")
        y,m,d = a.split("-")
        global localdate
        global localtime
        localdate = d + "/" + m + "/" + y
        hr,mi,se = b.split(":")
        localtime = hr + ":" + mi + ":00"
        print("local time inside later page " + localtime  +"\n" + "localdate inside later page "+ localdate )
        

        # print('later page', date_time_selected)current_time()
        
        
        #clock = tk.Label(self, font=('times', 20, 'bold'), bg='green')
        #clock.pack(fill="both", expand=0)

        #clock.config(text = date_time_selected)

        label = tk.Label(self, text="Stores available", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.config(height=1, width=18)
        button1.place(x=5,y=310)
        button2 = tk.Button(self, text="Quit",
                            command=lambda: controller.destroy())
        button2.config(height=1, width=16)
        button2.place(x=190,y=310)
        #date_time_selected = datetime.datetime.now()
        
        def testing(restaurant):
            global restaurant_selected
            restaurant_selected = restaurant
            print('restaurant selected',restaurant_selected)
            controller.show_later_menu_frame(laterMenuFrame)
        
        weekday = w_day(localdate)
        formatted_time = localtime[0:2]
        print("weekday inside later page " + weekday  +"\n" + "formatted time inside later page "+ formatted_time)
        openorclosed(weekday,formatted_time)
#BY JOEL
        def printstore(intx):
            if(intx == 0):
                
                store1 = tk.Button(self, text=open_stores[0], command= partial(testing, restaurant=open_stores[0]))
                store1.config(height=2, width=36)
                store1.place(x=20, y=50)
            elif(intx == 1):
                store2 = tk.Button(self, text=open_stores[1], command=partial(testing, restaurant=open_stores[1]))
                store2.config(height=2, width=36)
                store2.place(x=20, y=100)
            elif(intx == 2):
                store3 = tk.Button(self, text=open_stores[2], command=partial(testing, restaurant=open_stores[2]))
                store3.config(height=2, width=36)
                store3.place(x=20, y=150)
            elif(intx == 3):
                store4 = tk.Button(self, text=open_stores[3], command=partial(testing, restaurant=open_stores[3]))
                store4.config(height=2, width=36)
                store4.place(x=20, y=200)
            elif(intx == 4):
                store5 = tk.Button(self, text=open_stores[4], command=partial(testing, restaurant=open_stores[4]))
                store5.config(height=2, width=36)
                store5.place(x=20, y=250)
        
        for intx, items in enumerate(open_stores):
                    if (items != None):
                        printstore(intx)

class menuPage(tk.Frame):
    #Done By Jianhong and joel
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global restaurant_selected
        print ("global restaurant_selected " + restaurant_selected)
        get_menu(restaurant_selected)  #menu_items_available will hold the menu info
        waitingtimecalc(restaurant_selected)

        global waiting_time
        global menu_items_available
        local_menu = str(menu_items_available)
        print ("menu item available  " + local_menu)
        global waiting_e
                    #[('Fish Burger', 2.5), ('Mcspicy', 5.5), ('McChicken', 3.5), ('Nuggets', 3.5)] [('Mbrkfast', 3)]
        menu_str = """             Menu : %s              \n\n""" %(restaurant_selected)
        
        #to save menu item to string menu_str 
        for items, price in menu_items_available:
            item_str = """    %s.       %s$\n""" % (items, price )
            menu_str+=item_str

        waiting_e = tk.Entry(self, width=10)
        class popupWindow(object):
            def __init__(self):
                top = self.top = tk.Toplevel()
                self.l = tk.Label(top, text="Enter Number of People in Queue")
                self.l.pack()
                self.ent = tk.Entry(top)
                self.ent.pack()
                self.b = tk.Button(top, text='Ok', command=self.cleanup)
                self.b.pack()

            def cleanup(self):
                try:
                    global waiting_time
                    global waiting_e
                    waiting_time = waiting_time * int(self.ent.get())
                    waiting_e.insert(0, waiting_time)
                    waiting_e.config(state='disabled', font=SMALL_FONT)
                    waiting_e.place(x=180, y=35)
                except Exception as e:
                    print(e)
                finally:
                    self.value = self.ent.get()
                    self.top.destroy()
        
        #getting the oper hrs data into str operating menu
        
        def operating_windows():
            global restaurant_selected
            global operating_hrs
            getopenhrs(restaurant_selected)
            operating_menu = ""
            for day, openhrs in operating_hrs:
                item_str = """   %s : %s \n""" %(day, openhrs)
                operating_menu += item_str
            messagebox.showinfo("Operating Hours", operating_menu)

        waiting_time_btn = tk.Button(self, text="Select People in Queue", command=popupWindow).place(x=5,y=0)
        wait_label = tk.Label(self, text="Waiting Time: ", font=MEDIUM_FONT)
        wait_label.place(x=80,y=35)

        operating_time_btn = tk.Button(self, text="Operating Time", command=operating_windows).place(x=200,y=0)
        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage)).pack(side="bottom")
        button2 = tk.Button(self, text="Back to Restaurants",
                            command=lambda: controller.show_frame(laterPage)).pack(side="bottom")

        #the label that contains the title and menu info:
        title_label = tk.Label(self, text=menu_str, font=LARGE_FONT)
        title_label.place(x=0, y=80)

class laterMenuFrame(tk.Frame):
    #Done by Jianhong and joel
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global restaurant_selected
        print ("global restaurant_selected " + restaurant_selected)
        get_menu(restaurant_selected)  #menu_items_available will hold the menu info
        waitingtimecalc(restaurant_selected)

        global waiting_time
        global menu_items_available
        local_menu = str(menu_items_available)
        print ("menu item available  " + local_menu)
        global waiting_e
                    #[('Fish Burger', 2.5), ('Mcspicy', 5.5), ('McChicken', 3.5), ('Nuggets', 3.5)] [('Mbrkfast', 3)]
        menu_str = """              Menu:%s               \n\n""" %(restaurant_selected)
        

        #to save menu item to string menu_str 
        
        for items, price in menu_items_available:
            item_str = """    %s.       %s$\n""" % (items, price )
            menu_str+=item_str

        waiting_e = tk.Entry(self, width=10)
        class popupWindow(object):
            def __init__(self):
                top = self.top = tk.Toplevel()
                self.l = tk.Label(top, text="Enter Number of People in Queue")
                self.l.pack()
                self.ent = tk.Entry(top)
                self.ent.pack()
                self.b = tk.Button(top, text='Ok', command=self.cleanup)
                self.b.pack()

            def cleanup(self):
                try:
                    global waiting_time
                    global waiting_e
                    waiting_time = waiting_time * int(self.ent.get())
                    waiting_e.insert(0, waiting_time)
                    waiting_e.config(state='disabled', font=SMALL_FONT)
                    waiting_e.place(x=180, y=35)
                except Exception as e:
                    print(e)
                finally:
                    self.value = self.ent.get()
                    self.top.destroy()
        
        #getting the oper hrs data into str operating menu
        
        def operating_windows():
            global restaurant_selected
            global operating_hrs
            getopenhrs(restaurant_selected)
            operating_menu = ""
            for day, openhrs in operating_hrs:
                item_str = """   %s : %s \n""" %(day, openhrs)
                operating_menu += item_str
            messagebox.showinfo("Operating Hours", operating_menu) #pulling data from json to display the operating hours

        waiting_time_btn = tk.Button(self, text="Select People in Queue", command=popupWindow).place(x=5,y=0)
        wait_label = tk.Label(self, text="Waiting Time: ", font=MEDIUM_FONT)
        wait_label.place(x=80,y=35)

        operating_time_btn = tk.Button(self, text="Operating Time", command=operating_windows).place(x=200,y=0)
        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage)).pack(side="bottom")
        button2 = tk.Button(self, text="Back to Restaurants",
                            command=lambda: controller.show_later_frame(laterPage)).pack(side="bottom")

        #the label that contains the title and menu info:
        title_label = tk.Label(self, text=menu_str, font=LARGE_FONT)
        title_label.place(x=0, y=80)
        

class PageTwo(tk.Frame):
#Done by Jianhong and joel
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Select a date: ", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        global date_time_selected
        global datevar
        def date_picker():
            global datevar
            def print_sel():
                global date_time_selected
                global datevar
                print(cal.selection_get())
                datevar = str(cal.selection_get())
                top.destroy()
                print ("the  value of date time selected inside the print sel is \n\n\n" + datevar)
                # cal.see(datetime.date(year=2016, month=2, day=5))


            top = tk.Toplevel(self)

            cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                             disabledforeground='red',
                           cursor="hand1", year=2019, month=11, day=7)
            cal.pack(fill="both", expand=True)
            tk.Button(top, text="ok", command=print_sel).pack()
            # return cal.selection_get()

        button3 = tk.Button(self, text="Select Date",
                            command=date_picker).pack()

        label_time = tk.Label(self, text="Select Time: ", font=LARGE_FONT)
        label_time.place(x=130, y=100)
        
        data = range(0,24)
        var = tk.StringVar()
        var.set(data[0])
        p = tk.OptionMenu(self, var, *data)
        # p.grid(row=1, column=0)
        p.place(x=120, y=175)
        label_col = tk.Label(self, text=" : ", font=LARGE_FONT)
        label_col.place(x=175, y=175)
        data_1 = range(0,60)
        var_1 = tk.StringVar()
        var_1.set(data_1[0])
        p_1 = tk.OptionMenu(self, var_1, *data_1)
        p_1.place(x=200, y=175) 
        def confirm():
            
            global date_time_selected
            hours = var.get()
            minutes = var_1.get()
            if len(hours) <2:
                hours = "0"+hours
            if len(minutes) <2:
                minutes = "0"+minutes
             #   date = date_time_selected.strftime("%m/%d/%Y")
            date_time_selected = datevar + " " + hours+":"+minutes+":00"
            print ("the date time values inside page two is : \n\n\n\n\n" + date_time_selected)
             
            controller.show_later_frame(laterPage)
               
        
        button_select_time = tk.Button(self, text="Confirm", command=confirm).place(x=130, y=230)


        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage)).pack(side="bottom")

class PageThree(tk.Frame):
    """Menu Frame that links the store to here"""
    #Done by Jianhong
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage)).pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne)).pack()


if __name__ == "__main__":
    app = Guiinterface()
    app.mainloop()
