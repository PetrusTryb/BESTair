#!./pyenv/bin/python
import urllib.request
from pathlib import Path
import zipfile
import os
import shutil

datafilesPath = "./datafiles/"

def downloadFile(url, path):
  Path(path).parent.mkdir(parents=True, exist_ok=True)
  print("Downloading file from: " + url)
  urllib.request.urlretrieve(url, path)

def downloadData():
  baseurl = "https://powietrze.gios.gov.pl/pjp/archives/downloadFile/"
  cachePath = "./.cache/"
  filesIds = [ 223, 224, 225, 226, 202, 203, 227, 228, 229, 230, 231, 232, 233, 234, 302, 236, 242, 262, 303, 322, 424, 486 ]
  for index, id in enumerate(filesIds):
      url = baseurl + str(id)
      year = 2000 + index
      path = f"{cachePath}{year}.zip"
      downloadFile(url, path)
      print("Unzipping file: " + path)
      with zipfile.ZipFile(path,"r") as zip_ref:
          zip_ref.extractall(f"{datafilesPath}{year}/")
      os.remove(path)
  os.rmdir(cachePath)

  metadataUrl = f"{baseurl}484"
  downloadFile(metadataUrl, f"{datafilesPath}metadata.xlsx")

def removeDatafiles():
  shutil.rmtree(datafilesPath)

if __name__ == "__main__":
  downloadData()
