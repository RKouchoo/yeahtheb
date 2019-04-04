# Main downloader class

from sys import argv
from bs4 import BeautifulSoup  
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import wget
import time

baseConnURL = "https://www.tubeoffline.com/downloadFrom.php?host=Xvideos&video="

# We need a dictionary to filter the input url.
regexDict = {
	" " : "%20",
	"/" : "%2F",
	":" : "%3A"
}

target = argv[1] # The URL to grab all of the info from.

chromeOptions = Options()  
chromeOptions.add_argument("--headless")
chromeOptions.add_argument("--window-size=3840,2160") # 4K to make sure as many as possible video's are rendered on the page.

browser = webdriver.Chrome(chrome_options=chromeOptions)
browser.get(target)
time.sleep(5)
browser.get_screenshot_as_file("capture.png")
htmlSource = browser.page_source
browser.close()

#print(htmlSource)

# get the main page metadata
targetSoup = BeautifulSoup(htmlSource, 'html.parser')

links = []

for link in targetSoup.find_all('div', class_="thumb"):
	
	testSoup = BeautifulSoup(str(link), 'html.parser')
	
	for l in testSoup.find_all('a'):
		s = l.get("href")
		if "prof-video-click" not in s:
			filler = True # do nothing
		else:
			#print(s)
			links.append(s)

# Flatten the url list to a standard form.
newURLList = []
for aLink in links:
	if "https" not in aLink:
		new = "https://www.xvideos.com" + aLink
		newURLList.append(new)
	else:
		newURLList.append(aLink)

# need to resolve the redirect urls
redirectURLList = []
pos = 1
for sLink in newURLList:
	r = requests.get(sLink)
	tempUrl = r.url
	print("Resolving video: {} of {}".format(pos, len(newURLList)))
	pos += 1
	redirectURLList.append(r.url)


# converts the url to an xstring using the dictionary
def convertURLToBaseConnURL(baseURL):
	for character, rep in regexDict.items():
		baseURL = baseURL.replace(character.lower(), rep)
	return baseURL

dlPos = 1
for urls in redirectURLList:

	convertedTarget = convertURLToBaseConnURL(urls)
	connnectedConvertedTarget = baseConnURL + convertedTarget
	requestedURLHTML = requests.get(connnectedConvertedTarget)
	siteSoup = BeautifulSoup(requestedURLHTML.text, 'html.parser')
	
	downloadURL = ""

	for link in siteSoup.find_all('a'):
		testLink = link.get('href')
		if isinstance(testLink, str):
			if "/videos/mp4/" in testLink:
				downloadURL = testLink

	print("Downloading video: {} of {}".format(dlPos, len(redirectURLList)))
	print(downloadURL)
	time.sleep(2)
	dlPos += 1

	wget.download(downloadURL)
