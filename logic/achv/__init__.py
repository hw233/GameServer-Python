# -*- coding: utf-8 -*-
'''成就系统
'''

def createAchv(achvId):
	import achv.load
	return achv.load.moduleList[achvId].Achievement()

def createAchvAndLoad(achvId, data):
	'''创建成就，并加载数据
	'''
	achvObj = createAchv(achvId)
	achvObj.load(data)
	return achvObj