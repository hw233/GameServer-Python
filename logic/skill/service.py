# -*- coding: utf-8 -*-
# 技能服务
import endPoint
import skill_pb2

class cService(skill_pb2.terminal2main):

	@endPoint.result
	def rpcSkillSchUpgrade(self,ep, who, reqMsg): return rpcSkillSchUpgrade(who, reqMsg)
	
	@endPoint.result
	def rpcSkillGuildLearn(self,ep, who, reqMsg): return rpcSkillGuildLearn(who, reqMsg)
	
	@endPoint.result
	def rpcSkillGuildUse(self,ep, who, reqMsg): return rpcSkillGuildUse(who, reqMsg)
	
	# @endPoint.result
	# def rpcSkillMakeMedicine(self,ep, who, reqMsg): return rpcSkillMakeMedicine(who, reqMsg)

	@endPoint.result
	def rpcSkillPracticeOpen(self,ep, who, reqMsg): return rpcSkillPracticeOpen(who, reqMsg)

	@endPoint.result
	def rpcSkillPracticeLearn(self,ep, who, reqMsg): return rpcSkillPracticeLearn(who, reqMsg)

def rpcSkillSchUpgrade(who, reqMsg):
	skId = reqMsg.iId
	if skId == 0: # 一键升级
		skill.upgrade.doSkillSchUpgradeAll(who)
	else:
		skill.upgrade.doSkillSchUpgrade(who, skId)

def rpcSkillGuildLearn(who, reqMsg):
	skId = reqMsg.iId
	skill.upgrade.doSkillGuildLearn(who, skId)

def rpcSkillGuildUse(who, reqMsg):
	skId = reqMsg.iId
	skLv = reqMsg.iLevel
	skill.upgrade.doSkillGuildUse(who, skId, skLv)

def rpcSkillPracticeOpen(who, reqMsg):
	guildLevel = who.getPracticeGuildLevel()
	guildPoint = who.getPracticeGuildPoint()
	guildHistory = who.fetch("guildPoint")
	who.endPoint.rpcSkillPracticeLevel(guildLevel,guildPoint,guildHistory)

def rpcSkillPracticeLearn(who, reqMsg):
	skId = reqMsg.iId
	learnType = reqMsg.iType
	skill.upgrade.doSkillPracticeLearn(who, skId, learnType)

# def rpcSkillMakeMedicine(who, reqMsg):
# 	skId = 504
# 	level = who.querySkillLevel(skId)
# 	if not level:
# 		return
# 	skObj = skill.new(skId)
# 	skObj.level = level
	
# 	propsIdList = {}
# 	for propsId in reqMsg.iPropsIdList:
# 		propsIdList[propsId] = propsIdList.get(propsId, 0) + 1

# 	if propsIdList:
# 		skill.upgrade.doSkillMakeMedicine(who, skObj, propsIdList)
# 	else:
# 		skill.upgrade.doSkillMakeMedicineByCash(who, skObj)

def rpcSkillLevelAll(who):
	'''发送所有人物技能信息
	'''
	skillInfoList = []
	for skillObj in who.skillCtn.getAllValues():
		skillInfoList.append(packSkillData(skillObj))
	for skillObj in who.equipSkillCtn.getAllValues():
		skillInfoList.append(packSkillData(skillObj))
	skillInfoAll = skill_pb2.skillInfoAll()
	skillInfoAll.skillInfoList.extend(skillInfoList)
	who.endPoint.rpcSkillLevelAll(skillInfoAll)

def packSkillData(skillObj):
	skillInfo = skill_pb2.skillInfo()
	skillInfo.iId = skillObj.id
	skillInfo.iLevel = skillObj.level
	if hasattr(skillObj, "getPoint"):
		skillInfo.iPoint = skillObj.getPoint()
	return skillInfo

def rpcSkillAdd(who, skillObj):
	'''增加技能
	'''
	msgObj = packSkillData(skillObj)
	who.endPoint.rpcSkillAdd(msgObj)
	
def rpcSkillDelete(who, skillId):
	'''删除技能
	'''
	who.endPoint.rpcSkillDelete(skillId)

def rpcSkillChange(who, skillObj, *attrNameList):
	'''修改技能
	'''
	msg = {}
	msg["iId"] = skillObj.id
	
	for attrName in attrNameList:
		if attrName == "level":
			msg["iLevel"] = skillObj.level
		elif attrName == "point":
			msg["iPoint"] = skillObj.getPoint()
	
	who.endPoint.rpcSkillChange(**msg)
	

import skill.upgrade
