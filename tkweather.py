import tkinter as tk
import requests, json
from io import BytesIO
from PIL import ImageTk, Image
import datetime

base_url = "http://api.openweathermap.org/data/2.5/weather?"
forecast_url = "http://api.openweathermap.org/data/2.5/forecast?"
api_key= "8fe79b85155beefc0a3882d4b1377ddd"

pics = {}

def createDay(date,info):
    global pics
    dayFrame = tk.Frame(forecastWeatherFrame)
    dayFrame.pack(side = tk.LEFT)

    year, month, day = date.split("-")
    formatted = datetime.date(int(year),int(month),int(day))
    weekday = formatted.strftime("%A")
    tk.Label(dayFrame, text = weekday).pack()
    tk.Label(dayFrame, text = date).pack()

    temp = str(int(info[0]))+'\u00b0'+"F"
    tk.Label(dayFrame, text = temp  ).pack()

    if(not date in pics):
        url = "http://openweathermap.org/img/wn/"+info[1]+"@2x.png"
        resp = requests.get(url)
        data = resp.content
        pic = Image.open(BytesIO(data))
        icon = ImageTk.PhotoImage(image = pic)
        pics[date] = icon
    else:
        icon = pics[date]

    tk.Label(dayFrame,bg = "white" ,image = icon , text = info[2], compound= tk.TOP).pack()

def getInfo(dummy= None):
    city_Name = city.get()
    complete_url = base_url + "appid=" + api_key + "&q=" +city_Name +"&units=imperial"
    cforecast_url = forecast_url + "appid=" + api_key + "&q=" +city_Name +"&units=imperial"
    
    response= requests.get(complete_url)
    responseFore = requests.get(cforecast_url)

    info = response.json()
    infoFore = responseFore.json()

    currentTemp = info["main"]["temp"]
    currentDesc= info["weather"][0]["description"]

    print(currentTemp)
    print(currentDesc)

    forecast ={}
    
    for day in infoFore["list"]:
        dateText= day["dt_txt"]
        dayText = dateText.split(" ")[0]
        temp = day["main"]["temp"]
        icon = day["weather"][0]["icon"]
        desc = day["weather"][0]["description"]

        if(not dayText in forecast):
            forecast[dayText]= [temp, icon, desc]

    for day in forecast:
        createDay(day,forecast[day]) 


main = tk.Tk()

city = tk.StringVar()
cityName = tk.Entry(main, textvariable = city)
cityName.pack()

submitButton= tk.Button(main,text = "submit",command = getInfo)
submitButton.pack()

currentWeatherFrame = tk.Frame(main)
currentWeatherFrame.pack()

forecastWeatherFrame = tk.Frame(main)
forecastWeatherFrame.pack()

main.bind("<Return>", getInfo)

main.mainloop()

