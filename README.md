# Clip Ship Planet CLI addon

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1005752.svg)](https://doi.org/10.5281/zenodo.1005752)
[![Planet](https://img.shields.io/badge/SupportedBy%3A-Planet%20Ambassador%20Program-brightgreen.svg)](https://www.planet.com/products/education-and-research/)
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/samapriya)

Planet's Clip API was a compute API designed to allowed users to clip the images to their area of interest. This would save them time in preprocessing and also allow the user to save on their area quota which might have restrictions. Based on Planet's Education and Research Program this quota is set at 10,000 square kilometers a month, which means saving up on quota is very useful. The discussion also led to an important clarification that users are in fact charged only for the area downloaded post clip if using the clip operation and hence this tool. This tool takes a sequential approach from activation to generating a clip request for multiple images activated and then processing the download tokens to actually download the clipped image files. The tool also consists of a sort function which allows the user to extract the files and sort them by type and deleting the original files to save on space.

## Installation
To install the Clip-Ship-Planet-CLI you can simply perform the following action with Linux(Tested on Ubuntu 16):
```
git clone https://github.com/samapriya/Clip-Ship-Planet-CLI.git
cd Clip-Ship-Planet-CLI && pip install -r requirements.txt
```

On a windows as well as a linux machine, installation is an optional step; the application can also be run directly by executing pclip.py script. The advantage of having it installed is being able to execute ppipe as any command line tool. I recommend installation within virtual environment but you can also install it to system python and should not create any conflicts. To install on windows download the setup files as a zip package, unpack and run

```
python setup.py develop or python setup.py install
```

In a linux distribution
```
sudo python setup.py develop or sudo python setup.py install
pclip -h
```
![pclip-cli](https://i.imgur.com/bqds1Cm.jpg)

## Table of contents
* [Getting started](#getting-started)
* [Usage examples](#usage-examples)
	 * [Planet Key](#planet-key)
   * [AOI JSON](#aoi-json)
   * [Activate or Check Asset](#activate-or-check-asset)
	* [List IDs](#list-ids)
   * [Clipping with GeoJSON](#clipping-with-geojson)
   * [Clipping with JSON](#clipping-with-json)
   * [Downloading Clipped Imagery](#downloading-clipped-imagery)
	* [Sorting](#sorting)

## Getting started

As usual, to print help:
```
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



## Usage examples
The tools have been designed to follow a sequential setup from activation, clip, download and even sort and includes steps that help resolve additional issues a user might face trying to download clipped area of interests instead of entire scenes. The system will ask you to enter your API key before the CLI starts(this will prompt you only once to change API key use the Planet Key tool).

### Planet Key
This tool basically asks you to input your Planet API Key using a password prompt this is then used for all subsequent tools
```
usage: pclip planetkey [-h]

optional arguments:
  -h, --help  show this help message and exit
```
If using on a private machine the Key is saved as a csv file for all future runs of the tool.
 
### AOI JSON
The aoijson tab within the toolset allows you to create filters and structure your existing input file to that which can be used with Planet's API. The tool requires inputs with start and end date, along with cloud cover. You can choose from multiple input files types such as KML, Zipped Shapefile, GeoJSON, WKT or even Landsat Tiles based on PathRow numbers. The geo option asks you to select existing files which will be converted into formatted JSON file called aoi.json. If using WRS as an option just type in the 6 digit PathRow combination and it will create a json file for you.
```
usage: pclip aoijson [-h] [--start START] [--end END] [--cloud CLOUD]
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
As with the [Planet-GEE-Pipeline-CLI](https://github.com/samapriya/Planet-GEE-Pipeline-CLI) the aoijson tool allows the user to bring any filetype of interest, which includes GEOJSON, WKT, KML or SHP file including but not limited to WRS rowpath setup and structures it to enable filtered query using Planet's data API. A simple setup would be

```pclip aoijson --start "2017-06-01" --end "2017-12-31" --cloud "0.15" --inputfile "GJSON" --geo "C:\planet\myarea.geojson" --loc "C:\planet"```

the output is always named as aoi.json.

### Activate or Check Asset
The activate tool allows the users to either check or activate planet assets. This tool makes use of an existing json file sturctured for use within Planet API or the aoi.json file created earlier. This is a necessary step since the clip API can only work with those ID(s) which have been activated. In the future the list ID tool will check for number of activated id and wait for all of them to be activated before generating an ID list.

```
usage: pclip activate [-h] [--aoi AOI] [--action ACTION] [--asst ASST]

optional arguments:
  -h, --help       show this help message and exit
  --aoi AOI        Choose aoi.json file created earlier
  --action ACTION  choose between check/activate
  --asset ASST      Choose between planet asset types (PSOrthoTile
                   analytic/PSOrthoTile analytic_dn/PSOrthoTile
                   visual/PSScene4Band analytic/PSScene4Band
                   analytic_dn/PSScene3Band analytic/PSScene3Band
                   analytic_dn/PSScene3Band visual/REOrthoTile
                   analytic/REOrthoTile visual
```
An example setup for asset activation is the following

```pclip activate --aoi "C:\planet\aoi.json" --action "activate" --asset "PSOrthoTile analytic"```

### List IDs
The next step is to list ID(s) that you have activated, this creates a temporary file containing the list of ID(s) which can be used to iteratively call the clips API. This is a modification of the activation function to use only the item id instead of item type and asset id and write to file for future use.
```
usage: pclip idlist [-h] [--aoi AOI] [--asset ASSET]

optional arguments:
  -h, --help     show this help message and exit
  --aoi AOI      Input path to the structured json file from which we will
                 generate the clips
  --asset ASSET  Choose from asset type for example:"PSOrthoTile
                 analytic"|"REOrthoTile analytic"
```
The example setup for this command is the following

```pclip idlist --aoi “C:\planet\aoi.json” --asset “PSOrthoTile analytic”```


### Clipping with GeoJSON
A geejson file can be used directly to clip and query the area of interest and then submit clip process. I added this is a functionality but want to make clear that this does not take into consideration any other filters such as cloud cover or start and end date, and hence should be used only when you do not need to apply any filter.

```
usage: pclip geojsonc [-h] [--path PATH] [--item ITEM] [--asset ASSET]

optional arguments:
  -h, --help     show this help message and exit
  --path PATH    Path to the geojson file including filename (Example:
                 C:\users ile.geojson)
  --item ITEM    Choose from item type for example:"PSOrthoTile","REOrthoTile"
  --asset ASSET  Choose from asset type for example: "visual","analytic"
  ```
 A simple setup for the JSON tool is the following
 
```pclip geojsonc --path “C:\planet\aoi.geojson” --item “PSOrthoTile” --asset “analytic"```

### Clipping with JSON
This is the preferred style of submitting the clip requests using the IDlist we generated earlier. This is already structured before even activating assets and includes the additional filters you might have used for selecting the images.
```
usage: pclip jsonc [-h] [--path PATH] [--item ITEM] [--asset ASSET]

optional arguments:
  -h, --help     show this help message and exit
  --path PATH    Path to the json file including filename (Example: C:\users
                 ile.json)
  --item ITEM    Choose from item type for example:"PSOrthoTile","REOrthoTile"
  --asset ASSET  Choose from asset type for example: "visual","analytic"
  ```
A simple setup for the JSON tool is the following

```pclip jsonc --path “C:\planet\aoi.json” --item “PSOrthoTile” --asset “analytic"```

### Downloading Clipped Imagery
The last step includes providing a location where the clipped imagery can be downloaded. This includes the zip files that are generated from the earlier step and include a download token that expires over time. This batch downloads the clipped zip files to destination directory

```
usage: pclip downloadclips [-h] [--dir DIR]

optional arguments:
  -h, --help  show this help message and exit
  --dir DIR   Output directory to save the assets. All files are zipped and
              include metadata
```

A simple setup includes just the location to the download directory for the zipped & clipped files to be downloaded

```
pclip downloadclips --dir “C:\planet\zipped"
```

### Sorting
As an additional measure and because it makes arranging and handling datasets easily, this setup comes completed with a sort tool. If a output directory is provided for the unzipped files, the tool unzips all files, moves the images and metadata to seperate directories and then deletes the original zipped files to save space. 

```
usage: pclip sort [-h] [--zipped ZIPPED] [--unzipped UNZIPPED]

optional arguments:
  -h, --help           show this help message and exit
  --zipped ZIPPED      Folder containing downloaded clipped files which are
                       zipped
  --unzipped UNZIPPED  Folder where you want your files to be unzipped and
                       sorted
```

A simple would be the following (Images and metadata are sorted into an image and metadata folder inside the unzipped files folder)

```
pclip sort --zipped “C:\planet\zipped” --unzipped “C:\planet\unzipped”
```

## Changelog
### v0.2.1
- Thanks to commit suggested by [Rabscuttler](https://github.com/Rabscuttler)
- Fixed issues with help text and installer

### v0.2.0
- Fixed issues with config files

### v0.1.9
- Now handles running and succeeded status better
- Now enumerates during clip and download to allow user estimates on number of assets clipped and/or downloaded

### v0.1.8
- Includes required packages list within installer
- Robust GEOJSON Parsing

### v0.1.7
- Fixed issues with processing visual asset types
- The Clip function now handles error codes if the post response code is not 202(accepted for processing) then the error code and item and asset type is printed.

### v0.1.6
- Handles single time input API Key, this is needed only once to start the program
- Fixed issue with base metadata folder during sort
- Updated asset argument for asset activation to match styles

### v0.1.5
- Updated Requirements.txt to include pyshp
- Fixed subprocess shell error, for now shell=True

### v0.1.4
- General Improvements

### v0.1.3
- General Improvements

### v0.1.2
- Tested on Ubuntu 16.04 and now handles permissions problem
- Temporary files now written to config folders to avoid admin permission

### v0.1.1
- General Improvements
