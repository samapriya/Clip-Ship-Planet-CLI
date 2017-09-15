import os,shutil,zipfile,subprocess
os.chdir(os.path.dirname(os.path.realpath(__file__)))
def sort(zipped,unzipped):
    if not os.path.exists(os.path.join(unzipped,"images")):
        os.mkdir(os.path.join(unzipped,"images"))
    if not os.path.exists(os.path.join(unzipped,"metadata")):
        os.mkdir(os.path.join(unzipped,"metadata"))
    ziplist=os.listdir(zipped)
    for zipfiles in ziplist:
        file_name = os.path.join(zipped,zipfiles) # get full path of files
        zip_ref = zipfile.ZipFile(file_name) # create zipfile object
        zip_ref.extractall(unzipped) # extract file to dir
        zip_ref.close() # close file
        print("Unzipping "+file_name)
    filelist=os.listdir(unzipped)
    for files in filelist:
        if files.endswith(".tif"):
            baseimage=os.path.basename(files)
            shutil.move(os.path.join(unzipped,files), os.path.join(unzipped,"images"))
            print("Moving "+baseimage)
        if files.endswith(".xml"):
            basemeta=os.path.basename(files)
            shutil.move(os.path.join(unzipped,files), os.path.join(unzipped,"metadata"))
            print("Moving "+basemeta)
    for zipfiles in ziplist:
        if zipfiles.endswith(".zip"):
            print("Deleting "+str(zipfiles))
            os.unlink(os.path.join(zipped,zipfiles))
