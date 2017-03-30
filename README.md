NCATS RePORTER Map Project 
by Stephan Forden
==========================

The goal of this project is to create an interactive map that visualizes NIH's RePORTER data. Much of the map's functionality and interactivity is still to be implemented by whomever continues to work on this. This readme will detail what has been accomplished so far in July and August 2014, and what features still need to or could be developed.

report.py contains two functions:
Getjson() parses a RePORTER xml file, creates an object containing the reporter project data, and converts that object into a geojson file format that will constitute map data.
Getsize() checks to see how many calls to the google geocoding API would be made by each reporter file. That data is found in api_calls.txt. No more than 2500 calls/24h and 10 calls/s can be made using the free API.

Getgeo() in geocode.py takes a formatted address as a parameter, makes a call to the google geocoding API, parses its output for coordinates, and returns those coordinates.

Re_149.json is the resulting data from a corresponding RePORTER file that will be imported to CartoDB or another mapmaking platform. Note again that it is structured according to the geojson file format. You can read about this format in the appended links.

The CartoDB interface uses a combination of SQL, CSS, and a few UI tools. There are plenty of tutorials in the links below that are helpful.

Lastly, an embeddable, standalone, final version of this map will likely be the product of HTML, JavaScript, SQL, CSS, and their respective CartoDB libraries. More information on those are again detailed in links below. 
I have created a simple map visualization in Re_viz.html using some of CartoDB's tutorials.


TO DO and IDEAS
---------------

- Structure data so that projects and project data are subordinate to individual organizations. Right now, when you click on a map point, only one project is visible because others in that organization are hidden underneath that point. (SQL or Python)
- Implement search bar (JS + SQL)
- I have omitted the project terms from the data for now, because cartoDB won't accept columns with that much data. Create a structure that includes project terms that cartoDB will be able to handle.
- Interactive infowindows. (Click on org in map -> infowindow with ICs -> click on IC -> list of projects under that IC-> click on project-> info on proj)
- Cool/simple visualisations and interactivity (e.g. animated lines connecting projects that have common IC or project terms) 
- Classify projects based on budget, and visualize accordingly (e.g. appended pdf link)
---

MAPS for REFERENCE
http://ngoaidmap.org/
http://www.afdc.energy.gov/locator/stations/


RELEVANT DOCUMENTS AND TUTORIALS
--------------------------------

RePORTER DATA
	http://exporter.nih.gov/ExPORTER_Catalog.aspx
  
GOOGLE GEOCODE API
  https://developers.google.com/maps/documentation/geocoding/
  
GEOJSON
	http://geojson.org/geojson-spec.html
  
CARTODB
	http://www.cartodb.com
	http://docs.cartodb.com/tutorials.html
  
SQL
	http://www.postgresql.org/docs/9.1/static/
	http://postgis.net/docs/manual-2.0/
  
CARTODB LIBRARIES
	http://docs.cartodb.com/cartodb-platform.html
  
HEAD/TAIL BREAKS DATA CLASSIFICATION
	http://arxiv.org/ftp/arxiv/papers/1209/1209.2801.pdf

