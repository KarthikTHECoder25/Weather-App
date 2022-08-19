from tkinter import *
from PIL import ImageTk, Image
import sqlite3
import requests
import json
from tkinter import messagebox

root = Tk()
root.title("Karthik's Weather App")
root.geometry("1100x510")
root.configure(background = "#ADD8E6")

conn = sqlite3.connect('favorites.db')
c = conn.cursor()

'''c.execute("""Create TABLE favorites(
        location text,
        temperature text
        )""")'''

filler = Label(root, text = "Hello everyone I like to read about weather and many other weather related topics as ", bg = "#ADD8E6", fg = "#ADD8E6").grid(row = 0, column = 1)


tempactual = Label(root, text = 'Loading...', font = ("Helvectica", 15),  bg = "white")
tempactual.grid(row = 2, column = 0, pady = (5, 80))

uvactual = Label(root, text = 'Loading...', font = ("Helvectica", 15),  bg = "white")
uvactual.grid(row = 4, column = 0, pady = (5, 80))

windspeedactual = Label(root, text = 'Loading...', font = ("Helvectica", 15),  bg = "white")
windspeedactual.grid(row = 6, column = 0, pady = (5, 80))

precipactual = Label(root, text = 'Loading...', font = ("Helvectica", 15),  bg = "white")
precipactual.grid(row = 4, column = 2, pady = (5, 80))

aqiActual = Label(root, text = 'Loading...', font = ("Helvectica", 15),  bg = "white")
aqiActual.grid(row = 2, column = 2, pady = (5, 80))

locationlabel = Label(root)
iconlabel = Label(root)

y = StringVar() 
y.set("Not Favorited") 

search_bar = Entry(root, width = 35)
search_bar.grid(row = 0, column = 2, sticky = W , pady = 5)



def exit():
    response = messagebox.askokcancel("Exit Program","You are about to exit this app. ")
    if response == 1 or response == 'ok':
        root.quit()
    else:
        pass

