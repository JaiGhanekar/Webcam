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
#     api_key='{3cbcdb71306a768f85f79f14ff92a358a9c63566}')
# print(json.dumps(visual_recognition.detect_faces('/Users/ryanli/Documents/hackRice2016/testImg.jpg')))

import time
import requests
import uuid
from PIL import Image
import json
from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3
from collections import defaultdict
import os
from io import BytesIO
import sys

# import line to: from /usr/local/lib/python2.7/dist-packages/watson_developer_cloud import VisualRecognitionV3 as VisualRecognition

# imports for zipUrls function 
# import uuid
# import requests
from zipfile import ZipFile

class WatsonVision:
    """docstring for ClassName"""
    def __init__(self):
#        self.myKey = 'cb6c267484a54861e0b43ba8e24f91718fff0fb3'
        self.myKey = 'cb6c267484a54861e0b43ba8e24f91718fff0fb3'
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
        print(strAdd)
        cmd = "curl -X POST -F " + strAdd + '\"name =' + name + '\" ' + '\"https://watson-api-explorer.mybluemix.net/visual-recognition/api/v3/classifiers?api_key='+ self.myKey+'&version=2016-05-20\"'
        # print cmd
        out = os.system(cmd)
        return out


    def predict(self, urlStr, classifierID):
        # @classifier: a classifier object for watson
        # @return a json for the image classifed
        # DEPRECATED

        cmd = "curl -X GET --header \'Accept: application/json\' --header \'Accept-Language: en\' \'https://watson-api-explorer.mybluemix.net/visual-recognition/api/v3/classify?api_key=831bb3c24f7bcc0755f7d538fa651d0dc6323296" + '&url=' + urlStr + "&classifier_ids=" + classifierID + "&version=2016-05-20\'"
        out = os.system(cmd)
#        print out
        return out

    def splitPredict(self, imgURL, classifierID):
        # predicts the identity of faces in pictures with 1, 2, or possibly more faces. 
        # @imgURL: URL of image to be analyzed
        # returns @resps: dictionary with keys = face #, values = [identity, score]

        # Testing import codes: 
#       img = open(join(dirname(__file__), imgFileName), 'rb')
#       with Image.open(BytesIO(requests.get(imgURL).content)) as imgObj:
    
        # create Visual Recognition Class Object 
        # vr = VisualRecognitionV3('2016-05-20',api_key=apiKey)
            
        # Detect faces in img 
        listFaces = json.loads(self.visual_recognition.detect_faces(images_url=imgURL).decode('utf-8'))

        faces = listFaces['images'][0]['faces']
        
        # Instantiate response 
        resps = defaultdict(list)

        # CLassify sub-images of cropped faces if image has >2 faces
        if len(faces) >= 2:   
            with Image.open(BytesIO(requests.get(imgURL).content)) as imgObj:
                imgFileName = str(uuid.uuid4()) + '.png'
                imgObj.save(imgFileName)
                for face in faces: 
                    bbox = face['face_location']
                    box = (bbox['left'],bbox['top'],bbox['left']+bbox['width'],bbox['top']+bbox['height'])
                    tempImg = imgObj.crop(box)
                    tempImgFileName = 'face_' + str(faces.index(face)) + '.png'
                    tempImg.save(tempImgFileName)
                    names = []; scores = []; 
                    with open(join(dirname(__file__), tempImgFileName), 'rb') as tempImg:           
                        a = self.visual_recognition.classify(images_file=tempImg, classifier_ids=classifierID)
                        for pred in a['images'][0]['classifiers'][0]['classes']:
                            names.append(pred['class']); scores.append(pred['score'])
                    resps[faces.index(face)].append(names)
                    resps[faces.index(face)].append(scores)
        
        # Classify single image that has only 1 face 
        else:
                clf = self.visual_recognition.classify(images_url=imgURL, classifier_ids=classifierID)
                return clf                
                names = []; scores = []; 
                for pred in clf['images'][0]['classifiers'][0]['classes']:
                    names.append(pred['class']); scores.append(pred['score'])
                resps[0].append(names); resps[0].append(scores)
        
            
        # Return final prediction responses 
        final_preds = {}
        for faceIndex in resps.keys():
                 results = resps[faceIndex]
                 names = results[0]; scores = results[1];
                 maxScore = max(scores); 
                 final_preds[faceIndex] = names[scores.index(maxScore)]
        
        print(resps)
        return final_preds

    def clean(self, classifierID):
        cmd = "curl -X DELETE --header \'Accept: application/json\' \'https://watson-api-explorer.mybluemix.net/visual-recognition/api/v3/classifiers/" + classifierID + "?api_key=831bb3c24f7bcc0755f7d538fa651d0dc6323296&version=2016-05-20\'"
        out = os.system(cmd)
#        print out
        return out


## test bench and example use:
# instance the class
a = WatsonVision() 
# make classififier with zip files:
# possible buggy when zip is not in the same directory with this python file
a.createClassifier(['ryan.zip', 'linus.zip','jai.zip','tracy.zip','john.zip'],'ppl')
# find out who is this with predict
#b = a.splitPredict('https://s13.postimg.org/w5s3cktsn/yls2.jpg', 'ppl_838926004')
#clean delete the classifer
# a.clean('ppl_2145507184')
