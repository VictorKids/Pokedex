#Pokédex
>It only works up to gen1 until now.
<h2>Step 0:</h2>
  Convert the .csv database to a .db if you does not have the .db yet or want to get a new version from kaggle (https://www.kaggle.com/datasets/rounakbanik/pokemon).
'''
python csv_to_db.py
'''
<h2>Step 1:</h2>
  Run the main file to open the Pokédex (Windows)
'''
python main.py
'''
  If some error about an empty database happens, comment the line with "self.import_historic()" (around line 30)
  Run the main
  After that, you can uncomment the line

<h2>To Do:</h2>
* Apply clean code;
* Add more information in the hover message box;
* Create an first time run mode, to avoid the database error;
* Add up to generation 7;
* Improve the frontend.


