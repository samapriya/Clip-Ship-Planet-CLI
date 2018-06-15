import requests,json,re,csv,os,subprocess,urllib2,getpass
from pprint import pprint
from os.path import expanduser
from urllib2 import Request, urlopen
from planet.api.utils import read_planet_json
os.chdir(os.path.dirname(os.path.realpath(__file__)))
planethome=os.path.dirname(os.path.realpath(__file__))
try:
        PL_API_KEY = read_planet_json()['key']
except:
        subprocess.call('planet init',shell=True)
CAS_URL='https://api.planet.com/compute/ops/clips/v1/'
headers = {'Content-Type': 'application/json',}
def idlist(aoi=None,item_asset=None):
    subprocess.call('python download.py --query '+aoi+' --checklist '+item_asset,shell=True)
