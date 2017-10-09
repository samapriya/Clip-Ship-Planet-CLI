import requests,json,re,csv,os,subprocess,urllib2,getpass,time,progressbar
from pprint import pprint
from os.path import expanduser
from urllib2 import Request, urlopen

os.chdir(os.path.dirname(os.path.realpath(__file__)))
planethome=expanduser("~/.config/planet/")
pkey=expanduser("~/.config/planet/pkey.csv")
f=open(pkey)
for row in csv.reader(f):
    #print(str(row).strip("[']"))
    PL_API_KEY=str(row).strip("[']")

CAS_URL='https://api.planet.com/compute/ops/clips/v1/'
headers = {'Content-Type': 'application/json',}
if not os.path.exists(os.path.join(planethome,'urllist.csv')):
        with open(os.path.join(planethome,'urllist.csv'),'w') as completed:
            writer=csv.writer(completed,delimiter=',',lineterminator='\n')
with open(os.path.join(planethome,"urllist.csv")) as f:
    csv_f = csv.reader(f)
    value = len(list(csv_f))
def downloadclips(filepath=None):
    with open(os.path.join(planethome,"urllist.csv")) as f:
        csv_f = csv.reader(f)
        for i,row in enumerate(csv_f):
            URL=str(row).replace("'","").replace("[","").replace("]","")
            downlink = requests.get(url=URL, auth=(PL_API_KEY, ''))
            if downlink.status_code==200:
                content=downlink.json()
                item_id=(content['targets'][0]['item_id'])
                item_typ=(content['targets'][0]['item_type'])
                asset_typ=(content['targets'][0]['asset_type'])
                try:
                    if content['state']=='running':
                        while content['state']=='running':
                            bar = progressbar.ProgressBar()
                            for i in bar(range(60)):
                                time.sleep(1)
                            downlink = requests.get(url=URL, auth=(PL_API_KEY, ''))
                            if downlink.status_code==200:
                                content=downlink.json()
                    elif content['state']=='succeeded':
                        filelink = urllib2.urlopen(str(content['_links']['results'][0]))
                        filename=item_id+"_"+item_typ+"_"+asset_typ+".zip"
                        ov=os.path.join(filepath,filename)
                        if not os.path.exists(ov):
                            with open(ov, "wb") as code:
                                code.write(filelink.read())
                            print("Downloading: "+str(i+1)+" of "+str(value)+" "+(item_id+"_"+item_typ+"_"+asset_typ))
                        else:
                            print("asset exists..Skipping "+str(filename))

                    else:
                        print("Clip Function still " +content['state']+" "+str(filename))
                except Exception as e:
                    print e
            else:
                print("Got Download Return Error Code: "+str(downlink.status_code))
