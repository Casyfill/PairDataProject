#!/usr/bin/env python
#-*- coding: utf-8 -*-

import json
from geojson import MultiLineString, LineString, Feature, FeatureCollection
import geojson
# MultiLineString([[(),()][(),()]])

def verifyGeoJson(Json):
	import requests
	validate_endpoint = 'http://geojsonlint.com/validate'
	request = requests.post(validate_endpoint, data=Json)
	
 
	if request.json()['status']!='ok':
		print 'geoJson is valid'
	else:
		print 'geoJson is not valid'


path = "/Users/casy/Dropbox/My_Projects/Coursera/Coursera_maps/2015_04_30_moves_export/geojson/full/activities.geojson"
rPath = "/Users/casy/Dropbox/My_Projects/Coursera/Coursera_maps/CourseProject/data/activities.geojson"

with open(path) as data_file:    
    data = json.load(data_file)

lineList = []

for feature in data['features']:
	date = feature['properties']["date"]
	for i in xrange(len(feature['geometry']['coordinates'])):
		geometry = LineString(feature['geometry']['coordinates'][i])

		activity = feature['properties']['activities'][i]
		properties= activity
		properties['date']=date
		lineList.append(Feature(geometry=geometry, properties=properties))


fCollection = FeatureCollection(lineList)
verifyGeoJson(fCollection)
# print len(fCollection['features'])
# print fCollection

with open(rPath,'w') as outFile:
	geojson.dump(fCollection, outFile, sort_keys=True)
