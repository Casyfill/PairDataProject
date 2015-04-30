#!/usr/bin/env python
#-*- coding: utf-8 -*-

import json
from geojson import Point, Feature, FeatureCollection
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


path = "/Users/casy/Dropbox/My_Projects/Coursera/Coursera_maps/2015_04_30_moves_export/geojson/full/places.geojson"
rPath = "/Users/casy/Dropbox/My_Projects/Coursera/Coursera_maps/CourseProject/data/places.geojson"

with open(path) as data_file:    
    data = json.load(data_file)

places = {}

for feature in data['features']:
	ID = feature['properties']['place']['id'] 
	# date = feature['properties']["date"]
	if ID in places.keys():
		places[ID]['properties']['count']+=1
	else:
		geometry =  Point(feature['geometry']['coordinates'])

		x = feature['properties']['place']
		properties = {'id':x['id'], 'count':1,'type':x['type']}
		if 'name' in x.keys():
			properties['name']=x['name']

		if x['type']=='foursquare':
			if 'foursquareId'in x.keys():
				properties['foursquareId']=x['foursquareId']
			if 'foursquareCategoryIds'in x.keys():
				properties['foursquareCategoryIds']=x['foursquareCategoryIds']

		places[ID]=Feature(geometry=geometry, properties=properties)


fCollection = FeatureCollection(places.values())
verifyGeoJson(fCollection)
# print len(fCollection['features'])
# print fCollection

with open(rPath,'w') as outFile:
	geojson.dump(fCollection, outFile, sort_keys=True)
