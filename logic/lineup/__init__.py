# -*- coding: utf-8 -*-
'''阵法相关
'''

if "gLineupList" not in globals():
	gLineupList = {}

def createLineup(lineupId):
	'''创建阵法
	'''
	return lineup.object.Lineup(lineupId)

def createLineupAndLoad(lineupId, data):
	'''创建阵法，并加载数据
	'''
	lineupObj = createLineup(lineupId)
	lineupObj.load(data)
	return lineupObj

def createEye(eyeId):
	'''创建阵眼
	'''
	return lineup.object.Eye(eyeId)

def createEyeByNo(eyeNo, eyeId=None):
	'''根据导表创建阵眼
	'''
	if eyeId is None:
		eyeId = block.sysActive.gActive.genPropsId()

	eyeObj = createEye(eyeId)
	eyeObj.setNo(eyeNo)
	
	data = lineupData.getLineupEyeData(eyeNo)
	eyeObj.setSpeRatio(data["初始速度系数"])
	eyeObj.setSkill(data["主动技编号"])
	for skillId in data["被动技编号"]:
		eyeObj.setSkill(skillId)
	
	return eyeObj

def createEyeAndLoad(eyeId, data):
	'''创建阵眼，并加载数据
	'''
	eyeObj = createEye(eyeId)
	eyeObj.load(data)
	return eyeObj

def addEye(who, eyeNo):
	'''增加阵眼
	'''
	eyeObj = createEyeByNo(eyeNo)
	who.eyeCtn.addItem(eyeObj)
	return eyeObj

def get(lineupId):
	'''获取缓存中的阵法对象
	'''
	global gLineupList
	lineupObj = gLineupList.get(lineupId)
	if not lineupObj:
		lineupObj = createLineup(lineupId)
		gLineupList[lineupId] = lineupObj
	return lineupObj

def forkEye(eyeObj):
	obj = createEyeAndLoad(eyeObj.key, copy.deepcopy(eyeObj.save()))
	return obj

import lineup.object
import lineupData
import block.sysActive
import copy