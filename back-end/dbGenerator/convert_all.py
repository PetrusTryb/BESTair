#!../pyenv/bin/python
import convert_data
import convert_meta
import db_control
import download_data

def main():
  print('Removing prevoius db...')
  db_control.dropDatabase()
  print('Downloading data...')
  download_data.downloadData()
  print('Adding stations metadata')
  convert_meta.main()
  print('Adding pollution data...')
  convert_data.main()
  print('Removing downloaded data...')
  download_data.removeDatafiles()
  print('Done!')

if __name__ == '__main__':
  main()