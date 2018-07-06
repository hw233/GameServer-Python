# -*- coding: utf-8 -*-

def learn(who, lineupId):
	'''学习阵法
	'''
	if who.lineupCtn.getItem(lineupId): # 已有此阵法
		message.tips(who, "你已学习过此阵法")
		return
	
	data = lineupData.getLineupData(lineupId)
	needPropsNo = data["学习道具"]
	propsObj = who.propsCtn.hasPropsByNo(needPropsNo)
	if not propsObj:
		message.tips(who, "你身上没有对应的阵法道具")
		return
	
	writeLog("lineup/learn", "%d learn %d cost %s" % (who.id, lineupId, needPropsNo))
	who.propsCtn.addStack(propsObj, -1)
	lineupObj = who.lineupCtn.setLevel(lineupId, 1)
	message.tips(who, "习得#C02%s#n成功！" % data["名称"])
	
	import listener
	listener.doListen("学习阵法", who, lineupId=lineupId)

def upgrade(who, lineupObj, propsIdList):
	'''提升阵法
	'''
	oldLevel = lineupObj.level
	if oldLevel >= lineupObj.getLevelMax():
		message.tips(who, "阵法已经最大级，不需要再学习")
		return
	
	expTotal = 0
	for propsId, amount in propsIdList.iteritems():
		propsObj = who.propsCtn.getItem(propsId)
		if not propsObj:
			message.tips(who, "你身上没有此升级材料")
			return
		if amount <= 0:
			return
		if propsObj.stack() < amount:
			message.tips(who, "#C02%s#n不足" % propsObj.name)
			return
		
		exp = lineupData.getExpByProps(lineupObj.id, propsObj.no()) * amount
		if not exp: # 材料不对
			message.tips(who, "请选择正确的升级材料")
			return
		
		expTotal += exp
		
	writeLog("lineup/upgrade", "%d %d add exp %d cost %s" % (who.id, lineupObj.id, expTotal, propsIdList))
	
	for propsId, amount in propsIdList.iteritems():
		propsObj = who.propsCtn.getItem(propsId)
		who.propsCtn.addStack(propsObj, -amount)
		
	who.lineupCtn.addExp(lineupObj.id, expTotal)
	if lineupObj.level > oldLevel:
		message.tips(who, "恭喜！#C02%s#n已经提升至#C04%d级#n" % (lineupObj.name,lineupObj.level))

def eyeChange(who, eyeObj):
	'''变幻
	'''
	if eyeObj.skillCount() >=4:
		message.confirmBoxNew(who, functor(responseEyeChange, eyeObj.id), "当前的阵眼不错，是否真的需要变幻？\nQ取消\nQ变幻")
		return
	doEyeChange(who, eyeObj.id)
		
def responseEyeChange(who, yes, eyeId):
	if not yes:
		return
	doEyeChange(who, eyeId)
	
def doEyeChange(who, eyeId):
	eyeObj = who.eyeCtn.getItem(eyeId)
	if not eyeObj:
		return
			
	if not who.day.fetch("eyeChange"):
		if not eyeCheckAndCost(who,eyeObj):
			return
	else:
		who.day.set("eyeChange",1)

	speRation = rand(63,80)
	isStart = 0
	tips = "变化成功"
	if rand(100) < 10: #变星
		changeSkillList = skillListByCommon(True)
		changeSkillList.append(skillListByStart())
		isStart = 1
		tips = "恭喜！该阵眼已成变星"
	else:
		changeSkillList = skillListByCommon()

	skillList = eyeObj.fetch("skillList")[:1]
	skillList.extend(changeSkillList)
	eyeObj.set("skillList",skillList)
	eyeObj.generateSkillList()
	eyeObj.setStar(isStart)
	eyeObj.setSpeRatio(speRation)
	lineup.service.rpcEyeMod(who,eyeObj,"isStar","skillList","speRatio")
	message.tips(who, tips)

def skillListByStart():
	'''变星库抽取技能
	'''
	starSkillList = lineupData.getSkillList("变星被动技库")
	startSkill = starSkillList[rand(len(starSkillList))]
	return startSkill

def skillListByCommon(isStart=False):
	'''普通库抽取技能
	'''
	if isStart:
		count = 3
	else:
		count = rand(0,3)
	if not count:
		return []
	commonSkillList = lineupData.getSkillList("普通被动技库")
	return shuffleList(commonSkillList,count)

def eyeCheckAndCost(who, eyeObj):
	'''检查和扣除道具
	'''
	costData = eyeObj.getConfig("刷新道具")
	keyList = costData.keys()
	haveList = who.propsCtn.getPropsAmountByNos(*keyList)

	for idx,key in enumerate(keyList):
		if haveList[idx] < costData[key]:
			message.tips(who, "道具不够")
			return False

	for propsNo,count in costData.iteritems():
		who.propsCtn.subtractPropsByNo(propsNo,count,"阵眼变幻")

	return True

from common import *
import message
import lineupData
import lineup.service
import lineup