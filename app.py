import os
import subprocess
import requests as request
import asyncio
import time
from datetime import datetime
from random import randint

# Dependency of program
# - Feh

# Python Module Dependency
# - request ( To Fetch )

# TODO -
# Add many tags and randomly pick a one
# Make a GUI Version of this script

class RandomWallpaper():
    def __init__(self):
        self.dir = []
        self.latest_img = ""
        self.query = []
        self.images = []
        self.__app_id = ""

        if self.__app_id == "":
            print("Add a proper unsplash api key in __app_id variable")
            quit()

    def setQuery(self):
        """
        This function changes the query by time
        """
        time_obj = datetime.now()
        time = int(time_obj.strftime("%H"))

        if time > 12:
            self.query = [
                 "Nature-Morning",
                 "Sun-Rise",
                 "Cool-Morning"
            ]
        elif time < 19:
            self.query = [
                "Hot-Weather",
                "Sun-in-Noon",
                "Warm-Weather",
                "Hot-Day"
           ]
        else:
            self.query = [
                "moon",
                "dark Trees",
                "dark Nature"
            ]

    async def fetchImages(self):
        url = f"https://api.unsplash.com/photos"
        random_query = randint(0, len(self.query) - 1)
        params = { "client_id": self.__app_id, "query": self.query[random_query] }
        
        res = request.get(url = url, params = params)
        self.images = res.json()
    
    def setWallpaper(self):
        random_wallpaper = randint(0, len(self.images) - 2)
        active_img = self.images[random_wallpaper]
        img_url = active_img["urls"]["raw"]
        get_img = request.get(url = img_url) 
        
        def saveImg(fetched_img):
            img_dir = os.path.expanduser("~/.local/share/dw/")
            
            if not os.path.isdir(img_dir):
                os.mkdir(img_dir)

            file_path = img_dir + active_img["id"] + ".jpg"

            for random_number in range(15):
                random_numbers = randint(0, 15)
                random_numbers = str(random_numbers) + str(random_numbers)
                file_path = img_dir+ active_img["id"] + ".jpg"

            with open(file_path, "wb") as img:
                img.write(fetched_img.content)
            
            # Set latest img
            self.latest_img = file_path

        saveImg(get_img)

        wallpaper_command = "feh --bg-fill "  + self.latest_img
        subprocess.Popen(wallpaper_command.split(), stdout=subprocess.PIPE)
        
    def run(self):
        while True:
            self.setQuery()
            print("Setted query..")

            asyncio.run(self.fetchImages())
            print("Fetched Image..")

            self.setWallpaper()
            print("Setted Wallpaper, done ...")
            
            time.sleep(20 * 60) # Change wallpaper in delay of 20 mins
                
app = RandomWallpaper() 
app.run()

