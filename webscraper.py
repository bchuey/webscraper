#!/usr/local/bin/python3

import csv
import urllib
import urllib.parse
import urllib.request
import html5lib						
import re

from bs4 import BeautifulSoup

user_query_input = input('Type your search query: ')										# Allow user to type a search query (python3 => input())
																						
user_location_input = input('Type your search location: ')									# Allow user to type a query for location

search_query = user_query_input																# Grab value of user_query_input and assign it to search_query; replace any 'space' with '+'
search_location = user_location_input														# Grab value of user_location_input and assign it to search_location; replace any 'space' with '+'

urls_to_scrape_list = []																	# create empty list to store urls
page_two_url_list = []
all_business_info = []																		# create empty list to store business info dictionary

base_url = 'http://www.yelp.com'															# main url
search_url = base_url + '/search?'															# url foundation to use with search queries

query_dictionary = {'find_desc':search_query,'find_loc':search_location}					# Create empty dictionary for key:value pairs for parameters
params = urllib.parse.urlencode(query_dictionary)											# encode the dictionary
crawl_page_url = search_url + params														# append parameters to search_url

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}

req = urllib.request.Request(crawl_page_url, headers=headers)

page = urllib.request.urlopen(req)												# open url

soup = BeautifulSoup(page.read(), "html5lib")												# read the HTML tree

for link in soup.find_all('a',{'class':'biz-name'}):										# go through HTML tree and find all <a class="biz-name"> elements
	biz_name_url = link.get('href')															# grab the href value of each <a> element
	url_to_scrape = base_url + biz_name_url													# append the href value to the base_url
	urls_to_scrape_list.append(url_to_scrape)												# add each new url to a list called 'urls_to_scrape_list'

for link in soup.find_all('a',{'class':'pagination-links_anchor'}):
	next_page = link.get('href')
	url_to_open = base_url + next_page
	page_two_url_list.append(url_to_open)

for url in page_two_url_list[:-1]:

	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page.read(), "html5lib")
	for link in soup.find_all('a',{'class':'biz-name'}):
		biz_name_url = link.get('href')
		url_to_scrape = base_url + biz_name_url
		urls_to_scrape_list.append(url_to_scrape)


for url in urls_to_scrape_list[1:]:																

	yelp_url = url

	page = urllib.request.urlopen(url)															# request and open url

	soup = BeautifulSoup(page.read(), "html5lib")															# read the HTML structured tree

	try:
		business_name = soup.find('h1',{'class':'biz-page-title','itemprop':'name'}).get_text()	# find the name element and grab text
		business_name = business_name.strip()
	except (AttributeError):
		business_name = None

	try:

		BUSINESS_URL_REGEX = r'[w]{3}.\w+.[a-z]{3}'
		pattern = re.compile(BUSINESS_URL_REGEX)

		business_url = soup.find('div',{'class':'biz-website'})									# find div with class name 'biz-website'
		business_url = business_url.find('a')['href']											# find the href value of the <a> tag within 'biz-website' <div>
		# business_url = re.findall(r'%2F..*com', business_url)									# within href, find the string matching regular expression
																								# create a new regex matching string

		result = pattern.search(business_url)
		business_url = result.group(0)

		# try:
		# 	business_url = business_url[0]														# grab the web url from the list
		# 	business_url = business_url.lstrip('%2F')											# strip off extra part of matched string			
		# except (AttributeError, IndexError):
		# 	pass

	except (AttributeError):
		business_url = None

	try:
		streetAddress = soup.find('span',{'itemprop':'streetAddress'}).get_text()				# find the street address element and grab text
	except (AttributeError):
		streetAddress = None

	try:	
		addressLocality = soup.find('span',{'itemprop':'addressLocality'}).get_text()			# find the address locality element and grab text
	except (AttributeError):
		addressLocality = None

	try:
		addressRegion = soup.find('span',{'itemprop':'addressRegion'}).get_text()				# find the address region element and grab text
	except (AttributeError):
		addressRegion = None

	try:
		postalCode = soup.find('span',{'itemprop':'postalCode'}).get_text()						# find the postal code element and grab text
	except (AttributeError):
		postalCode = None

	try:
		telephone = soup.find('span',{'class':'biz-phone','itemprop':'telephone'}).get_text()	# find the telephone element and grab text
		telephone = telephone.strip()
	except (AttributeError):
		telephone = None

	try:
		ratingValue = soup.find('meta',{'itemprop':'ratingValue'}).get('content')				# find the ratingValue element and get the content					
	except (AttributeError):
		ratingValue = None					

	single_business_info = {																	# create a key:value pair dictionary to store the scraped information

		'yelp':yelp_url,
		'name':business_name,
		'website':business_url,
		'street_address':streetAddress,
		'address_locality':addressLocality,
		'address_region':addressRegion,
		'postal_code':postalCode,
		'phone_number':telephone,
		'rating':ratingValue

	}


	all_business_info.append(single_business_info)											# add the business info key:value pairs to a list

# print(all_business_info)

"""
write to a csvfile
"""
with open('listing.csv', 'w') as csvfile:
	fieldnames = ['name', 'phone_number', 'website', 'yelp', 'rating', 'street_address', 'address_locality', 'address_region', 'postal_code']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	writer.writeheader()


	for business in all_business_info:
		# print(business)
		writer.writerow(
			{
				'name': business['name'],
				'phone_number': business['phone_number'],
				'website': business['website'],
				'yelp': business['yelp'],
				'rating': business['rating'],
				'street_address': business['street_address'],
				'address_locality': business['address_locality'],
				'address_region': business['address_region'],
				'postal_code': business['postal_code'],

			}
		)







