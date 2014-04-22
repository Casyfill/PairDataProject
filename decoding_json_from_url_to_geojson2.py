#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import urllib2
import json
import csv
# import pprint
# pp = pprint.PrettyPrinter(indent=4)
import sys
import cProfile
# cProfile.run('foo()')

'''
 суммировать точки!!!! - done
 все в def's - done
 4sqr_places_stats - done
 cities = done
 venueStats - done
 вытащить 4sqr в allFeats из функций (упростить) - done
 заменить URL requests??

 в категориях и суммации - генераторы
 summation - починить и упростить
 profiler
 filter bad movements
 more filters_collectors - для "опозданий на работу, например"
 
 personal_analytics
 define sleeping
 define workPlace
 define weekend_Place

 define favorite
 define favoriteFood

'''
# чтобы не светить пароли в гите
def getAcces():
	path = "/Users/casy/Dropbox (RN&IA'N)/My_Projects/PairDataProject/code/4sqr_access_token.txt"
	with open(path, 'r') as file:
		frsqrAcess=file.read().strip()
		return frsqrAcess
		file.close()


frsqrAcess1= getAcces()
# version = 4

def collectData(person, Type, frsqrAcess):
	version = 5
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

	def totalMoves(List, person):
		if person == 'anna':
			ps = 'NuraStoryString'
		elif person == 'philipp':
			ps = 'PhilippStoryString'
		
		def parseMoves(j):


			# print j
			def ifWeekend(date):
				import time
				wday= time.strptime(date, "%Y%m%d").tm_wday
				if wday>=5:
					return True
				else :
					return False


			data = json.loads(j)[0]
			date = data['date']
			weekend = ifWeekend(date)


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
							'weekend': weekend,
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

		allFeats = []
		# rows.append('distance|trackPoints|startTime|duration|endTime|date|type\n')
		for story in List:
			temp = parseMoves(story[ps])
			if temp!=None:
				allFeats.extend(temp)
		print 'Всего перемещений: ', len(allFeats)
		return allFeats

	def totalPlaces(List, person, frsqrAcess):
		if person == 'anna':
			ps = 'NuraStoryString'
		elif person == 'philipp':
			ps = 'PhilippStoryString'

		def frsqrStatAll(List, acces_tocken):
					url = 'https://api.foursquare.com/v2/venues/categories?oauth_token=%s&v=20140416' % (acces_tocken)
					catResponse = urllib2.urlopen(url)
					Answer = catResponse.read()
					catJson = json.loads(Answer)
					print 'all cats scraped from 4sqr site!'

					catStrings = {}
					for cat in catJson['response']['categories']:
						catStrings[cat['name']] = json.dumps(cat,  indent=4 )
						# print cat['name'], ':::', catStrings[cat['name']]

					# return catJson
					for key in catStrings.keys():
						print key

					def frsqrStat(place, acces_tocken, catStrings):
						ID = place['properties']['foursquareId']
						url = 'https://api.foursquare.com/v2/venues/%s?oauth_token=%s&v=20140416' % (ID, acces_tocken)
						fsqrResponse = urllib2.urlopen(url)
						Answer = fsqrResponse.read()
						venueJson = json.loads(Answer)
						
						try:
							place['properties']['city'] = venueJson['response']['venue']['location']['city']
							
						except:
							place['properties']['city'] = None

						try:
							place['properties']['country'] = venueJson['response']['venue']['location']['country']
						except:
							place['properties']['country'] = None


						try:
							place['properties']['state'] = venueJson['response']['venue']['location']['state']
						except:
							place['properties']['state'] = None

						categoryID = venueJson['response']['venue']['categories'][0]['id']
						place['properties']['categoryName'] = venueJson['response']['venue']['categories'][0]['name']		

						def defMainCat(categoryID, catStrings):
							mainCat = None

							for key in catStrings.keys():
								if categoryID in catStrings[key]:
									mainCat = key
									break

							if mainCat==None:
								print categoryID, ' did not found category :('

							return mainCat
							 		
						
						place['properties']['MainName'] = defMainCat(categoryID,catStrings)

						return place

					for place in List:
						if place['properties']['foursquareId']!=None:
							place = frsqrStat(place, acces_tocken, catJson)
					return List


		def parsePlaces(j, pList):
			# print len(pList)
			idList = [x['properties']['id'] for x in pList]


			data = json.loads(j)[0]
			date = data['date']
			movements = data['segments']

			if movements == None:
				# print 'lazy Day!'
				# pp.pprint(data)
				pass
			else:	
				for m in movements:
					if m['type']=='place':

						ID = m['place']['id']
						if ID not in idList:


							try: 
								foursquareId = m['place']['foursquareId']
							except:
								foursquareId = None


							try: 
								name = m['place']['name']
							except:
								name = 'unknown'
						


							prop = {
								# 'date': [date],
								'type': 'place',
								'id' : m['place']['id'],
								'foursquareId' : foursquareId,
								'pType' : m['place']['type'],
								'name' : name,

								'amoung' : 1
							# 'duration' : (int(m['endTime'])-int(m['startTime'])),
							# 'endTime' : m['endTime'],
							# 'startTime' : m['startTime']
								}
							# print prop['name']
						
							lat =  m['place']['location']['lat']
							lon =  m['place']['location']['lon']
							Location = [lon, lat]

							Feature={
								'type': 'Feature',
								'geometry': {
		        					'type': 'Point',
		        					'coordinates': Location
		    					},
		    					'properties': prop #'n/a'#
		    					}	
							pList.append(Feature)	
							idList.append(ID)
						else:
							pList[idList.index(ID)]['properties']['amoung']+=1

			return pList

		allFeats = []
		for story in List:
			allFeats = parsePlaces( story[ps], allFeats)
		

		#  getting data from 4sqr
		allFeats = frsqrStatAll(allFeats, frsqrAcess)
		print 'Всего мест: ',len(allFeats)
		return allFeats

	def verifyGeoJson(Json):
		import requests
		validate_endpoint = 'http://geojsonlint.com/validate'
		request = requests.post(validate_endpoint, data=Json)
		return request.json()


	if person == 'anna':
		url = 'https://premium.scraperwiki.com/eoypwpi/69446f906b4c40f/sql/?q=select%0A%20--%20%20%20%20Time%2C%0A%09--%20Ncyc%2C%0A%20--%20%20%20%20Nwlk%2C%0A%20--%20%20%20%20Nrun%2C%0A%20--%20%20%20%20Ntrs%2C%0A%09--%20NplaceCOunt%2C%0A%20--%20%20%20%20Pcyc%2C%0A%20--%20%20%20%20Pwlk%2C%0A%20--%20%20%20%20Prun%2C%0A%20--%20%20%20%20Ptrs%2C%0A%20--%20%20%20%20PplaceCount%2C%0A%20%20%20%20NuraStoryString%0A%20%20%20%20%0Afrom%20swdata%0A--%20where%20NplaceCOunt%20%3E%20%0Aorder%20by%20Time%20DESC%0A--%20limit%202'
	elif person == 'philipp':
		url = 'https://premium.scraperwiki.com/eoypwpi/69446f906b4c40f/sql/?q=select%0A%20%20%20%20PhilippStoryString%0A%20%20%20%20%0Afrom%20swdata%0A--%20where%20NplaceCOunt%20%3E%20%0Aorder%20by%20Time%20DESC%0A--%20limit%202' 
	out_path = '/Users/casy/Dropbox/My_Projects/PairDataProject/mapping_part/' + person + '_' + Type + str(version) +'.json' 

	print 'script started!'

	response = urllib2.urlopen(url)
	Answer = response.read()
	d = json.loads(Answer)
	print 'parsing - done'
	# pp.pprint(json.loads(d[0]['PhilippStoryString']))

	if Type == 'movements':
		result = totalMoves(d, person)
	elif Type == 'places':
		result = totalPlaces(d, person, frsqrAcess)

	features = {
	    'type': 'FeatureCollection',
	    'features': result,
	}

	geo_str = json.dumps(features,  indent=4, sort_keys=True)
	# pp.pprint(geo_str)

	if verifyGeoJson(geo_str)['status']!='ok':
		print verifyGeoJson(geo_str)
	else:
		with open(out_path, 'w') as file:
			file.writelines(geo_str)
    		file.close()
    		print 'file ' + out_path.split('/')[-1] +  ' written!'


cProfile.run("collectData('philipp', 'places', frsqrAcess1)")
# collectData('philipp', 'places', frsqrAcess1)