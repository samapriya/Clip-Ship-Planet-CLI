import requests,json,re,csv,os,subprocess,urllib2,getpass
from pprint import pprint
from os.path import expanduser
from urllib2 import Request, urlopen

planethome=expanduser("~/.config/planet/")
if not os.path.exists(planethome):
    os.mkdir(planethome)
    pkey=expanduser("~/.config/planet/pkey.csv")
    if not os.path.exists(pkey):
        print("Enter your Planet API Key")
        password=getpass.getpass()
        os.chdir(planethome)
        with open("pkey.csv",'w') as completed:
            writer=csv.writer(completed,delimiter=',',lineterminator='\n')
            writer.writerow([password])
pkey=expanduser("~/.config/planet/pkey.csv")
f=open(pkey)
for row in csv.reader(f):
    #print(str(row).strip("[']"))
    PL_API_KEY=str(row).strip("[']")
os.chdir(os.path.dirname(os.path.realpath(__file__)))
CAS_URL='https://api.planet.com/compute/ops/clips/v1/'
headers = {'Content-Type': 'application/json',}
def idlist(aoi=None,item_asset=None):
    subprocess.call('python download.py --query '+aoi+' --checklist '+item_asset,shell=True)
