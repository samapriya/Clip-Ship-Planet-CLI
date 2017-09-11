import requests,json,re,csv,os,subprocess,urllib2,getpass
from pprint import pprint
from os.path import expanduser
from urllib2 import Request, urlopen

os.chdir(os.path.dirname(os.path.realpath(__file__)))
pkey=expanduser("~/.config/planet/pkey.csv")
f=open(pkey)
for row in csv.reader(f):
    #print(str(row).strip("[']"))
    PL_API_KEY=str(row).strip("[']")

CAS_URL='https://api.planet.com/compute/ops/clips/v1/'
headers = {'Content-Type': 'application/json',}
def idlist(aoi=None,item_asset=None):
    subprocess.call('python download.py --query '+aoi+' --checklist '+item_asset)
