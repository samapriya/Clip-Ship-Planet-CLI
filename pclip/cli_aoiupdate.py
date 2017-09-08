from datetime import date, timedelta
import os,csv
import time
os.chdir(os.path.dirname(os.path.realpath(__file__)))
def aoiupdate(indir=None,infile=None,days=None):
    if infile==None:
        inputfolder=indir
        n=days
        yesterday = date.today() - timedelta(int(n))
        b=yesterday.strftime('%Y-%m-%d')
        folder=inputfolder
        for filename in os.listdir(folder):
            if filename.endswith('.json'):
                infilename = os.path.join(folder,filename)
                fsp=filename.split("_x")[0]
                with open(infilename, 'r') as f:
                    inp=f.read()
                    a=inp.split('"field_name": "acquired", "config": {"gte":"')[1].split('T')[0]
                    replacement=inp.replace(a,str(b))
                    with open(infilename, 'w') as file:
                        file.write(replacement)
                    f.close()
                print("JSON Updated: "+fsp)
                subprocess.call("python slack_notifier.py botupdate --msg JSON Updated: "+'"'+str(fsp)+'"')
    else:
        with open(infile) as csvFile:
            inputfolder=indir
            n=days
            yesterday = date.today() - timedelta(int(n))
            b=yesterday.strftime('%Y-%m-%d')
            reader = csv.DictReader(csvFile)
            for row in reader:
                infilename=str(row["pathways"])
                with open(infilename, 'r') as f:
                    inp=f.read()
                    a=inp.split('"field_name": "acquired", "config": {"gte":"')[1].split('T')[0]
                    replacement=inp.replace(a,str(b))
                    with open(infilename, 'w') as file:
                        file.write(replacement)
                    f.close()
                print("JSON Updated: "+os.path.basename(infilename))
                subprocess.call("python slack_notifier.py botupdate --msg JSON Updated: "+'"'+str(os.path.basename(infilename))+'"')
        
