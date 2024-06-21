import tkinter as tk
from tkinter import ttk
import sqlite3
import os
from PIL import Image, ImageTk


class Escena:
    def __init__(self, master):
        self.master = master
        self.master.geometry("900x450")
        master.iconbitmap(icon_directory)
        master.title("Crops Searcher")
        # Frame
        self.frame = tk.Frame(self.master)
        # Title
        self.label = tk.Label(self.frame, text="Stardew Valley Crops Searcher", font=font["title"])
        self.label.pack(pady=20)
        
        # Searcher
        
        self.options = ["Amaranth","Ancient Fruit","Artichoke","Beet","Blue Jazz","Blueberry","Bok Choy","Cactus Fruit","Cauliflower","Coffee Bean","Corn","Cranberries","Eggplant","Fairy Rose","Garlic","Grape","Green Bean","Hops","Hot Pepper","Kale","Melon","Parsnip","Pineapple","Poppy","Potato","Pumpkin","Radish","Red Cabbage","Rhubarb","Starfruit","Strawberry","Summer Spangle","Sunflower","Sweet Gem Berry","Taro Root","Tomato","Tulip","Unmilled Rice","Wheat","Yam"]
        
        self.selected_value = tk.StringVar()
        
        self.combobox = ttk.Combobox(self.frame, textvariable=self.selected_value, values=self.options)
        self.combobox.pack()
        self.combobox.focus()
        self.combobox.bind('<KeyRelease>', self.update_options)
        self.combobox.bind('<Return>', lambda event: self.search(self.combobox))
        self.combobox.bind("<<ComboboxSelected>>", lambda event: self.search(self.combobox))
        
        # No coincidense warning
        self.warning = tk.Label(self.frame, text="", foreground="red", font=font["warning"])
        self.warning.pack()
        
        # Button to search
        search_button = tk.Button(self.frame, text="Search", command=lambda entry=self.combobox : self.search(entry))
        search_button.pack(pady=3)
        
        # Creating information Frame
        information_frame = tk.Frame(self.frame, bd=1, relief="solid", width=300, height=200)
        information_frame.pack(pady=15)

        # Creating a Canvas for The Image
        self.crop_image = tk.Canvas(information_frame, bg="white", width=100, height=200)
        self.crop_image.pack(side="left")

        # Adding the image into the Canvas
        image_directory = os.path.join(directory, "images/example.png")
        image = Image.open(image_directory)
        image = image.resize((100,100))
        image = ImageTk.PhotoImage(image)
        self.crop_image.image = image 
        self.crop_photo = self.crop_image.create_image(0, 80, anchor="nw", image=image)
        
        # Adding text into the canvas
        self.crop_name = self.crop_image.create_text(50, 20, text="", font=("Arial", 12))

        # Creating a Frame for the text boxes
        boxes_frame = tk.Frame(information_frame, bg="white", bd=1, relief="solid")
        boxes_frame.pack(side="right", fill="both", expand=True)

        # Creating the Boxes
        self.boxes = []
        for j in range(6):
            text = f"                           "
            box = tk.Label(boxes_frame, text=text, padx=10, pady=5, borderwidth=1, relief="solid", font=font["information"])
            box.grid(row=0, column=j, sticky="nsew")
            self.boxes.append(box)

        # Configurar el grid dentro del marco_texto
        boxes_frame.grid_rowconfigure(0, weight=2)


        self.frame.pack()
        


    def search(self,entry):
        crop = entry.get()
        crop = crop.strip().title()
        crop = [crop]
        
        
        
        # Getting informacion from the database
        cursor.execute("""SELECT "name" FROM "crops" WHERE "name" = (?) """,crop)
        name = cursor.fetchone()[0]

        # cheking if input is valid
        if not name:
            self.warning.config(text="Not found")
            return
        else:
            self.warning.config(text="")
            
        cursor.execute('''SELECT * FROM "crops" WHERE name = (?)''', crop)
        data = [dict(row) for row in cursor.fetchall()][0]

            
        # Getting all the rest of the information
        p_pierre = data["price_pierre"]
        
        p_joja = data["price_joja"]
        
        grow_days = data["days_grow"]
        
        season = data["season"]
        
        price_n = data["sellng_price_n"]
        
        price_s = data["sellng_price_s"]
        
        price_g = data["sellng_price_g"]
        
        price_i = data["sellng_price_i"]
        
        multi = data["multi_crop"]
        
        re_harvest = data["multi_harvest"]
        
        g_perday = data["g_perday"]
        
        id = data["id"]
        
        cursor.execute(f"""SELECT "use" FROM "uses" WHERE "id" = '{id}' """)
        uses = cursor.fetchall()

        # Re formating the data
        if re_harvest == (0,):
            re_harvest = "No"
        else:
            re_harvest = "Yes"
        
        if multi == (0,):
            multi = "No"
        else:
            multi = "Yes"
            
        if len(uses) > 0:
            uses_str = "Uses: \n"
            for use in uses[0]:
                uses_str = uses_str + f"{use} \n"
        else:
            uses_str = "No uses"
            
        if season == "/":
            season = "Can't be cultivated\n in any season"
        elif season.find("/") != -1:
            slash = season.find("/")
            season1 = season[:slash]
            if season[slash+1:].find("/") != -1:
                new_season = season[slash+1:]
                slash = new_season.find("/")
                season = f"Can be cultivated in {season1},\n {new_season[:slash]} and {new_season[slash+1:]}"
            else:
                season = f"Can be cultivated\n in {season1} and {season[slash+1:]}"
        else:
            season = f"Can be cultivated\n in {season}"
            
            
        # showing the information
        image_directory = os.path.join(directory, f"images/crop{id}.png")
        image = Image.open(image_directory)
        image = image.resize((100,100))
        image = ImageTk.PhotoImage(image)
        self.crop_image.image = image 
        self.crop_image.itemconfigure(self.crop_name, text=f"{name}\ngpd={g_perday}")
        self.crop_image.itemconfigure(self.crop_photo, image=image)
        self.boxes[0].config(text=f"//PRICE//\nPierre's: {p_pierre}\nJoja's: {p_joja}")
        self.boxes[1].config(text=f"Takes\n {grow_days} days to grow")
        self.boxes[2].config(text=season)
        self.boxes[3].config(text=f"//SELL//\nNormal Quality: {price_n}\nSilver Quality: {price_s}\nGold Quality: {price_g}\nIridium Quality: {price_i}")
        self.boxes[4].config(text=f"Multi Harvest: {re_harvest}\nMulti Production: {multi}")
        self.boxes[5].config(text=uses_str)
        
        
    def update_options(self, event):

        input_text = self.combobox.get()
        filtered_options = [option for option in self.options if option.lower().startswith(input_text.lower().strip())]


        self.combobox['values'] = filtered_options




# Geting important variabels as cursor or directory for connecting to database and loading images
directory = os.path.dirname(os.path.abspath(__file__))
db_directory = os.path.join(directory, 'stardew.db')
conection = sqlite3.connect(db_directory)
conection.row_factory = sqlite3.Row
cursor = conection.cursor()
directory = os.path.dirname(os.path.abspath(__file__))
icon_directory = os.path.join(directory, "images/example.ico")


# Creating the window 
root = tk.Tk()
font = {
    "title" : ("Arial", 21),
    "warning" : ("Arial", 10),
    "information" : ("Arial", 10)
}
current_scene = "escena1"
escena1 = Escena(root)

root.mainloop()