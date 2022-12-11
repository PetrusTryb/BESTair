import sqlite3
import os

DB_FILEPATH = './data.db'

def getDbConnection():
  connection = sqlite3.connect(DB_FILEPATH)
  sql1 = """CREATE TABLE IF NOT EXISTS stations(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    code STRING NOT NULL UNIQUE,
    name STRING NOT NULL,
    old_code STRING,
    voivodeship STRING,
    city STRING,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
  )
  """
  sql2 = """CREATE TABLE IF NOT EXISTS pollution (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    station_id INTEGER NOT NULL,
    indicator STRING NOT NULL,
    date DATETIME NOT NULL,
    value REAL,
    unit STRING,
    FOREIGN KEY (station_id)
      REFERENCES stations (id)
  )
  """
  connection.execute(sql1)
  connection.execute(sql2)
  connection.commit()
  return connection

def insertDataToDb(data:dict, table:str, db):
  keys = ', '.join(data.keys())
  question_marks = ', '.join(['?']*len(data))
  sql = f'INSERT INTO {table} ({keys}) VALUES ({question_marks})'
  # print(sql, list(data.values()))
  db.execute(sql, list(data.values()))

def dropDatabase():
  if os.path.isfile(DB_FILEPATH):
    os.remove(DB_FILEPATH)