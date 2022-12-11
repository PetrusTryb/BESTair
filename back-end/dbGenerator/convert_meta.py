#!./pyenv/bin/python
import openpyxl
import os
import sqlite3
import db_control

def getDataFromFile(filename):
  wb = openpyxl.open(filename)
  sheet = wb.active
  data = []
  for row in sheet.iter_rows():
    rowData = []
    for cell in row:
      rowData.append(cell.value)
    data.append(rowData)
  return data

def insertDataFromFileToDb(filename, db):
  data = getDataFromFile(filename)[1:]
  for row in data:
    station = {}
    station['code'] = row[1]
    station['name'] = row[3]
    station['old_code'] = row[4]
    station['voivodeship'] = row[10].title()
    station['city'] = row[11]
    station['latitude'] = float(row[13])
    station['longitude'] = float(row[14])
    
    db_control.insertDataToDb(station, 'stations', db)
  db.commit()

def main():
  db = db_control.getDbConnection()
  filename = './datafiles/metadata.xlsx'
  insertDataFromFileToDb(filename, db)

if __name__ == '__main__':
  main()