from os import path
import tkinter as tk 
from tkinter import ttk, NS, Canvas, Scrollbar
from tktooltip import ToolTip
import math
import sqlite3
import pickle
from PIL import ImageTk, Image

class SpritesData:
    def __init__(self, saved_sprites, saved_names, saved_ids):
        self.sprites = saved_sprites # sprites objects list
        self.names   = saved_names   # sprites name for future checking
        self.ids     = saved_ids     # sprites ids for future sorting
    
    def load_sprites_data(self, pickle_names, pickle_ids):
        self.names = pickle_names
        self.ids   = pickle_ids
        for name in self.names:
            self.sprites.append(ImageTk.PhotoImage(Image.open("imgs/"+ name +".png").resize((80,80))))

    def append_all_sprite_info(self, sprite, name, id):
        self.sprites.append(sprite)
        self.ids.append(id)
        self.names.append(name)

    def insert_all_sprite_info(self, sprite, name, id, index):
        self.sprites.insert(index, sprite)
        self.ids.insert(index, id)
        self.names.insert(index, name)

    def remove_all_sprite_info(self, index):
        del self.sprites[int(index)-1]
        del self.names[int(index)-1]
        del self.ids[int(index)-1]        

class MainApp(tk.Tk):

    def __init__(self):

        ### Initial Set Up #########################################################################################
        
        super().__init__()
        self.title("Pokédex")
        self.iconbitmap("favicon.ico")
        self.geometry("800x600")
        self.configure(background="crimson")

        ### Importing Data #########################################################################################
        
        self.connection = sqlite3.connect("pokemon.db")
        self.pkm_list = self.get_names_from_database()  
        self.sprites = SpritesData([], [], []) 
        self.sprites_control = []
        self.tooltips = []

        self.import_historic()

        ### ROW 1 - Main Title #####################################################################################
        
        self.main_title = tk.Label(self, text="Pokédex", fg="yellow", bg="crimson",
                                         font=("Helvetica, 42"), padx=280, pady=30)
        self.main_title.grid(row=0, column=0)

        ### ROW 2 - Menu Bar #######################################################################################
        
        # creating the menu bar elements objects
        self.btn_frame    = tk.Frame(self, bg="crimson")
        self.clicked      = tk.StringVar()
        self.clicked.set("Search for the new Pokémon name")
        self.combo = ttk.Combobox(self.btn_frame, textvariable=self.clicked)
        self.combo['values'] = self.pkm_list
        self.combo['state'] = 'readonly'
        self.combo.config(width=35)

        #self.drop.config(width=30)
        self.update_btn   = tk.Button(self.btn_frame, 
                                      text="Update Dex", 
                                      borderwidth=5, 
                                      command=lambda:self.print_mons()) # associate the button to a funtion call
        self.entry        = tk.Entry(self.btn_frame, text="Pokémon index")
        self.del_btn      = tk.Button(self.btn_frame, 
                                 text="Remove",  
                                 borderwidth=5, 
                                 command=lambda:self.remove_sprite())
                                 
        # grid's positioning of the menu bar elements
        #self.drop.grid(        row=0, column=0, padx=15)
        self.combo.grid(       row=0, column=0, padx=15)
        self.update_btn.grid(  row=0, column=1)
        self.entry.grid(       row=0, column=2, padx=15)
        self.del_btn.grid(     row=0, column=3)
        self.btn_frame.grid(   row=1, column=0)

        ### ROW 3 - Pokémon List ###################################################################################
        
        #section's super frame
        self.pkm_list_mainframe = tk.Frame(self, pady=20)
        self.pkm_list_mainframe.grid(row=2, column=0, pady=20)

        # left side of the frame, where the sprites will be
        self.canvas = Canvas(self.pkm_list_mainframe, width=700, height=300)
        self.canvas.grid(row=0, column=0, sticky="news")

        # right side of the frame, where the scroll bar will be
        # and connecting left side to the scroll bar action
        self.scrollbar = Scrollbar(self.pkm_list_mainframe, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns", rowspan=max(math.ceil(len(self.sprites.sprites)/4), 1))
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # internal frame of the left side canvas
        self.pkm_list_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.pkm_list_frame, anchor="nw")

        # update sprites on screen
        self.print_mons()

        # sync between left and right side
        self.pkm_list_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.pkm_list_frame.bind("<Configure>", self.reset_scrollregion)

        ### ROW 4 - Save Button ####################################################################################

        self.tail_frame    = tk.Frame(self, bg="crimson")
        self.save_btn   = tk.Button(self.tail_frame, 
                                      text="Save", 
                                      borderwidth=5, 
                                      command=lambda:self.save_historic()) # associate the button to a funtion call
        self.save_btn.grid(row=0, column=0)
        self.tail_frame.grid(row=4, column=0)


    ### Import and Export data with Pickle ##########################################################################       

    def import_historic(self):
        if path.getsize("names_historic.pkl") != 0:
            with open("names_historic.pkl", "rb") as hist_names_file:
                with open("ids_historic.pkl", "rb") as hist_ids_file:
                    self.sprites.load_sprites_data(pickle.load(hist_names_file), pickle.load(hist_ids_file))
     
    def save_historic(self):
        with open("names_historic.pkl", "wb") as hist_names_file:
            with open("ids_historic.pkl", "wb") as hist_ids_file:
                pickle.dump(self.sprites.names, hist_names_file)
                pickle.dump(self.sprites.ids, hist_ids_file)
   
    ### Database handling ##########################################################################################       

    def get_names_from_database(self):
        with self.connection:
            tuples_list = self.connection.execute("SELECT name FROM all_pokemon ORDER BY pokedex_number ASC;").fetchall()
            names_list = []
            for t in tuples_list:
                names_list.append(t[0])
            return names_list

    def get_id_from_database(self, name):
        with self.connection:
            a_tuple = self.connection.execute(f"SELECT pokedex_number FROM all_pokemon WHERE name='{name}';").fetchall()
            return a_tuple[0][0]

    def get_classification_from_database(self, name):
        with self.connection:
            a_tuple = self.connection.execute(f"SELECT classfication FROM all_pokemon WHERE name='{name}';").fetchall()
            return a_tuple[0][0]

    def get_types_from_database(self, name):
        with self.connection:
            a_tuple1 = self.connection.execute(f"SELECT type1 FROM all_pokemon WHERE name='{name}';").fetchall()       
            a_tuple2 = self.connection.execute(f"SELECT type2 FROM all_pokemon WHERE name='{name}';").fetchall()
            if a_tuple2[0][0] == None:
                return a_tuple1[0][0], ""       
            return a_tuple1[0][0], a_tuple2[0][0]       
    
    ### Utility Functions ##########################################################################################       

    def sprite_hover(self, index):
        pkm_name = self.sprites.names[index]
        pkm_num = f"{self.sprites.ids[index]}"
        pkm_classfi = self.get_classification_from_database(pkm_name)
        pkm_type1, pkm_type2 = self.get_types_from_database(pkm_name)
        pkm_info = " " + pkm_name + "  #" + pkm_num + "\n\n" + pkm_classfi + "\n\n" + pkm_type1 + " " + pkm_type2
        return pkm_info

    def reset_scrollregion(self, event):
        # redifine scrollbar size acording to sprites list updates
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def add_sprite(self, name, dex_number):
        if name not in self.sprites.names:                
            if len(self.sprites.ids) == 0 or self.sprites.ids[-1] <= dex_number: # if the id is the final id in the list
                self.sprites.append_all_sprite_info(ImageTk.PhotoImage(Image.open("imgs/"+ name +".png").resize((80,80))), name, dex_number)               
            else:
                for id_index in range(len(self.sprites.ids)):
                    if dex_number <= self.sprites.ids[id_index]:
                        self.sprites.insert_all_sprite_info(ImageTk.PhotoImage(Image.open("imgs/"+ name +".png").resize((80,80))), name, dex_number, id_index)
                        break
            # add a sprite in the sprites list (and sort it by (not yet))

    def print_mons(self):
        # check if an option from the drop down menu has been selected
        tmp_name = self.clicked.get()
        if tmp_name != "Search for the new Pokémon name":
            self.add_sprite(tmp_name, self.get_id_from_database(tmp_name))
        k = 0
        j = 0
        # remove past sprites list labels, this way past elements will not apper in unplesent positions 
        for i in self.sprites_control:
            i.destroy()

        # reprint all sprites, saving references to the objects to an easier remove later, if needed
        for i in range(len(self.sprites.sprites)):
            lab = tk.Label(self.pkm_list_frame, image=self.sprites.sprites[i])
            tip = ToolTip(lab, msg=self.sprite_hover(i))
            self.sprites_control.append(lab)
            self.tooltips.append(tip)
            lab.grid(row=j, column=k)
            k += 1
            if k % 8 == 0:
                j += 1
                k = 0
        # resets standard string to avoid duplicated inserts
        self.clicked.set("Search for the new Pokémon name")

    def remove_sprite(self):
        # get the input in the entry
        # checks if it is viable, and if yes, remove the respective sprite
        index = self.entry.get()
        if index.isdecimal() and int(index) <= len(self.sprites.sprites) and int(index) > 0:
            self.sprites.remove_all_sprite_info(index)
            self.print_mons()
        self.entry.delete(0, 'end') # clean the entry area

### Main ###########################################################################################################
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()