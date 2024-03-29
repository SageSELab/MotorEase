import os
import xml.etree.ElementTree as ET
import math
from PIL import Image

def getBounds(inText):
	split = inText.split('][')
	
	split[0] = split[0].strip('[')
	split[1] = split[1].strip(']')
	
	split[0] = split[0].split(",")
	split[1] = split[1].split(",")
	
	split[0] = [int(split[0][0]), int(split[0][1])]
	split[1] = [int(split[1][0]), int(split[1][1])]
	return split

def isSmall(bounds):
	screenBounds = [[0, 0], [1080, 1794]]
	h = bounds[1][0] - bounds[0][0]
	w = bounds[1][1] - bounds[0][1]
	area = h*w
	screenArea = 1080*1794
	if area < screenArea/10:
		return True
	else:
		return False

def get4(box):
	return([box[0][0], box[0][1], box[1][0], box[1][1],])

def subtractBounds(b1, b2):
	firstPair = abs(b1[0][0] - b2[0][0])
	firstPair1= abs(b1[0][1] - b2[0][1])
	
	secondPair = abs(b1[1][0] - b2[1][0])
	secondPair1 = abs(b1[1][1] - b2[1][1])
	
	# (diff in first set of starting, diff in second set of ending bounds)
	totalDiff = (firstPair + secondPair, firstPair1 + secondPair1)
	return totalDiff
	

def findViolations(dictionary, dataPath):
	allViolations = []
	noViolations = []
	for i in dictionary: 
		if len(dictionary[i]) > 1:

			initBounds = get4(dictionary[i][0][0])

			imgPathinit = dataPath + "/" + str(dictionary[i][1][1][0:-3]) + "png"
			sub = (0, 0)
			
			initPixels1 = Image.open(imgPathinit)
			init = initPixels1.crop(initBounds)
			initPixels = list(init.getdata())

			for j in dictionary[i]:
				fourBox = get4(dictionary[i][0][0])
				imgPath = dataPath + "/" + str(j[1][0:-3]) + "png"
				im = Image.open(imgPath)
				im = im.crop(fourBox)
				pixels = list(im.getdata())

				if pixels == initPixels:
					if dictionary[i][0][0][0][0] == j[0][0][0] and subtractBounds(dictionary[i][0][0], j[0])[0] != 0 and subtractBounds(dictionary[i][0][0], j[0])[1] != 0:
						#print(subtractBounds(dictionary[i][0][0], j[0]))
						if j[1].split("_B")[0] not in allViolations and j[1].split("_B")[0]:
							allViolations.append(j[1].split("_B")[0])
						elif j[1].split("_B")[0] not in allViolations and j[1].split("_B")[0] not in noViolations:
							noViolations.append(j[1].split("_B")[0])
				initPixels1.close()
				im.close()
	return([allViolations, noViolations])


def PersistentDriver(dataPath):
	fullDictionary = {}
	screenshots = []
	xmls = []
	for subdir1, dirs1, files1 in os.walk(dataPath):
		for file in files1:
			if ".png" in file: 
				screenshots.append(file)
			if ".xml" in file: 
				xmls.append(file)
				xmlPath = dataPath + "/" + file
				tree = ET.parse(xmlPath)
				for elem in tree.iter():
					obj = elem.items()
					if len(obj) > 2:
						if obj[2][1] != '':
							objectBounds= getBounds(obj[len(obj)-1][1])
							if isSmall(objectBounds):
								if 'frame_item_image' not in obj[2][1]:
									if obj[2][1] not in fullDictionary.keys():
										addList = [objectBounds, file]
										#print(obj[2][1])
										fullDictionary[obj[2][1]] = [addList]
										#print(obj[2])
										#print(obj[len(obj)-1])
									else:
										newl = fullDictionary[obj[2][1]]
										addList = [objectBounds, file]
										newl.append(addList)
										fullDictionary[obj[2][1]] = newl
	screenshots.sort()
	xmls.sort()
	res = findViolations(fullDictionary, dataPath)
	# results = open("PeristentEvaluationResults.txt", 'w')
	#print(noViolations)
	#print(allViolations)
	return(res)
	# for i in list(dict.fromkeys(noViolations)):
	#     results.write(i + "--0" + "\n")
	# for i in list(dict.fromkeys(allViolations)):
	#     results.write(i + "--1" + "\n")

	results.close()    
#print(fullDictionary)
		#print(xmls)




		
		
		
		
		
		
		
		
		
		
		
		
