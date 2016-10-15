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

class watsonVision:
	"""docstring for ClassName"""
	def __init__(self):
		self.visual_recognition = VisualRecognitionV3('2016-05-20', api_key='3cbcdb71306a768f85f79f14ff92a358a9c63566')

	# @staticmethod
	def detectFaces(self, urlStr):
		# @ans: return a JSON file that contain face recognition information
		ans = json.dumps(self.visual_recognition.detect_faces(images_url = urlStr), indent = 2)
		return ans

	def zipURLs(self, lstUrls):
		# @lstUrls: a list of urls;
		# @ans: a zip file, that is saved

		
		return ans

	def createClassification(self, zipFile):
		# @zipfile: a zip file object
		# @classifier: a classifier object for watson

		# example for creating a classifier
		with open(join(dirname(__file__), 
			'../resources/trucks.zip'), 'rb') as trucks, \
				open(join(dirname(__file__), 
					'../resources/cars.zip'), 'rb') as cars:

		classifer = json.dumps(self.visual_recognition.create_classifier('CarsvsTrucks', trucks_positive_examples = trucks, 
			negative_examples = cars), indent = 2)
		# example for creating a classifier

		return classifier

	def predict(self, classifier, urlStr):
		# @classifier: a classifier object for watson
		# @return a json for the image classifed
		return json.dumps(self.visual_recognition.classifier(images_url = urlStr), indent = 2)




## test bench
a = watsonVision()
print a.detectFaces('http://a4.files.maxim.com/image/upload/c_fit,cs_srgb,dpr_1.0,h_1200,q_80,w_1200/MTM1MTQzNDQ5NjgxNzM0Mjc1.jpg')