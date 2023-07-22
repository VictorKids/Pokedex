<h1 align="center"> Pokédex </h1>

A Python grafical user interface project originated from a idea in a Pokémon RPG play test. It emulates some of the features of a Pokédex in order to allow the players to track all Pokémon they have seen during their journey.

<h3>Technologies</h3>

* Python
    * Tkinter
    * Pickle
* Sqlite3


>It only works up to gen1 until now.

---

<h3>Step 0:</h3>

  Convert the .csv database to a .db if you does not have the .db yet or want to get a new version from kaggle (https://www.kaggle.com/datasets/rounakbanik/pokemon).
  
```
python csv_to_db.py
```

<h3>Step 1:</h3>

  Run the main file to open the Pokédex (Windows)
  
```  
python main.py
```

  If some error about an empty database happens, comment the line with "self.import_historic()" (around line 30), then run the main. After that, you can uncomment the line.

---

<h3>To Do:</h3>

* Apply clean code rules; <a href='' target="_blank"><img alt='on progress' src='https://img.shields.io/badge/on_progress-100000?style=for-the-badge&logo=on progress&logoColor=FFFFFF&labelColor=black&color=EADB0E'/></a>
* Add more information in the hover message box;
* Create a first time run mode, to avoid the database error;
* Add up to generation 7;
* Improve the frontend.


