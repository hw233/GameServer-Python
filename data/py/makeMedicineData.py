#-*- coding: utf-8 -*-

def getConfig(level):
	dWeight = {}
	for medicineId,data in gdData.iteritems():
		func = data["权重"]
		dWeight[medicineId] = func(level)
	return dWeight

#导表开始
gdData={
	221001:{"权重":lambda lv:lv*15+1000},
	221002:{"权重":lambda lv:lv*15+1000},
	221301:{"权重":lambda lv:lv*25+500},
	221302:{"权重":lambda lv:lv*22+700},
	221303:{"权重":lambda lv:lv*22+800},
	221304:{"权重":lambda lv:lv*22+800},
}
#导表结束