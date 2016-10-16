from vision import WatsonVision
import sys

visionUtil = WatsonVision()
result = visionUtil.splitPredict('http://192.241.132.19:80/img/' + sys.argv[1], 'ppl_1905871502')
return result
