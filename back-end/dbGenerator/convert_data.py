#!./pyenv/bin/python
import openpyxl
import os
import sqlite3
import datetime
import itertools
import re
import db_control
import sys

                
def checkUnit(filename):
  wb = openpyxl.open(filename)
  sheet = wb.active
  data = []
  for row in sheet.iter_rows(max_row=7):
    rowData = []
    for cell in row:
      rowData.append(cell.value)
    data.append(rowData)
  try:
    return next(filter(lambda x: x[0] == 'Jednostka', data))
  except Exception as e:
    return None

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

def insertDataFromFileToDb(filename, db = db_control.getDbConnection()):
  data = getDataFromFile(filename)
  indicatorTypes = ['NO2', 'NOx', 'O3', 'PM10', 'SO2', 'BaP(PM10)', 'C6H6', 'Cd(PM10)', 'Ni(PM10)', 'As(PM10)', 'Pb(PM10)', 'PM2.5', 'CO', 'BaA(PM10)', 'BbF(PM10)', 'BjF(PM10)', 'BkF(PM10)', 'DBahA(PM10)', 'IP(PM10)', 'formaldehyd', 'Ca2+(PM2.5)', 'Cl', 'EC(PM2.5)', 'K+(PM2.5)', 'Mg2+(PM2.5)', 'Na+(PM2.5)', 'NH4+(PM2.5)', 'NO3-(PM2.5)', 'OC(PM2.5)', 'SO42', 'DBah(PM10)', 'depozycja', 'Hg(TGM)', 'Jony', 'PM25', 'Depozycja', 'NO', 'PrekursoryZielonka', 'HG(TGM)']
  codes = []
  indicator = os.path.basename(filename).split('_')[-2]
  
  units = []
  for i in range(5):
    row = data[i]
    example = str(row[1])
    if(example == '1g'): # skip 1h data
      return
    elif('/' in example):
      units = row[1:]
    elif(not example in indicatorTypes and example != '1g' and example != '24g' and type(row[0]) != datetime.datetime):
      codes = row[1:]
  print(codes, indicator, units, sep='\n')
  
  # skip headers
  def isHeader(row):
    if type(row[0]) is datetime.datetime:
      return False
    return True
  data = itertools.dropwhile(isHeader, data[1:])


  # change polish numbers to floats
  def plNumToFloat(x):
    if x is None:
      return x
    return float(str(x).replace(',', '.'))
  data = [[row[0], *map(plNumToFloat, row[1:])] for row in data]

  #indicator = next(itertools.dropwhile(lambda x: x is None, indicators))
  unit = None
  if len(units) > 0:
    unit = next(itertools.dropwhile(lambda x: x is None, units))

  # find ids for all stations
  station_ids = []
  for code in codes:
    cur = db.cursor()
    station_id_query = 'SELECT id FROM stations WHERE code = ? OR old_code = ?'
    cur.execute(station_id_query, [code]*2)
    results = cur.fetchall()
    if len(results) < 1:
      station_ids.append(None)
      continue
    station_ids.append(results[0][0])

  print(station_ids)

  for row in data:
    date = row[0]
    if date is None:
      continue
    for station_id, value in itertools.zip_longest(station_ids, row[1:]):
      if station_id is None:
        continue

      value_data = {
        'station_id': station_id,
        'indicator': indicator,
        'date': date,
        'value': value,
        'unit': unit,
      }
      #print(value_data)
      db_control.insertDataToDb(value_data, 'pollution', db)
  db.commit()

def main():
  db = db_control.getDbConnection()

  for subdir, dirs, files in os.walk('./datafiles/'):
    for file in files:
      filename = os.path.join(subdir, file)
      if '_24g' not in filename:
        continue
      print(filename)
      insertDataFromFileToDb(filename, db)

if __name__ == '__main__':
  main()