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
import os

# import line to: from /usr/local/lib/python2.7/dist-packages/watson_developer_cloud import VisualRecognitionV3 as VisualRecognition

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

	def createClassifier(self, zipFiles, name):
		# @zipfile: a list of strings that point to zip files
		# @classifier: a classifier object for watson
		# example for creating a classifier

		strAdd = ''
		for i in range (0, len(zipFiles)):
			fileName = zipFiles[i]
			fileName = fileName.replace('.zip', '')
			strAdd = strAdd + '\"'+ fileName + '_positive_examples=@' + fileName +'.zip' '\"' + ' -F '
		print strAdd
		cmd = "curl -X POST -F " + strAdd + '\"name =' + name + '\" ' + '\"https://watson-api-explorer.mybluemix.net/visual-recognition/api/v3/classifiers?api_key=3cbcdb71306a768f85f79f14ff92a358a9c63566&version=2016-05-20\"'
		# print cmd
		out = os.system(cmd)
		return out


	def predict(self, urlStr, classifierID):
		# @classifier: a classifier object for watson
		# @return a json for the image classifed

		cmd = "curl -X GET --header \'Accept: application/json\' --header \'Accept-Language: en\' \'https://watson-api-explorer.mybluemix.net/visual-recognition/api/v3/classify?api_key=3cbcdb71306a768f85f79f14ff92a358a9c63566" + '&url=' + urlStr + "&classifier_ids=" + classifierID + "&version=2016-05-20\'"
		out = os.system(cmd)
		print out
		return out

	def clean(self, classifierID):
		cmd = "curl -X DELETE --header \'Accept: application/json\' \'https://watson-api-explorer.mybluemix.net/visual-recognition/api/v3/classifiers/" + classifierID + "?api_key=3cbcdb71306a768f85f79f14ff92a358a9c63566&version=2016-05-20\'"
		out = os.system(cmd)
		print out
		return out


## test bench and example use:
# instance the class
a = WatsonVision() 
# make classififier with zip files:
# possible buggy when zip is not in the same directory with this python file
a.createClassifier(['kerr.zip', 'jo.zip'],'ppl')
# find out who is this with predict
a.predict('https://watson-api-explorer.mybluemix.net/visual-recognition/api/v3/classify?api_key=3cbcdb71306a768f85f79f14ff92a358a9c63566&url=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2F4%2F40%2FMiranda_Kerr_(6873397963).jpg', 'ppl_104579820')
#clean delete the classifer
a.clean('ppl_104579820')
