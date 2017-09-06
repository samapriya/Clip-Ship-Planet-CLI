# Clip Ship Planet CLI addon

## Installation
We assume Earth Engine Python API is installed and EE authorised as desribed [here](https://developers.google.com/earth-engine/python_install). We also assume Planet Python API is installed you can install by simply running.
```
pip install planet
```
Further instructions can be found [here](https://www.planet.com/docs/api-quickstart-examples/cli/) 

**This toolbox also uses some functionality from GDAL**
For installing GDAL in Ubuntu
```
sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
sudo apt-get install gdal-bin
```
For Windows I found this [guide](https://sandbox.idre.ucla.edu/sandbox/tutorials/installing-gdal-for-windows) from UCLA

To install **Planet-GEE-Pipeline-CLI:**
```
git clone https://github.com/samapriya/Planet-GEE-Pipeline-CLI.git
cd Planet-GEE-Pipeline-CLI && pip install .
```
This release also contains a windows installer which bypasses the need for you to have admin permission, it does however require you to have python in the system path meaning when you open up command prompt you should be able to type python and start it within the command prompt window. Post installation using the installer you can just call ppipe using the command prompt similar to calling python. Give it a go post installation type
```
ppipe -h
```
Installation is an optional step; the application can be also run directly by executing ppipe.py script. The advantage of having it installed is being able to execute ppipe as any command line tool. I recommend installation within virtual environment. To install run
```
python setup.py develop or python setup.py install

In a linux distribution
sudo python setup.py develop or sudo python setup.py install
```

## Getting started

As usual, to print help:
```
usage: pclip.py [-h]
                {
                ,planetkey,aoijson,activate,aoiupdate,idlist,geojsonc,jsonc,downloadclips,sort}
                ...

Planet Clip Tools CLI

positional arguments:
  { ,planetkey,aoijson,activate,aoiupdate,idlist,geojsonc,jsonc,downloadclips,sort}
                        -------------------------------------------
                        -----Choose from Planet Clip Tools-----
                        -------------------------------------------
    planetkey           Enter your planet API Key
    aoijson             Tool to convert KML, Shapefile,WKT,GeoJSON or Landsat
                        WRS PathRow file to AreaOfInterest.JSON file with
                        structured query for use with Planet API 1.0
    activate            Tool to query and/or activate Planet Assets
    aoiupdate           Allows users to batch update assets using a directory
                        with json or list of json(Sends updates on Slack if
                        slack key added)
    idlist              Allows users to generate an id list for the selected
                        item and asset type for example item_asset=
                        PSOrthoTile analytic/PSScene3Band visual. This is used
                        with the clip tool
    geojsonc            Allows users to batch submit clipping request to the
                        Planet Clip API using geometry in geojson file
    jsonc               Allows users to batch submit clipping request to the
                        Planet Clip API using geometry in structured json
                        file. This is preferred because the structured JSON
                        allows the activate tool to stream line asset ids
                        being requested and to extract geometry from the same
                        file
    downloadclips       Allows users to batch download clipped assets post
                        computation using a directory path(Requires you to
                        first activate and run geojson or json tool)
    sort                Allows users to unzip downloaded files to new folder
                        and sorts into images and metadata

optional arguments:
  -h, --help            show this help message and exit
```

To obtain help for a specific functionality, simply call it with _help_
switch, e.g.: `ppipe upload -h`. If you didn't install ppipe, then you
can run it just by going to _ppipe_ directory and running `python
ppipe.py [arguments go here]`


## Usage examples
Usage examples have been segmented into two parts focusing on both planet tools as well as earth engine tools, earth engine tools include additional developments in CLI which allows you to recursively interact with their python API

## Planet Tools
The Planet Toolsets consists of tools required to access control and download planet labs assets (PlanetScope and RapidEye OrthoTiles) as well as parse metadata in a tabular form which maybe required by other applications.

### Planet Key
This tool basically asks you to input your Planet API Key using a password prompt this is then used for all subsequent tools
```
usage: ppipe.py planetkey [-h]

optional arguments:
  -h, --help  show this help message and exit
```

If using on a private machine the Key is saved as a csv file for all future runs of the tool.
 
### AOI JSON
The aoijson tab within the toolset allows you to create filters and structure your existing input file to that which can be used with Planet's API. The tool requires inputs with start and end date, along with cloud cover. You can choose from multiple input files types such as KML, Zipped Shapefile, GeoJSON, WKT or even Landsat Tiles based on PathRow numbers. The geo option asks you to select existing files which will be converted into formatted JSON file called aoi.json. If using WRS as an option just type in the 6 digit PathRow combination and it will create a json file for you.
```
usage: ppipe.py aoijson [-h] [--start START] [--end END] [--cloud CLOUD]
                     [--inputfile INPUTFILE] [--geo GEO] [--loc LOC]

optional arguments:
  -h, --help            show this help message and exit
  --start START         Start date in YYYY-MM-DD?
  --end END             End date in YYYY-MM-DD?
  --cloud CLOUD         Maximum Cloud Cover(0-1) representing 0-100
  --inputfile INPUTFILE
                        Choose a kml/shapefile/geojson or WKT file for
                        AOI(KML/SHP/GJSON/WKT) or WRS (6 digit RowPath
                        Example: 023042)
  --geo GEO             map.geojson/aoi.kml/aoi.shp/aoi.wkt file
  --loc LOC             Location where aoi.json file is to be stored
```

### Activate or Check Asset
The activatepl tab allows the users to either check or activate planet assets, in this case only PSOrthoTile and REOrthoTile are supported because I was only interested in these two asset types for my work but can be easily extended to other asset types. This tool makes use of an existing json file sturctured for use within Planet API or the aoi.json file created earlier
```
usage: ppipe.py activatepl [-h] [--aoi AOI] [--action ACTION] [--asst ASST]

optional arguments:
  -h, --help       show this help message and exit
  --aoi AOI        Choose aoi.json file created earlier
  --action ACTION  choose between check/activate
  --asst ASST      Choose between planet asset types (PSOrthoTile
                   analytic/REOrthoTile analytic/PSOrthoTile
                   analytic_xml/REOrthoTile analytic_xml

```
