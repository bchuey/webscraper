# webscraper

Input: user's query
Output: Business listing info

v1:
- grabs the query
- opens url w/ ?params
- uses BS4 to search for <tags>
- creates object for each business listing
- spits out in CSV format

v2:
- uses Selenium to open browser
- traverses through pagination
- ...
