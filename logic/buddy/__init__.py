# -*- coding: utf-8 -*-
'''助战伙伴
'''
def create(iNo):
	obj = buddy.object.Buddy(iNo)
	shape = buddyData.getBuddyInfo(iNo, "造型")
	shape, shapeParts = template.transShapeStr(shape)
	obj.shape = shape
	obj.shapeParts = shapeParts
	return obj

def new(iNo):
	obj = create(iNo)
	obj.onBorn()
	skillList = list(obj.getConfig("主动技能"))
	skillList.extend(list(obj.getConfig("天赋技能")))
	obj.set("skillList",skillList)
	obj.reCalcAttr()
	return obj

def createAndLoad(iNo, data, bReClc=True):
	obj = create(iNo)
	obj.load(data)
	if bReClc:
		obj.reCalcAttr()
	return obj

def add(who, iNo):
	buddyObj = new(iNo)
	who.buddyCtn.addItem(buddyObj)
	buddyObj.checkRelation(who)
	who.buddyCtn.addMajor(buddyObj)
	buddyObj.reCalcAttr()
	
	import listener
	listener.doListen("获得助战", who, buddyNo=buddyObj.no)

	return buddyObj

def onUpLevel(who):
	for buddyObj in who.buddyCtn.getAllValues():
		buddyObj.reCalcAttr()

def sendBuddyForNewbie(who):
	for iPos,iNo in enumerate([1001,2001,3001,4001]):
		buddyObj = add(who, iNo)
		buddyObj.addQuality(2)
		skillId = buddyObj.getConfig("天赋技能")[buddyObj.getQuality()-2]
		buddyObj.setSkill(skillId)
		buddyObj.reCalcAttr()
		buddyObj.attrChange("quality")
		who.buddyCtn.upBattle(1,iNo,iPos)

import buddy.object
import buddyData
import template