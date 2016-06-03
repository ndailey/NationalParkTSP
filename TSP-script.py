# Author: Naomi Dailey
# Project: TSP National Parks Edition
# Date: 15 March 2016
# Purpose: script that accompanies ProjectManual.pdf instructions (use headers to follow along)


### Import modules and set directory

# note that some of these modules require install from command line (pip install)
import bs4, re, requests, json, os, csv
import matplotlib.pyplot as plt
import numpy as npy
import pandas as pd
from geojson import Feature, Point, FeatureCollection, LineString
from shapely.geometry import Point, mapping

# set working directory and results path to '/Dailey_FinalProject'
path = os.path.join(os.getcwd(), "Desktop/Dailey_FinalProject")
outpath = os.path.join(path, "Results")
if not os.path.exists(outpath): os.mkdir(outpath)

# moves the map .html document into your results folder
map_oldpath = os.path.join(path, "TSP_webmap.html")
map_newpath = os.path.join(outpath, "TSP_webmap.html")
os.rename(map_oldpath, map_newpath)


### Scrape via HTML tags

# write function to scrape HTML
def webScrapeAllHTML(myURL):
    page = requests.get(myURL)
    # imports the source code as text
    content = page.text 
    # create BeautifulSoup object to search the text by tags
    return (bs4.BeautifulSoup(content, 'lxml'))

# fetch URL from Wikipedia National Parks website
parks_url = 'https://en.wikipedia.org/wiki/List_of_national_parks_of_the_United_States'
soup = webScrapeAllHTML(parks_url)


### Create list of coordinates

# identify coordinates using the tags in the webScrapeAllHTML() output
html_coords = soup.find_all("span", "geo")

# extract coordinates from soup and cast to list
coords = []
for tag in html_coords:
    lat, lon = tag.text.strip().split(';') # pulls coordinates out
    lat, lon = float(lat), float(lon) # reformat to floats
    latlon = [lat, lon]
    coords.append(latlon) # create list of lat lon values


### Create list of names

# same as above, but identify names using tags in webScrapeAllHTML() output
html_names = soup.find_all('th', attrs = {'scope':'row'})

# extract names from soup and cast to list
names = []
for name in html_names:
    extract = name.text.strip()
    names.append(extract)


### Create coordinate dictionary from CSV

# operates under assumption that  sammple.csv is in the current working directory (path)
mycsv = 'sample.csv'
newcsv = 'sample_new.csv'
csvpath = os.path.join(path, mycsv) # set path to user's .csv

with open(csvpath, mode = 'r') as infile:
    reader = csv.reader(infile) # read the user's .csv
    with open(newcsv, mode = 'w') as outfile:
        writer = csv.writer(outfile)
        # compile .csv rows into dictionary using dictionary comprehension
        mydict = {rows[0]: [float(rows[1]), float(rows[2])] for rows in reader} 
print(mydict.keys())


### Build dictionary and delete unwanted parks

# NOTE: if you are using Option 2 (.csv method above) skip this step
# make a dictionary of names with associated coordinates
NPdict = dict(zip(names, coords))

# identify parks outside of contiguous US
keys_to_remove = []

# NOTE: the following 2 loops are not combined because we cannot change the size of the dictionary while iterating
for key in NPdict.keys():
    if (NPdict[key][1] < -130 or NPdict[key][1] > -65):
        keys_to_remove.append(key) # append those identified parks into a list

# delete unwanted parks that lie outside of contiguous US
for key in keys_to_remove:
    NPdict.pop(key, None)

# delete stragglers (island parks that fall within the bounding box)
del NPdict['Channel Islands']
del NPdict['Dry Tortugas']


### Cast dictionary to data frame

# make data frame from dictionary
dataframe = pd.DataFrame.from_dict(NPdict).T
dataframe.columns = ['Lat', 'Lon']
dataframe.head()


### Write distance function

# calculate geodesic distances for any set of lat lon values you have
# NOTE: this calculates Euclidean distance, not driving distance!!
def earthDistance(lat1, lon1, lat2, lon2, radius = 6378.388, unit_miles = False):

    """
    This equation computes distances between two points on Earth's surface specified by lat and lon.
    Assume Earth to be a perfect sphere with a given radius (default is 6378.388 km).
    Function can output miles or km (default is km).
    
    Reference
    ---------
    Adopted from John D. Cook's blog post: http://www.johndcook.com/blog/python_longitude_latitude/
    and from Mortada Mehyar's blog post: http://mortada.net/the-traveling-tesla-salesman.html
    """
    
    # convert lat and lon to spherical coordinates in radians
    deg_to_rad = npy.pi / 180.0
    
    # phi = 90 - lat
    phi1 = (90.0 - lat1) * deg_to_rad
    phi2 = (90.0 - lat2) * deg_to_rad
    
    # theta = longitude
    theta1 = lon1 * deg_to_rad
    theta2 = lon2 * deg_to_rad
    
    # compute spherical distance from converted coordinates
    cos = (npy.sin(phi1) * npy.sin(phi2) * npy.cos(theta1 - theta2) + npy.cos(phi1) * npy.cos(phi2))
    arc = npy.arccos(cos)
    length = arc * radius
    
    if (unit_miles == True):
        length = length/1.60934
    
    return length


### Use earthDistance() to calculate National Park distances

# make list of park names from dictionary to use in distance calculation
dictnames = list(NPdict.keys())
distances = {}

