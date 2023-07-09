import sqlite3
import pandas as pd

df = pd.read_csv('pokemon.csv')

df.columns = df.columns.str.strip()

connection = sqlite3.connect('pokemon.db')

df.to_sql('all_pokemon', connection, if_exists='replace')

connection.close()