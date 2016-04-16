#!/usr/local/bin/python3

import csv

from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

user_query_input = input('Type your search query: ')															
user_location_input = input('Type your search location: ')								

startTime = datetime.now()


all_business_info = []									# create empty list to store business info dictionary


driver = webdriver.Chrome()
driver.get("http://www.yelp.com")

searchQueryInputElement = driver.find_element_by_name("find_desc")
searchQueryInputElement.send_keys(user_query_input)

locationQueryInputElement = driver.find_element_by_name("find_loc")
# locationQueryInputElement.send_keys(Keys.CONTROL + "a")
locationQueryInputElement.clear()
locationQueryInputElement.send_keys(user_location_input + Keys.RETURN)


driver.implicitly_wait(10)

current_url = driver.current_url

for i in range(10):

	driver.get(current_url)

	for x in range(10):
		
		# wait = WebDriverWait(driver, 10)
		# hrefElements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'biz-name')))
		hrefElements = driver.find_elements_by_class_name("biz-name")

		# click first hrefElement
		hrefElements[x].click()

		driver.implicitly_wait(10)

		try:
			businessNameElement = driver.find_element_by_xpath("//h1[@itemprop='name']")
			business_name = businessNameElement.text
		except:
			business_name = None

		try:
			ratingValueElement = driver.find_element_by_xpath("//meta[@itemprop='ratingValue']")
			rating_value = ratingValueElement.get_attribute("content")
		except:
			rating_value = None

		try:
			streetAddressElement = driver.find_element_by_xpath("//span[@itemprop='streetAddress']")
			street_address = streetAddressElement.text
		except:
			street_address = None

		try:
			addressLocalityElement = driver.find_element_by_xpath("//span[@itemprop='addressLocality']")
			address_locality = addressLocalityElement.text
		except: 
			address_locality = None

		try:
			addressRegionElement = driver.find_element_by_xpath("//span[@itemprop='addressRegion']")
			address_region = addressRegionElement.text
		except:
			address_region = None

		try:
			postalCodeElement = driver.find_element_by_xpath("//span[@itemprop='postalCode']")
			postal_code = postalCodeElement.text
		except:
			postal_code = None

		try:
			telephoneElement = driver.find_element_by_xpath("//span[@itemprop='telephone']")
			phone_number = telephoneElement.text
		except:
			phone_number = None

		try:
			websiteElement = driver.find_element_by_xpath("//div[@class='biz-website']/a")
			website_url = websiteElement.get_attribute("href")
		except:
			website_url = None


		single_business_info = {}

		single_business_info['name'] = business_name
		single_business_info['rating'] = rating_value
		single_business_info['street_address'] = street_address
		single_business_info['address_locality'] = address_locality
		single_business_info['address_region'] = address_region
		single_business_info['postal_code'] = postal_code
		single_business_info['phone'] = phone_number
		single_business_info['website'] = website_url

		all_business_info.append(single_business_info)

		# go back to previous
		driver.execute_script("window.history.go(-1)")

	# print(hrefElements)
	paginationLinkElement = driver.find_element_by_link_text("Next")
	paginationLinkElement.click()
	current_url = driver.current_url


# print(all_business_info)
driver.quit()
"""
write to a csvfile
"""
with open('listing.csv', 'w') as csvfile:
	fieldnames = ['name', 'phone', 'website', 'rating', 'street_address', 'address_locality', 'address_region', 'postal_code']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	writer.writeheader()


	for business in all_business_info:
		# print(business)
		writer.writerow(
			{
				'name': business['name'],
				'phone': business['phone'],
				'website': business['website'],
				# 'yelp': business['yelp'],
				'rating': business['rating'],
				'street_address': business['street_address'],
				'address_locality': business['address_locality'],
				'address_region': business['address_region'],
				'postal_code': business['postal_code'],

			}
		)

print(datetime.now() - startTime)

