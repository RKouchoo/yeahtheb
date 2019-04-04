# The class that creates a download que and downloads each video individually
# Code is pulled from other classes.

from sys import argv
from bs4 import BeautifulSoup  
import requests
import wget
import yaml

# We need a dictionary to filter the input url.
regexDict = {
	" " : "%20",
	"/" : "%2F",
	":" : "%3A"
}

#	     add, save, delete, load, load-append
commands = ["a", "s", "d", "l", "lp"]

baseConnURL = "https://www.tubeoffline.com/downloadFrom.php?host=Xvideos&video="

currentDownloadQue = []

# converts the url to an xstring using the dictionary
def convertURLToBaseConnURL(baseURL):
	for character, rep in regexDict.items():
		baseURL = baseURL.replace(character.lower(), rep)
	return baseURL

# takes in the url for a video and resolves and downloads it.
def doDownloadForURL(url):
	convertedTarget = convertURLToBaseConnURL(url)
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


def addToDownloadQue(url):
	currentDownloadQue.append(url)


def downloadScheduler():
	for url in currentDownloadQue:
		print("Downloading: {}".format(url))
		# force the video to be downloaded. (Sometimes the url isnt resolved)
		while True:
			try:
				print(url)
				doDownloadForURL(url)
				break
			except:
				print("Retrying download for: {}".format(url))
				pass


# saves an arraylist to a file.
def saveQueToYAML(que, fileName):
	data = yaml.dump(que)

	with open(fileName + ".yaml", "w+") as textFile:
		textFile.write(data)


# returns an array list loaded from a file.
def loadQueFromYAML(fileName):
	fileData = open(fileName, "r")
	return yaml.load(fileData.read())	



# Main thread
while(True):
	command = input("Enter command: ")

	if command == "a": # add url
		url = input("Please specify URL to add to que: ")
		addToDownloadQue(url)

	if command == "s": # save cache
		name = input("Please specify a file name: ")
		print("saving download cache")
		saveQueToYAML(currentDownloadQue, name)

	if command == "d": # download que
		print("Downloading que")
		downloadScheduler()
		saveQueToYAML(currentDownloadQue, "downloaded_que")
		pass

	if command == "l": # load cache
		name = input("Please specify que file-name: ")
		currentDownloadQue = loadQueFromYAML(name)

	if command == "lp": # append-load cache
		name = input("Please specify que file-name: ")
		tempQue = loadQueFromYAML(name)
		for url in tempQue:
			currentDownloadQue.append(url)
