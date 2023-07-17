# Pokédex

>It only works up to gen1 until now.

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

<h3>To Do:</h3>

* Apply clean code rules;
* Add more information in the hover message box;
* Create a first time run mode, to avoid the database error;
* Add up to generation 7;
* Improve the frontend.


