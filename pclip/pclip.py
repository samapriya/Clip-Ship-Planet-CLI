import requests,json,re,csv,os,subprocess,urllib2,argparse,getpass
from pprint import pprint
from os.path import expanduser
from urllib2 import Request, urlopen
from clip_idlist import idlist
from clip_geojson import geojsonc
from cli_aoi2json import aoijson
from clip_json import jsonc
from cli_aoiupdate import aoiupdate
from clip_download import downloadclips
from cli_sorter import sort
os.chdir(os.path.dirname(os.path.realpath(__file__)))
def planet_key_entry():
    planethome=expanduser("~/.config/planet/")
    if not os.path.exists(planethome):
        os.mkdir(planethome)
    print("Enter your Planet API Key")
    password=getpass.getpass()
    os.chdir(planethome)
    with open("pkey.csv",'w') as completed:
        writer=csv.writer(completed,delimiter=',',lineterminator='\n')
        writer.writerow([password])
def planet_key_from_parser(args):
    planet_key_entry()
def aoijson_from_parser(args):
    aoijson(start=args.start,end=args.end,cloud=args.cloud,inputfile=args.inputfile,geo=args.geo,loc=args.loc)
def activate_from_parser(args):
    aoi_json=str(args.aoi)
    action_planet=str(args.action)
    asset_type=str(args.asst)
    try:
        os.system("python download.py --query "+args.aoi+" --"+args.action+" "+asset_type)
    except Exception:
        print(' ')
def aoiupdate_from_parser(args):
    aoiupdate(indir=args.indir,
             days=args.days,
             infile=args.infile)
def idlist_from_parser(args):
    idlist(aoi=args.aoi,item_asset=args.asset)
def geojsonc_from_parser(args):
    geojsonc(path=args.path,item=args.item,asset=args.asset)
def jsonc_from_parser(args):
    jsonc(path=args.path,item=args.item,asset=args.asset)
def downloadclips_from_parser(args):
    downloadclips(filepath=args.dir)
def sort_from_parser(args):
    sort(zipped=args.zipped,unzipped=args.unzipped)

spacing="                               "
def main(args=None):
    parser = argparse.ArgumentParser(description='Planet Clip Tools CLI')

    subparsers = parser.add_subparsers()

    parser_pp3 = subparsers.add_parser(' ', help='-------------------------------------------')
    parser_P2 = subparsers.add_parser(' ', help='-----Choose from Planet Clip Tools-----')
    parser_pp4 = subparsers.add_parser(' ', help='-------------------------------------------')

    parser_planet_key = subparsers.add_parser('planetkey', help='Enter your planet API Key')
    parser_planet_key.set_defaults(func=planet_key_from_parser)

    parser_aoijson=subparsers.add_parser('aoijson',help='Tool to convert KML, Shapefile,WKT,GeoJSON or Landsat WRS PathRow file to AreaOfInterest.JSON file with structured query for use with Planet API 1.0')
    parser_aoijson.add_argument('--start', help='Start date in YYYY-MM-DD?')
    parser_aoijson.add_argument('--end', help='End date in YYYY-MM-DD?')
    parser_aoijson.add_argument('--cloud', help='Maximum Cloud Cover(0-1) representing 0-100')
    parser_aoijson.add_argument('--inputfile',help='Choose a kml/shapefile/geojson or WKT file for AOI(KML/SHP/GJSON/WKT) or WRS (6 digit RowPath Example: 023042)')
    parser_aoijson.add_argument('--geo', default='./map.geojson',help='map.geojson/aoi.kml/aoi.shp/aoi.wkt file')
    parser_aoijson.add_argument('--loc', help='Location where aoi.json file is to be stored')
    parser_aoijson.set_defaults(func=aoijson_from_parser)
    
    parser_activate=subparsers.add_parser('activate',help='Tool to query and/or activate Planet Assets')
    parser_activate.add_argument('--aoi', help='Choose aoi.json file created earlier')
    parser_activate.add_argument('--action', help='choose between check/activate')
    parser_activate.add_argument('--asst',help='Choose between planet asset types (PSOrthoTile analytic/PSOrthoTile analytic_dn/PSOrthoTile visual/PSScene4Band analytic/PSScene4Band analytic_dn/PSScene3Band analytic/PSScene3Band analytic_dn/PSScene3Band visual/REOrthoTile analytic/REOrthoTile visual')
    parser_activate.set_defaults(func=activate_from_parser)

    parser_aoiupdate = subparsers.add_parser('aoiupdate', help='Allows users to batch update assets using a directory with json or list of json(Sends updates on Slack if slack key added)')
    parser_aoiupdate.add_argument('--indir', help='Choose folder with aoi.json files',default=None)
    parser_aoiupdate.add_argument('--days', help='Choose the number of days before today as new start date for aoi',default=None)
    parser_aoiupdate.add_argument('--infile', help='File list with headers pathways:path to json file',default=None)
    parser_aoiupdate.set_defaults(func=aoiupdate_from_parser)

    parser_idlist = subparsers.add_parser('idlist', help='Allows users to generate an id list for the selected item and asset type for example item_asset= PSOrthoTile analytic/PSScene3Band visual. This is used with the clip tool')
    parser_idlist.add_argument('--aoi', help='Input path to the structured json file from which we will generate the clips',default=None)
    parser_idlist.add_argument('--asset', help='Choose from asset type for example:"PSOrthoTile analytic"|"REOrthoTile analytic"',default=None)
    parser_idlist.set_defaults(func=idlist_from_parser)

    parser_geojsonc = subparsers.add_parser('geojsonc', help='Allows users to batch submit clipping request to the Planet Clip API using geometry in geojson file')
    parser_geojsonc.add_argument('--path', help='Path to the geojson file including filename (Example: C:\users\file.geojson)',default=None)
    parser_geojsonc.add_argument('--item', help='Choose from item type for example:"PSOrthoTile","REOrthoTile"',default=None)
    parser_geojsonc.add_argument('--asset', help='Choose from asset type for example: "visual","analytic"',default=None)
    parser_geojsonc.set_defaults(func=geojsonc_from_parser)

    parser_jsonc = subparsers.add_parser('jsonc', help='Allows users to batch submit clipping request to the Planet Clip API using geometry in structured json file. This is preferred because the structured JSON allows the activate tool to stream line asset ids being requested and to extract geometry from the same file')
    parser_jsonc.add_argument('--path', help='Path to the json file including filename (Example: C:\users\file.json)',default=None)
    parser_jsonc.add_argument('--item', help='Choose from item type for example:"PSOrthoTile","REOrthoTile"',default=None)
    parser_jsonc.add_argument('--asset', help='Choose from asset type for example: "visual","analytic"',default=None)
    parser_jsonc.set_defaults(func=jsonc_from_parser)

    parser_downloadclips = subparsers.add_parser('downloadclips', help='Allows users to batch download clipped assets post computation using a directory path(Requires you to first activate and run geojson or json tool)')
    parser_downloadclips.add_argument('--dir', help='Output directory to save the assets. All files are zipped and include metadata',default=None)
    parser_downloadclips.set_defaults(func=downloadclips_from_parser)

    parser_sort = subparsers.add_parser('sort', help='Allows users to unzip downloaded files to new folder and sorts into images and metadata')
    parser_sort.add_argument('--zipped', help='Folder containing downloaded clipped files which are zipped',default=None)
    parser_sort.add_argument('--unzipped', help='Folder where you want your files to be unzipped and sorted',default=None)
    parser_sort.set_defaults(func=sort_from_parser)

    args = parser.parse_args()

    args.func(args)

if __name__ == '__main__':
    main()
