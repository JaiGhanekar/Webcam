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
		self.visual_recognition = VisualRecognitionV3('2016-05-20', api_key='3cbcdb71306a768f85f79f14ff92a358a9c63566')

	# @staticmethod
	def detectFaces(self, urlStr):
		# @ans: return a JSON file that contain face recognition information
		ans = json.dumps(self.visual_recognition.detect_faces(images_url = urlStr), indent = 2)
		return ans

	def zipper(self, lstUrls):
		# @lstUrls: a list of urls;
		# @ans: a zip file, that is saved
		zpfName = str(uuid.uuid4()) + '.zip'
		with ZipFile(zpfName,'a') as zpf:
			for url in lstUrls:
				response = requests.get(url)
				fileName = 'Sample_' + str(lstUrls.index(url)) + '.png'
				if fileName in zpf.namelist():
					continue
				zpf.writestr(fileName, response.content)
		zpf.close()
		return zpfName

	def createClassification(self, zipFile):
		# @zipfile: a zip file object
		# @classifier: a classifier object for watson

		# example for creating a classifier
		with open(join(dirname(__file__), '../resources/trucks.zip'), 'rb') as trucks, open(join(dirname(__file__), '../resources/cars.zip'), 'rb') as cars:
			classifer = json.dumps(self.visual_recognition.create_classifier('CarsvsTrucks', trucks_positive_examples = trucks, negative_examples = cars), indent = 2)
		# example for creating a classifier
		return classifier

	def predict(self, classifier, urlStr):
		# @classifier: a classifier object for watson
		# @return a json for the image classifed
		return json.dumps(self.visual_recognition.classifier(images_url = urlStr), indent = 2)



## test bench
a = WatsonVision()
#print a.detectFaces('http://a4.files.maxim.com/image/upload/c_fit,cs_srgb,dpr_1.0,h_1200,q_80,w_1200/MTM1MTQzNDQ5NjgxNzM0Mjc1.jpg')
lst = []
lst.append('https://upload.wikimedia.org/wikipedia/commons/4/40/Miranda_Kerr_(6873397963).jpg')
lst.append('https://upload.wikimedia.org/wikipedia/commons/c/c2/Miranda_Ker_(8449761941).jpg')
lst.append('http://www.fashiongonerogue.com/wp-content/uploads/2015/11/Miranda-Kerr-Swarovski-Spring-2016-Campaign04.jpg')
lst.append('http://a4.files.maxim.com/image/upload/c_fit,cs_srgb,dpr_1.0,h_1200,q_80,w_1200/MTM1MTQzNDQ5NjgxNzM0Mjc1.jpg')
lst.append('http://www.speakerscorner.me/wp-content/uploads/2015/12/miranda18.jpg')
lst.append('http://www.prettydesigns.com/wp-content/uploads/2014/01/Miranda-Kerr-Hairstyles-Ombre-Hair.jpg')
lst.append('https://upload.wikimedia.org/wikipedia/commons/7/7f/Miranda_Kerr_(6796124945).jpg')
lst.append('http://orig01.deviantart.net/7898/f/2014/040/4/5/digital_miranda_kerr_by_vannenov-d75s0z2.jpg')
lst.append('http://www.fashiongonerogue.com/wp-content/uploads/2015/07/Miranda-Kerr-Swarovski-2015.jpg')
lst.append('http://townsend-london.com/wp-content/uploads/Miranda_Kerr_01_2381.jpg')
print a.zipURLs(lst)