def lookup():
    #try:
    conn = sqlite3.connect("favorites.db")
    c = conn.cursor()
    
    global tempactual
    global uvactual
    global windspeedactual
    global precipactual
    global aqiActual
    global locationlabel
    global iconlabel
    global icon
    global iconimage
    global pcicon
    global cicon
    global clearicon
    global raining
    global x
    global specialparameterlabel
    global specialparameter
    global y
    global location
    global temperature

    data_location = []
    

    if y.get() == "Favorited":
        c.execute("SELECT *, oid from favorites")
        record2 = c.fetchall()
        print(record2)

        for record in record2:
            data_location += record
        

   
        if location not in data_location:
            c.execute("INSERT INTO favorites VALUES(:location, :temperature)",
            {   
            'location' : location,
            'temperature' : temperature
            })
        else:
            error = messagebox.showerror("Warning", "This location has already been favorited. Please try again.")
        
    print(data_location)
    
    conn.commit()
    conn.close()

    favorite = Checkbutton(root, text = "Favorite", variable = y, onvalue = "Favorited", offvalue = "Not Favorited")
    favorite.deselect()
    favorite.grid(row = 5, column  = 1, pady = (0,10))
    #print(y.get())

    url = "https://api.ambeedata.com/latest/by-city"
    querystring = {"city":search_bar.get()}
    headers = {
        'x-api-key': "99be5b6893333b9cac1f767f922a5759800f80e7e958ce6b62e854b5a169ea1a",
        'Content-type': "application/json"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    api1 = json.loads(response.content)

    latitude = str(api1["stations"][0]["lat"])
    longitude = str(api1["stations"][0]["lng"])
    #api_key = "eb48923fb7c9b66171ad156a2f34b2e8"

    #url = f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&exclude=hourly,minutely&appid={api_key}"  
    #api2 = requests.get(url).json()
    

    url2 = "https://api.ambeedata.com/weather/latest/by-lat-lng"
    querystring2 = {"lat": latitude,"lng":longitude}
    headers2 = {
        'x-api-key': "99be5b6893333b9cac1f767f922a5759800f80e7e958ce6b62e854b5a169ea1a",
        'Content-type': "application/json"
        }
    api2_response = requests.request("GET", url2, headers=headers2, params=querystring2)
    api2 = json.loads(api2_response.content)

    temperature = str(api2['data']['temperature']) + "°F"
    uv = api2['data']['cloudCover']
    windspeed = str(api2['data']['windSpeed']) + " MPH"
    icon_raw = api2['data']['icon']
    iconstring =  'Condition - ' + icon_raw[0].upper() + icon_raw[1:]
    #precipercent = str(api2[" data"]["precipProbability"] * 100) + '%'+  ' chance of ' + str(api2["data"]["precipType"])
    precipercent = api2["data"]["precipIntensity"]
    aqi = str(api1['stations'][0]['AQI']) + " - " +api1['stations'][0]['aqiInfo']['category']

    data = search_bar.get()
    dataupdated = data[0].upper() + data[1:]

    try: 
        location = str(dataupdated)+ ", " + api1['stations'][0]['countryCode']  
    except:
        location = str(dataupdated)+ ", " + api1['stations'][0]['state'] + ", "  + api1['stations'][0]['countryCode'] 

    tempactual.grid_forget()
    uvactual.grid_forget()
    windspeedactual.grid_forget()
    locationlabel.grid_forget()
    iconlabel.grid_forget()
    aqiActual.grid_forget()
    precipactual.grid_forget()
    icon.grid_forget()
    specialparameterlabel.grid_forget()
    specialparameter.grid_forget()
    
    pcicon = ImageTk.PhotoImage(Image.open("C:/Python/GUI/weatherappimages/partly-cloudy.png"))
    cicon = ImageTk.PhotoImage(Image.open("C:/Python/GUI/weatherappimages/cloudy.png"))
    clearicon =  ImageTk.PhotoImage(Image.open("C:/Python/GUI/weatherappimages/clear.png"))
    raining = ImageTk.PhotoImage(Image.open("C:/Python/GUI/weatherappimages/raining.png"))

    icondict = {
        'partly-cloudy': pcicon,
        'cloudy': cicon,
        'clear': clearicon,
        'raining': raining 
    }
    
    choice = api2['data']['icon']
   
    #picture = icondict[choice]
    
    if choice not in icondict.keys():
        picture = iconimage
    else: 
        picture = icondict[choice]

    icon = Label(root, image = picture, borderwidth = 3, relief = RAISED)
    icon.grid(row = 2, column = 1, pady = (0, 10))

    tempactual = Label(root, text = temperature, font = ("Helvectica", 15), borderwidth = 3, relief = RIDGE)
    tempactual.grid(row = 2, column = 0, pady = (5, 70))

    uvactual = Label(root, text = uv, font = ("Helvectica", 15), borderwidth = 3, relief = RIDGE)
    uvactual.grid(row = 4, column = 0, pady = (5, 70))

    windspeedactual = Label(root, text = windspeed, font = ("Helvectica", 15), borderwidth = 3, relief = RIDGE)
    windspeedactual.grid(row = 6, column = 0, pady = (5, 70))

    precipactual = Label(root, text = precipercent, font = ("Helvectica", 15), borderwidth = 3, relief = RIDGE)
    precipactual.grid(row = 4, column = 2, pady = (5, 70))


    aqi_color = {

        'Good': "#0C0",
        'Moderate':"yellow",
        'Unhealthy':'orange',
        'Very Unhealthy': 'red'
    }
    
    category = str(api1['stations'][0]['aqiInfo']['category'])
    color = aqi_color[category]           
    aqiActualcover = Label(root, text = aqi, font = ("Helvectica", 15), bg = "#ADD8E6", fg = "#ADD8E6")
    aqiActualcover.grid(row = 2, column = 2, pady = (5, 70))
    aqiActual = Label(root, text = aqi, font = ("Helvectica", 15), borderwidth = 3, relief = RIDGE, bg = color)
    aqiActual.grid(row = 2, column = 2, pady = (5, 70))

    locationlabel = Label(root, text = location, font = ("Helvectica", 20), borderwidth = 5, relief = RIDGE)
    locationlabel.grid(row = 3, column = 1, pady = 5)

    iconlabel = Label(root, text = iconstring, font = ("Helvectica", 15), borderwidth = 5, relief = RIDGE)
    iconlabel.grid(row = 4, column = 1, pady = 5)

    #Creating Special Parameter Dispay
    var = x.get()
    var_label = var.lower()

    if var != None:
        specialparameterlabel = Label(root, text = var_label[0].upper() + var_label[1:], font = ("Helvectica", 15), borderwidth= 2, relief = RIDGE)
        specialparameterlabel.grid(row = 5, column = 2)
    else:
        pass
        
    #Creating Favorite System


    try:
        specialparameter = Label(root, text = str(api2['data'][var]), font = ("Helvectica", 15), borderwidth = 3, relief = RIDGE)
        specialparameter.grid(row = 6, column = 2, pady = (5, 70))
    except:
        pass

    check_uvindex = Checkbutton(root, text = "UV Index", variable = x, onvalue = "uvIndex", offvalue = "None" )
    check_uvindex.deselect()
    check_uvindex.grid(row = 1, column = 3)

    check_visibility = Checkbutton(root, text = "Visibility", variable = x, onvalue = "visibility", offvalue = "None")
    check_visibility.deselect()
    check_visibility.grid(row = 2, column = 3)

    check_windgust = Checkbutton(root, text = "Wind Gust", variable = x, onvalue = "windGust", offvalue = "None" )
    check_windgust.deselect()
    check_windgust.grid(row = 3, column = 3)

    check_humidity = Checkbutton(root, text = "Humidity", variable = x, onvalue = "Humidity", offvalue = "None" )
    check_humidity.deselect()
    check_humidity.grid(row = 4, column = 3)

    check_dewpoint = Checkbutton(root, text = "Dew Point", variable = x, onvalue = "dewPoint", offvalue = "None" )
    check_dewpoint.deselect()
    check_dewpoint.grid(row = 5, column = 3)

    #Adding favorites to database



    search_bar.delete(0,END)


z = StringVar()
z.set("Nochoice")

def delete_btn(btn):
    warning = messagebox.askyesno("Delete Warning","You are about to delete this favorite. Do you wish to continue?")
    if warning == 'yes' or warning == 1:
        conn = sqlite3.connect('favorites.db')
        c = conn.cursor()

        updated1 = list(btn.split(", "))
        id = updated1[-1]

        c.execute("DELETE from favorites WHERE oid =" + id)

        conn.commit()
        conn.close()

def fav_btn(btn):
    global search_bar
    search_bar.delete(0,END)
    updated = list(btn.split(", "))
    more_updated = updated[0] + ", " + updated[1]
    search_bar.insert(0,more_updated)
    lookup()

def option(opt):
    global z


    if opt == "Favorites":
        favs = Toplevel()
        favs.title("Favorites")
        favs.configure(background = "#ADD8E6")
        conn = sqlite3.connect('favorites.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM favorites")
        records = c.fetchall()  

        for record in records:
            print_record = str(record[0]) + " - " + str(record[1])  
            shortened_record = str(record[0]) + ", " +  str(record[-1])
            Checkbutton(favs, text = print_record, variable = z , onvalue = shortened_record, offvalue = "Nochoice" , font = ("Helvectica", 12)).pack(pady = (7,0))
            #Button(favs, text = print_record,  font = ("Helvectica", 15), command = lambda: fav_btn(record[0])).pack(padx = 5, pady = 5)
            #for_button = print_record.split(", ")
            #usablestring = for_button[0] + ", " + for_button[1] 
           
        finalize = Button(favs, text = "Submit", font = ("Helvectica", 12), command = lambda: fav_btn(z.get())).pack(pady = (15,10))
        delete = Button(favs, text = "Delete", font = ("Helvectica", 12), command = lambda: delete_btn(z.get())).pack(pady = (0, 7))
        

        conn.commit()
        conn.close()

    if opt == 'Weather':
        favs.destroy()


    
    
#Creating welcome widget
welcome = Label(root, text = 'Welcome to Weather App', borderwidth= 5, relief = GROOVE, font = ("Helvectica", 20))
welcome.grid(row = 0, column = 0, sticky = W, pady = (10, 0))

#Creating Option Menu 
select = StringVar()
select.set('Weather')

opmenulst = ['Weather', 'Favorites']

menu = OptionMenu(root, select, *opmenulst)
menu.grid(row = 0, column = 1, sticky = W, padx = (115,0))

choosebtn = Button(root, text = "Select Option", command = lambda: option(select.get()))
choosebtn.grid(row = 0, column = 1, sticky = E, padx = (0,115))

#Creating search Bar



location = search_bar.get()
temperature = "N/A (Filler)"
#Creating search Button
search_button = Button(root, text = "Search City", command = lookup) #<--- ADD COMMAND FOR LOOKUP FUNCTION
search_button.grid(row = 0, column = 3, sticky = E + W, pady = 5, padx = (10,0))
#enter_label = Label(root, text = "Enter Zipcode or City, Country: ", bd = 5)
#enter_label.grid(row = 1, column = 0 ,sticky = W)

temp_label = Label(root, text = "Temperature:", font = ("Helvectica", 15), borderwidth= 2, relief = RIDGE)
temp_label.grid(row = 1, column = 0, pady = (20,0))

uv_label = Label(root, text = "Cloud Cover:", font = ("Helvectica", 15), borderwidth= 2, relief = RIDGE)
uv_label.grid(row = 3, column = 0)

windspeed_label = Label(root, text = "Windspeed:", font = ("Helvectica", 15), borderwidth= 2, relief = RIDGE)
windspeed_label.grid(row = 5, column = 0)

precip_label = Label(root, text = "Precipitation:", font = ("Helvectica", 15), borderwidth= 2, relief = RIDGE)
precip_label.grid(row = 3, column = 2)

aqi_label = Label(root, text = "Air Quality Index:", font = ("Helvectica", 15), borderwidth= 2, relief = RIDGE)
aqi_label.grid(row = 1, column = 2, pady = (20,0))

iconimage = ImageTk.PhotoImage(Image.open("C:/Python/GUI/weatherappimages/main.png"))
icon = Label(root, image = iconimage, borderwidth = 3, relief = RAISED)
icon.grid(row = 2, column = 1, pady = (0, 5))

locationlabel = Label(root)
iconlabel = Label(root)

x = StringVar()

'''lst = [
    ('Temperature', "Temperature", "No Temp", 1), 
    ("Cloud Cover", "Cloud Cover", "No CC",2), 
    ("Windspeed", "Windspeed", "No WS", 3), 
    ("Precipitation", "Precipitation", "No Precip", 4), 
    ("AQI", "Air Quality Index", 'No AQI', 5)]

for lbl, onval, offval, num in lst:
    Checkbutton(root, text = lbl, variable = x, onvalue = onval, offvalue = offval).grid(row = num, column = 3)'''

#Creating Special Parameter Labels (Optional Choice)
check_uvindex = Checkbutton(root, text = "UV Index", variable = x, onvalue = "uvIndex", offvalue = "None" )
check_uvindex.deselect()
check_uvindex.grid(row = 1, column = 3)

check_visibility = Checkbutton(root, text = "Visibility", variable = x, onvalue = "visibility", offvalue = "None")
check_visibility.deselect()
check_visibility.grid(row = 2, column = 3)

check_windgust = Checkbutton(root, text = "Wind Gust", variable = x, onvalue = "windGust", offvalue = "None" )
check_windgust.deselect()
check_windgust.grid(row = 3, column = 3)

check_humidity = Checkbutton(root, text = "Humidity", variable = x, onvalue = "Humidity", offvalue = "None" )
check_humidity.deselect()
check_humidity.grid(row = 4, column = 3)

check_dewpoint = Checkbutton(root, text = "Dew Point", variable = x, onvalue = "dewPoint", offvalue = "None" )
check_dewpoint.deselect()
check_dewpoint.grid(row = 5, column = 3)



specialparameterlabel = Label(root)
specialparameter = Label(root)

exit_program = Button(root, text = "Exit App", command = exit)
exit_program.grid(row = 6, column = 1)

conn.commit()
conn.close()

root.mainloop()
