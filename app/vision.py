## test code for Watson Visual Recognition 

# {
#   "credentials": {
#     "url": "https://gateway-a.watsonplatform.net/visual-recognition/api",
#     "note": "It may take up to 5 minutes for this key to become active",
#     "api_key": "3cbcdb71306a768f85f79f14ff92a358a9c63566"
#   }
# }


# import json
# from os.path import join, dirname
# from os import environ
# from watson_developer_cloud import VisualRecognitionV3

# visual_recognition = VisualRecognitionV3('2016-05-20', 
# 	api_key='{3cbcdb71306a768f85f79f14ff92a358a9c63566}')
# print(json.dumps(visual_recognition.detect_faces('/Users/ryanli/Documents/hackRice2016/testImg.jpg')))

import json
from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3

# imports for zipUrls function 
import uuid
import requests
from zipfile import ZipFile

class WatsonVision:
	"""docstring for ClassName"""
	def __init__(self):
		self.myKey = '3cbcdb71306a768f85f79f14ff92a358a9c63566'
		self.visual_recognition = VisualRecognitionV3('2016-05-20', api_key = self.myKey)

	# @staticmethod
	def detectFaces(self, urlStr):
		# @ans: return a JSON file that contain face recognition information
		ans = json.dumps(self.visual_recognition.detect_faces(images_url = urlStr), indent = 2)
		return ans

	def zipper(self, lstUrls, name):
		# @lstUrls: a list of urls;
		# @ans: a zip file, that is saved
		zpfName = name + '.zip'
		with ZipFile(zpfName,'a') as zpf:
			for url in lstUrls:
				response = requests.get(url)
				fileName = name + '_' + str(lstUrls.index(url)) + '.png'
				if fileName in zpf.namelist():
					continue
				zpf.writestr(fileName, response.content)
		return zpfName

	def createClassifier(self, zipFiles):
		# @zipfile: a list of strings that point to zip files
		# @classifier: a classifier object for watson
		# example for creating a classifier
		tempZipper = []
		# for fileName in zipFiles:
		for i in range (0, len(zipFiles)):
			fileName = zipFiles[i]
			fileName = fileName.replace('.zip', '')
			tempObj = open(join(dirname(__file__),  fileName + '.zip'), 'rb')
			tempZipper.append(tempObj)
		# send a multipart/form-data with requests in python
		url = 'https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classifiers?api_key=' + self.myKey + '&version=2016-05-20'
		# print url
		# for file in tempZipper:
		response = requests.post(url, tempZipper[0], tempZipper[1])
		print(response)

		# classifer = json.dumps(self.visual_recognition.create_classifier('people', people_positive_examples = tempZipper[0], tempZipper[1]), indent = 2)
		classifier = json.dumps(self.visual_recognition.create_classifier('peopleDetector', peopleDetector_positive_examples = response), indent = 2)
		# with open(join(dirname(__file__), '../resources/trucks.zip'), 'rb') as trucks, open(join(dirname(__file__), '../resources/cars.zip'), 'rb') as cars:
		# 	classifer = json.dumps(self.visual_recognition.create_classifier('CarsvsTrucks', trucks_positive_examples = trucks, negative_examples = cars), indent = 2)
		# example for creating a classifier
		print('Classifier Created Sucessfully.')
		return classifier

	def predict(self, classifier, urlStr):
		# @classifier: a classifier object for watson
		# @return a json for the image classifed
		return json.dumps(self.visual_recognition.classifier(images_url = urlStr), indent = 2)



# ## test bench
# a = WatsonVision()
# #print a.detectFaces('http://a4.files.maxim.com/image/upload/c_fit,cs_srgb,dpr_1.0,h_1200,q_80,w_1200/MTM1MTQzNDQ5NjgxNzM0Mjc1.jpg')
# # lst = []
# # lst.append('https://upload.wikimedia.org/wikipedia/commons/4/40/Miranda_Kerr_(6873397963).jpg')
# # lst.append('https://upload.wikimedia.org/wikipedia/commons/c/c2/Miranda_Ker_(8449761941).jpg')
# # lst.append('http://www.fashiongonerogue.com/wp-content/uploads/2015/11/Miranda-Kerr-Swarovski-Spring-2016-Campaign04.jpg')
# # lst.append('http://a4.files.maxim.com/image/upload/c_fit,cs_srgb,dpr_1.0,h_1200,q_80,w_1200/MTM1MTQzNDQ5NjgxNzM0Mjc1.jpg')
# # lst.append('http://www.speakerscorner.me/wp-content/uploads/2015/12/miranda18.jpg')
# # lst.append('http://www.prettydesigns.com/wp-content/uploads/2014/01/Miranda-Kerr-Hairstyles-Ombre-Hair.jpg')
# # lst.append('https://upload.wikimedia.org/wikipedia/commons/7/7f/Miranda_Kerr_(6796124945).jpg')
# # lst.append('http://orig01.deviantart.net/7898/f/2014/040/4/5/digital_miranda_kerr_by_vannenov-d75s0z2.jpg')
# # lst.append('http://www.fashiongonerogue.com/wp-content/uploads/2015/07/Miranda-Kerr-Swarovski-2015.jpg')
# # lst.append('http://townsend-london.com/wp-content/uploads/Miranda_Kerr_01_2381.jpg')
# # print a.zipper(lst, 'Kerr')

# kerrClass = a.createClassifier(['kerr.zip', 'scarlett.zip'])
# print a.predict(kerrClass, 'http://stylesweekly.com/wp-content/uploads/2014/07/Miranda-Kerr-Hair-Color.jpg')




