# Main downloader class

from sys import argv
from bs4 import BeautifulSoup  
import requests
import wget

baseConnURL = "https://www.tubeoffline.com/downloadFrom.php?host=Xvideos&video="

# We need a dictionary to filter the input url.
regexDict = {
	" " : "%20",
	"/" : "%2F",
	":" : "%3A"
}

target = argv[1] # The URL to grab all of the info from.

# converts the url to an xstring using the dictionary
def convertURLToBaseConnURL(baseURL):
	for character, rep in regexDict.items():
		baseURL = baseURL.replace(character.lower(), rep)
	return baseURL

convertedTarget = convertURLToBaseConnURL(target)
connnectedConvertedTarget = baseConnURL + convertedTarget
requestedURLHTML = requests.get(connnectedConvertedTarget)

siteSoup = BeautifulSoup(requestedURLHTML.text, 'html.parser')

downloadURL = ""

for link in siteSoup.find_all('a'):
	testLink = link.get('href')
	if isinstance(testLink, str):
		if "/videos/mp4/" in testLink:
			downloadURL = testLink

wget.download(downloadURL)