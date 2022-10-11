# Import the required libraries
from tkinter import *
#import tkinter as tk
import requests
from PIL import Image, ImageTk

# Create an instance of Tkinter Frame
app = Tk()


# Set the geometry of Tkinter Frame
app.geometry("700x450")

#WIDTH = 700
#HEIGHT = 450

# Open the Image File
bg_image = ImageTk.PhotoImage(file="landscape.png")
background_label = Label(app, image=bg_image, compound="top")
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create a Canvas
C = Canvas(app, width=700, height=3500)
C.pack(fill=BOTH, expand=True)

# Add Image inside the Canvas
C.create_image(0, 0, image=bg_image, anchor='nw')

frame = Frame(app, bg="blueviolet", bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor="n")

textbox = Entry(frame, font=40)
textbox.place(relwidth=0.65, relheight=1)

submit = Button(frame, text="Get Weather", font=40, command=lambda: getWeather(textbox.get()))
# submit.config(font=)
submit.place(relx=0.7, relwidth=0.3, relheight=1)

lower_frame = Frame(app, bg="blueviolet", bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor="n")

bg_color = "white"
results = Label(lower_frame, anchor="nw", justify="center", bd=4)
results.config(font=40, bg=bg_color)
results.place(relwidth=1, relheight=1)

weather_icon = Canvas(results, bg=bg_color)
weather_icon.place(relx=0.75, rely=0, relwidth=1, relheight=0.5, anchor="n")

def responseFormat(weather_json):
    while True:
        try:
            city = weather_json["name"]
            conditions = weather_json["weather"][0]["description"]
            temp = weather_json["main"]["temp"]
            final = "City: %s \nConditions: %s \nTemperature (°C): %s" % (city, conditions, temp)
        except:
            final = "There was a problem retrieving this information."
        return final

def getWeather(city):
    weather_key = "9e96f6ccd27fb16042c7f9e0b6245231"
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"APPID": weather_key, "q": city, "units":"imperial"}
    response = requests.get(url, params=params)
    print(response.json())
    weather_json = response.json()

    results["text"] = responseFormat(response.json())

    icon_name = weather_json["weather"][0]["icon"]
    openImage(icon_name)

def openImage(icon):
    size = int(lower_frame.winfo_height()*0.25)
    img = ImageTk.PhotoImage(Image.open("./img/"+icon+".png").resize((size, size)))
    weather_icon.delete("all")
    weather_icon.create_image(0, 0, anchor="nw", image=img)
    weather_icon.image = img

# Function to resize the window
def resizeImage(e):
    global image, resized, resizedImage
    # open image to resize it
    image = Image.open("landscape.png")
    # resize the image with width and height of root
    resized = image.resize((e.width, e.height), Image.ANTIALIAS)

    resizedImage = ImageTk.PhotoImage(resized)
    C.create_image(0, 0, image=resizedImage, anchor='nw')

# Bind the function to configure the parent window
app.bind("<Configure>", resizeImage)
app.mainloop()