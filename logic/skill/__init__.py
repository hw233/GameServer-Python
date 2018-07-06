# -*- coding: utf-8 -*-

def init():
	import skill.load

if "gSkillList" not in globals():
	gSkillList = {}

def new(skId):
	'''创建法术
	'''
	moduleList = skill.load.getModuleList()
	if skId not in moduleList:
		raise Exception("找不到编号为%s的技能" % skId)
	return moduleList[skId].Skill()

def createAndLoad(skId, data):
	skObj = new(skId)
	skObj.load(data)
	return skObj

def get(skId):
	'''获取法术
	'''
	global gSkillList
	if skId not in gSkillList:
		pfObj = new(skId)
		gSkillList[skId] = pfObj
	return gSkillList[skId]

def isLow(skId):
	'''是否低级技能
	'''
	return skId / 100 == 51

def isHigh(skId):
	'''是否高级技能
	'''
	return skId / 100 == 52

def getLow(skId):
	'''获取对应的低级技能
	'''
	if isHigh(skId):
		return 5100 + skId % 100
	return 0 

def getHigh(skId):
	'''获取对应的高级技能
	'''
	if isLow(skId):
		return 5200 + skId % 100
	return 0

def onUpLevel(who):
	'''玩家升级时
	'''
	skill.upgrade.checkSchSkillOpen(who)
	
def isPraticeSkill(skillId):
	'''是否修炼技能
	'''
	if 6101 <= skillId <= 6108:
		return 1
	return 0

def isRolePraticeSkill(skillId):
	'''是否人物修炼技能
	'''
	if 6101 <= skillId <= 6104:
		return 1
	return 0

def isPetPraticeSkill(skillId):
	'''是否宠物修炼技能
	'''
	if 6105 <= skillId <= 6108:
		return 1
	return 0

import skill.load
import skill.upgrade
