import requests,json,re,csv,os,subprocess,urllib2,getpass
from pprint import pprint
from os.path import expanduser
from urllib2 import Request, urlopen

os.chdir(os.path.dirname(os.path.realpath(__file__)))
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
    f=open(pkey)
    for row in csv.reader(f):
        #print(str(row).strip("[']"))
        os.environ['PLANET_API_KEY']=str(row).strip("[']")

CAS_URL='https://api.planet.com/compute/ops/clips/v1/'
headers = {'Content-Type': 'application/json',}

def downloadclips(filepath=None):
    with open("urllist.csv") as f:
        csv_f = csv.reader(f)
        for row in csv_f:
            URL=str(row).replace("'","").replace("[","").replace("]","")
            downlink = requests.get(url=URL, auth=(PL_API_KEY, ''))
            content=downlink.json()
            item_id=(content['targets'][0]['item_id'])
            item_typ=(content['targets'][0]['item_type'])
            asset_typ=(content['targets'][0]['asset_type'])
            try:
                if content['state']=='succeeded':
                    filelink = urllib2.urlopen(str(content['_links']['results'][0]))
                    filename=item_id+"_"+item_typ+"_"+asset_typ+".zip"
                    ov=os.path.join(filepath,filename)
                    if not os.path.exists(ov):
                        with open(ov, "wb") as code:
                            code.write(filelink.read())
                        print("Downloading: "+(item_id+"_"+item_typ+"_"+asset_typ))
                    else:
                        print("asset exists..Skipping "+str(filename))
                else:
                    print(content['state'])
            except:
                print("All successful links have been clipped and downloaded")
