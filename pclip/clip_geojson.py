import requests,json,re,csv,os,subprocess,urllib2,getpass
from pprint import pprint
from os.path import expanduser
from urllib2 import Request, urlopen
from os.path import expanduser
os.chdir(os.path.dirname(os.path.realpath(__file__)))
planethome=expanduser("~/.config/planet/")
pkey=expanduser("~/.config/planet/pkey.csv")
f=open(pkey)
for row in csv.reader(f):
    #print(str(row).strip("[']"))
    PL_API_KEY=str(row).strip("[']")

CAS_URL='https://api.planet.com/compute/ops/clips/v1/'
headers = {'Content-Type': 'application/json',}
def geojsonc(path=None,item=None,asset=None):
    with open(path) as f, open(os.path.join(planethome,"idl.csv"),'r') as f2,open(os.path.join(planethome,"urllist.csv"),'wb') as csvfile:
        geomloader = json.load(f)
        geom=geomloader['features'][0]['geometry']
        reader = csv.DictReader(f2)
        writer=csv.DictWriter(csvfile,fieldnames=["url"], delimiter=',')
        writer.writeheader()
        for i, line in enumerate(reader):
            item_id = line['id_no']
            data = r'{"aoi": '+str(geom)+r',"targets": [{"item_id": '+'"'+item_id+'"'+r',"item_type": '+'"'+item+'"'+r',"asset_type": '+'"'+asset+'"'+r'}]}'
            data2=str(data).replace("'",'"').replace('u"','"')
            main=requests.post('https://api.planet.com/compute/ops/clips/v1/', headers=headers, data=data2, auth=(PL_API_KEY, ''))
            if main.status_code==202:
                URL=str(main.json()).split('_self')[1].split(',')[0].replace("': u","").replace(" ","").replace("'","")
                content=main.json()
                item_id=(content['targets'][0]['item_id'])
                item_typ=(content['targets'][0]['item_type'])
                asset_typ=(content['targets'][0]['asset_type'])
                print("Clipping: "+(item_id+"_"+item_typ+"_"+asset_typ))
                with open(os.path.join(planethome,"urllist.csv"),'a') as csvfile:
                    writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                    writer.writerow([URL])
            elif main.status_code==429:
                time.sleep(2)
                URL=str(main.json()).split('_self')[1].split(',')[0].replace("': u","").replace(" ","").replace("'","")
                content=main.json()
                item_id=(content['targets'][0]['item_id'])
                item_typ=(content['targets'][0]['item_type'])
                asset_typ=(content['targets'][0]['asset_type'])
                print("Clipping: "+(item_id+"_"+item_typ+"_"+asset_typ))
                with open(os.path.join(planethome,"urllist.csv"),'a') as csvfile:
                    writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                    writer.writerow([URL])
            else:
                print("Issues with: "+(item_id+"_"+item+"_"+asset)+" has error code "+str(main.status_code))
