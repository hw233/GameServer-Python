# -*- coding: utf-8 -*-
import npc.object

class cNpc(npc.object.NpcBase):
	
	def __init__(self):
		npc.object.NpcBase.__init__(self)
		self.name = "物品Npc"
	
	def doLook(self, who):
		content = '''我可以为你做点什么呢?
Q清空包裹
Q丢弃物品
Q修改装备耐久
Q绑定或解绑物品
Q增加特技特效'''
		message.selectBoxNew(who, self.responseLook, content, self)
		
	def responseLook(self, who, selectNo):
		if selectNo == 1:
			who.propsCtn.clearAll()
			message.tips(who, "成功清空包裹")
		elif selectNo == 2:
			self.doGiveProps(who, self.discardProps)
		elif selectNo == 3:
			self.doGiveProps(who, self.modifyEquipLife, lambda propsObj:propsObj.kind==ITEM_EQUIP)
		elif selectNo == 4:
			self.doGiveProps(who, self.setBind)
		elif selectNo == 5:
			self.doGiveProps(who, self.addEquipSkill, lambda propsObj:propsObj.kind==ITEM_EQUIP)
			
	def doGiveProps(self, who, callbackFunc, filterFunc=None):
		pid = who.id
		propsIdList = []
		for propsObj in who.propsCtn.getAllValues():
			if filterFunc and not filterFunc(propsObj):
				continue
			propsIdList.append(propsObj.id)
		message.popPropsUI(who, functor(self.responseGiveProps, callbackFunc), "物品选择", propsIdList)
		
	def responseGiveProps(self, who, propsList, callbackFunc):
		propsObjList = []
		for propsId in propsList.iterkeys():
			propsObj = who.propsCtn.getItem(propsId)
			if not propsObj:
				message.tips(who, "你身上没有此物品")
				return
			propsObjList.append(propsObj)
			
		callbackFunc(who, propsObjList)
			
	def discardProps(self, who, propsObjList):
		for propsObj in propsObjList:
			who.propsCtn.removeItem(propsObj)
			message.tips(who, "丢弃了#C02%s#n" % propsObj.name)
			
	def modifyEquipLife(self, who, propsObjList):
		if len(propsObjList) != 1:
			message.tips(who, "每次只能修改一个")
			return
		propsObj = propsObjList[0]
		content = "装备#C02%s#n的耐久为%d, 请输入新的耐久:" % (propsObj.name, propsObj.getLife())
		message.inputBox(who, functor(self.doModifyEquipLife, propsObj.id), "设置装备耐久", content, TYPE_LIMIT_INT)
		
	def doModifyEquipLife(self, who, responseVal, propsId):
		propsObj = who.propsCtn.getItem(propsId)
		if not propsObj:
			return
		lifeNew = int(responseVal)
		if lifeNew < 0:
			return
		
		lifeAdd = lifeNew - propsObj.getLife()
		propsObj.addLife(lifeAdd)
		message.tips(who, "修改成功!")
		self.modifyEquipLife(who, [propsObj,])
		
	def setBind(self, who, propsObjList):
		'''绑定或解绑物品
		'''
		for propsObj in propsObjList:
			if propsObj.isBind():
				isBinded = False
			else:
				isBinded = True
			propsObj.bind(isBinded)
			who.endPoint.rpcModProps(propsObj.getMsg4Package(None, "addon"))
			
			if isBinded:
				message.tips(who, "[%s]绑定成功" % propsObj.name)
			else:
				message.tips(who, "[%s]解绑成功" % propsObj.name)
				
	def addEquipSkill(self, who, propsObjList):
		'''增加特技特效
		'''
		if len(propsObjList) != 1:
			message.tips(who, "一个一个来")
			return
		
		propsObj = propsObjList[0]
		skillList = []
		if propsObj.fetch("spEffect"):
			skillList.append(str(propsObj.fetch("spEffect")))
		if propsObj.fetch("spSkill"):
			skillList.append(str(propsObj.fetch("spSkill")))
		skillInfo = ",".join(skillList)

		content = "装备#C02%s#n的特技特效有[%s], 请输入新的特技特效:" % (propsObj.name, skillInfo)
		message.inputBox(who, functor(self.doAddEquipSkill, propsObj.id), "设置特技特效", content)
		
	def doAddEquipSkill(self, who, responseVal, propsId):
		propsObj = who.propsCtn.getItem(propsId)
		if not propsObj:
			return
		
		skillList = responseVal.split(",")
		if not skillList:
			message.tips(who, "格式错误")
			return
		
		for skillId in skillList:
			if not skillId.isdigit():
				message.tips(who, "格式错误")
				return
			skillId = int(skillId)
			skillObj = skill.get(skillId)
			if not skillObj:
				return

			if skillId / 1000 == 3:
				propsObj.set("spEffect", skillId)
			elif skillId / 1000 == 4:
				propsObj.set("spSkill", skillId)
			else:
				message.tips(who, "没有编号为%d的特技特效" % skillId)
				return
			
		who.endPoint.rpcModProps(propsObj.getMsg4Package(who.propsCtn, *propsObj.MSG_DETAIL))
		message.tips(who, "增加特技特效成功")
	

from common import *
from props.defines import *
from qanda.defines import *
import message
import skill