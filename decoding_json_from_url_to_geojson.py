#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import urllib2
import json
import csv
import pprint
pp = pprint.PrettyPrinter(indent=4)
import sys

# csv_path  = '/Users/casy/Dropbox/My_Projects/PairDataProject/data/philipp2.csv'
out_path = '/Users/casy/Dropbox/My_Projects/PairDataProject/mapping_part/Philipp_total_movements.json'


def parseJsonToString(j):
	# print j
	data = json.loads(j)[0]
	date = data['date']
	movements = data['segments']
	moves = []
	for m in movements:
		if m['type']=='move':
			move = {}
			move['date'] = str(date)
			move['type'] = str(m['activities'][0]['activity'])
			move['distance'] = str(m['activities'][0]['distance'])
			move['duration'] = str(m['activities'][0]['duration'])
			move['endTime'] = str(m['activities'][0]['endTime'])
			move['startTime'] = str(m['activities'][0]['startTime'])
			move['trackPoints'] = ''
			for point in m['activities'][0]['trackPoints']:
				move['trackPoints']+= (',' + str(point['lat']) + ';' + str(point['lon']))
			move['trackPoints'] = move['trackPoints'][1:]
			moveString = str('|'.join(move.values()) + '\n')
			moves.append(moveString)	
	return moves


def parseJson(j):
	# print j
	data = json.loads(j)[0]
	date = data['date']
	movements = data['segments']
	feats = []

	if movements == None:
		# print 'lazy Day!'
		# pp.pprint(data)
		return
	else:	
		for m in movements:
			if m['type']=='move':
				prop = {
					'date': date,
					'type' : m['activities'][0]['activity'],
					'distance' : m['activities'][0]['distance'],
					'duration' : m['activities'][0]['duration'],
					'endTime' : m['activities'][0]['endTime'],
					'startTime' : m['activities'][0]['startTime'],
					}
				LongLatList = []
				for point in m['activities'][0]['trackPoints']:
					LongLatList.append([point['lon'] ,point['lat']])
			# print len(LongLatList)
			
				Feature={
					'type': 'Feature',
					'geometry': {
        				'type': 'LineString',
        				'coordinates': LongLatList
    				},
    				'properties': prop #'n/a'#
    				}	
			
				feats.append(Feature)	
	return feats



def parseJsonPlaces(j):
	# print j
	data = json.loads(j)[0]
	date = data['date']
	movements = data['segments']
	feats = []

	if movements == None:
		# print 'lazy Day!'
		# pp.pprint(data)
		return
	else:	
		for m in movements:
			if m['type']=='place':
				# pp.pprint(m)
				try: 
					foursquareId = m['place']['foursquareId']
				except:
					foursquareId = None
				prop = {
					'date': date,
					'type': 'place',
					'id' : m['place']['id'],
					'foursquareId' : foursquareId,
					'location' : m['place'][0]['location'],
					'pType' : m['place'][0]['type'],
					'name' : m['place'][0]['name'],
					'duration' : m['activities'][0]['duration'],
					'endTime' : m['activities'][0]['endTime'],
					'startTime' : m['activities'][0]['startTime'],
					}
				print prop['name']
	# 			LongLatList = []
	# 			for point in m['activities'][0]['trackPoints']:
	# 				LongLatList.append([point['lon'] ,point['lat']])
	# 		# print len(LongLatList)
			
	# 			Feature={
	# 				'type': 'Feature',
	# 				'geometry': {
 #        				'type': 'LineString',
 #        				'coordinates': LongLatList
 #    				},
 #    				'properties': prop #'n/a'#
 #    				}	
			
	# 			feats.append(Feature)	
	# return feats


def totalFeatures(List):
	allFeats = []
	# rows.append('distance|trackPoints|startTime|duration|endTime|date|type\n')
	for story in List:
		temp = parseJsonPlaces(story['PhilippStoryString'])
	# 	if temp!=None:
	# 		allFeats.extend(temp)

	# return allFeats


def verifyGeoJson(Json):
	import requests
	validate_endpoint = 'http://geojsonlint.com/validate'
	request = requests.post(validate_endpoint, data=Json)
	return request



anna = 'https://premium.scraperwiki.com/eoypwpi/69446f906b4c40f/sql/?q=select%0A%20--%20%20%20%20Time%2C%0A%09--%20Ncyc%2C%0A%20--%20%20%20%20Nwlk%2C%0A%20--%20%20%20%20Nrun%2C%0A%20--%20%20%20%20Ntrs%2C%0A%09--%20NplaceCOunt%2C%0A%20--%20%20%20%20Pcyc%2C%0A%20--%20%20%20%20Pwlk%2C%0A%20--%20%20%20%20Prun%2C%0A%20--%20%20%20%20Ptrs%2C%0A%20--%20%20%20%20PplaceCount%2C%0A%20%20%20%20NuraStoryString%0A%20%20%20%20%0Afrom%20swdata%0A--%20where%20NplaceCOunt%20%3E%20%0Aorder%20by%20Time%20DESC%0A--%20limit%202'
philipp = 'https://premium.scraperwiki.com/eoypwpi/69446f906b4c40f/sql/?q=select%0A%20%20%20%20PhilippStoryString%0A%20%20%20%20%0Afrom%20swdata%0A--%20where%20NplaceCOunt%20%3E%20%0Aorder%20by%20Time%20DESC%0A--%20limit%202'
# person = 'PhilippStoryString'



print 'script started!'

response = urllib2.urlopen(philipp)
Answer = response.read()
d = json.loads(Answer)
print 'parsing - done'


result = totalFeatures(d)
# features = {
#     'type': 'FeatureCollection',
#     'features': result,
# }

# geo_str = json.dumps(features,  indent=4, sort_keys=True)
# print verifyGeoJson(geo_str)

# with open(out_path, 'w') as file:
#     file.writelines(geo_str)
#     file.close()
#     print 'file ', out_path.split('/')[-1],  ' written!,'
#     print 'done!'