# calculate distances between each national park
for i in range(len(dictnames)): 
    
    # start point
    start = dictnames[i]
    distances[start] = {}
    
    for j in range(len(dictnames)):
        
        # stop point
        stop = dictnames[j]
        
        # the distance is 0 from a point to itself
        if j == i:
            distances[start][stop] = 0.
            
        # if the names are different, then the earthDistance() function is used
        elif j > i:
            
            # list names are used to index the lat lon values from the data frame
            distances[start][stop] = earthDistance(dataframe.ix[start, 'Lat'], dataframe.ix[start, 'Lon'], dataframe.ix[stop, 'Lat'], dataframe.ix[stop, 'Lon'], unit_miles = True)
        
        # ensures you don't compute the same distances twice
        else:
            distances[start][stop] = distances[stop][start]


### Create data frame of earthDistance() output

# save distances to new dataframe and view values (in miles)
distances = pd.DataFrame(distances)
distances.head()


### Create histograms from distances output

# data visualization of distance results
closestNP = distances[distances > 0].min()
cnp = closestNP.hist(bins = 10, color = 'green') # set bins
cnp.set_title('Histogram of Closest Distances Between National Parks') # set labels
cnp.set_ylabel('Number of National Parks')
cnp.set_xlabel('Miles')

furthestNP = distances[distances > 0].max()
fnp = furthestNP.hist(bins = 10, color = 'green')
fnp.set_title('Histogram of Furthest Distances Between National Parks')
fnp.set_ylabel('Number of National Parks')
fnp.set_xlabel('Miles')


### Write .tsp file for Concorde TSP solver

# NOTE: before running this section, must install QSOPT + Concorde (see: '/Dailey_FinalProject/README.pdf')
# write the coordinate values to a .tsp file to use in Concorde
node_id = 0
output = ''

# iterate over park names to make an array of ID, latitude and longitude values
for name in dictnames:
    output += '%d %f %f\n' % (node_id, dataframe.ix[name, 'Lat'], dataframe.ix[name, 'Lon'])
    node_id += 1

# format for .tsp file
header = """NAME : NP TSP
COMMENT : National Park TSP
TYPE : TSP
DIMENSION : %d
EDGE_WEIGHT_TYPE : GEOM
NODE_COORD_SECTION 
""" % (node_id)

# compile results into .tsp file
tspfile = os.path.join(outpath, 'nationalparks.tsp')
with open(tspfile, 'w') as output_file:
    output_file.write(header)
    output_file.write(output)


### Execute Concorde

# this is done in the terminal


### Parse the 'nationalparks.sol' file

# import the Concorde .sol file
solution_file = os.path.join(path, 'concorde/TSP/nationalparks.sol')

# parse the .sol file to get solutions
# solutions are a list of ID's that correspond to the order of national parks you would visit
solution = []
f = open(solution_file, 'r')
for line in f.readlines():
    tokens = line.split()
    solution += [int(c) for c in tokens] 
f.close()

# ensure the solution length is the same as the park names list length
assert solution[0] == len(dictnames)

# first number in solution is just the dimension (# of nodes), don't need it
solution = solution[1:] 

# check that lengths are the same
assert len(solution) == len(dictnames)


### Append solutions and check optimal path

# append solutions into a list
optimal_path = []
for solution_id in solution:
    optimal_path.append(dictnames[solution_id])
    
# make sure the path starts and ends at the same national park
optimal_path.append(dictnames[solution[0]])

# reformat into a series for cleaner visualization
optimal_path_series = pd.Series(optimal_path)

# check that the first and last national parks are the same
optimal_path_series.head()
optimal_path_series.tail()


### Calculate total route distance for optimal path

# find the total distance of the optimal path
total_dist = 0
for i in range(len(optimal_path) - 1):
    total_dist += distances.ix[optimal_path[i], optimal_path[i + 1]]
total_dist

# total distance should be 10959.222 miles


### Use for loop to extract coordinates and write to .json

# extract coordinates and names from the pandas dataframe
TSP_coords = []
for name in optimal_path:
    TSP_coords += [[dataframe.ix[name, 'Lon'], dataframe.ix[name, 'Lat'], name]]

#gjson will be the main dictionary converted to .json format
gjsonpoint_dict = {}
gjsonpoint_dict["type"] = "FeatureCollection"
feat_list = []

# loop through all points, building a list entry which is a dictionary
for coords in TSP_coords:
    # each of these dictionaries has within it nested a type dict, 
    # which contains a point dict and properties dict
    type_dict = {}
    point_dict = {}
    prop_dict = {}
    
    type_dict["type"] = "Feature"
    point_dict["type"] = "Point"
    type_dict["geometry"] = mapping(Point(coords[0],coords[1]))
    
    prop_dict["Name"] = coords[2]
    type_dict["properties"] = prop_dict
    feat_list.append(type_dict)
    
gjsonpoint_dict["features"] = feat_list

# write the resulting dictionary to a .json file that outputs in the Results folder
points_path = os.path.join(outpath, 'tsp_point.json')
with open(points_path, 'w') as outfile:
    json.dump(gjsonpoint_dict, outfile, sort_keys = True, indent = 4, ensure_ascii = False)  


### Use geojson module to extract coordinates and write to .json

# extract only coordinates as list of tuples from the pandas dataframe
coordinates = []
for name in optimal_path:
    coordinates += [(dataframe.ix[name, 'Lon'], dataframe.ix[name, 'Lat'])]

# use geojson LineString method to create .json polyline file
gjsonline_dict = LineString(coordinates)

# as above, write the result to a .json file that outputs in the Results folder
line_path = os.path.join(outpath, 'tsp_line.json')
with open(line_path, 'w') as outfile:
    json.dump(gjsonline_dict, outfile, sort_keys = True, indent = 4, ensure_ascii = False)