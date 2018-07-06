# -*- coding: utf-8 -*-
import npc.object

class cNpc(npc.object.NpcBase):
	
	def __init__(self):
		npc.object.NpcBase.__init__(self)
		self.name = "异兽Npc"
	
	def doLook(self, who):
		content = '''我可以为你做点什么呢?
Q增加异兽寿命
Q设置异兽等级
Q增加异兽经验
Q设置异兽技能
Q增加异兽技能潜力点'''
		message.selectBoxNew(who, self.responseLook, content, self)
		
	def responseLook(self, who, selectNo):
		if selectNo == 1:
			self.selectPet(who, self.inputLife)
		elif selectNo == 2:
			self.selectPet(who, self.inputLevel)
		elif selectNo == 3:
			self.selectPet(who, self.inputExp)
		elif selectNo == 4:
			self.selectPet(who, self.inputSkill)
		elif selectNo == 5:
			self.selectPet(who, self.inputSkillPoint)
			
	def selectPet(self, who, func):
		txtList = []
		selList = []
		for petObj in who.petCtn.getAllValues():
			txtList.append("\nQ%s %d" % (petObj.name, petObj.level))
			selList.append(petObj.id)
		
		content = "请选择异兽：" + "".join(txtList)
		message.selectBoxNew(who, functor(self.responseSelectPet, selList, func), content, self)
		
	def responseSelectPet(self, who, selectNo, selList, func):
		if selectNo < 1 or selectNo > len(selList):
			return
		
		petId = selList[selectNo-1]
		petObj = who.petCtn.getItem(petId)
		if not petObj:
			return
		func(who, petObj)
		
	def inputLife(self, who, petObj):
		content = "异兽[#C02%s#n]的寿命为%d, 请输入要增加的寿命:" % (petObj.name, petObj.getLife())
		message.inputBox(who, functor(self.doAddLife, petObj.id), "增加异兽寿命", content, TYPE_LIMIT_INT)
		
	def doAddLife(self, who, responseVal, petId):
		petObj = who.petCtn.getItem(petId)
		if not petObj:
			return

		lifeAdded = int(responseVal)
		petObj.addLife(lifeAdded, "petHelper")
		
	def inputLevel(self, who, petObj):
		content = "异兽[#C02%s#n]的等级为%d, 请输入新的等级:" % (petObj.name, petObj.level)
		message.inputBox(who, functor(self.doSetLevel, petObj.id), "设置异兽等级", content, TYPE_LIMIT_INT)
		
	def doSetLevel(self, who, responseVal, petId):
		petObj = who.petCtn.getItem(petId)
		if not petObj:
			return
		levelNew = int(responseVal)
		if levelNew < 0:
			return
		
		levelAdd = levelNew - petObj.level
		if levelAdd == 0:
			message.tips(who, "异兽[#C02%s#n]已经是%d级" % (petObj.name, petObj.level))
			return
		
		if levelAdd < 0:
			petObj.add("level", levelAdd)
			petObj.attrChange("level")
			petObj.reCalcAttr()
		else:
			for i in xrange(levelAdd):
				petObj.exp += petObj.expNext
				petObj.upLevel()
		message.tips(who, "异兽[#C02%s#n]的等级成功设置为%d" % (petObj.name, petObj.level))
		
	def inputExp(self, who, petObj):
		content = "异兽[#C02%s#n]的经验为%d, 请输入要增加的经验:" % (petObj.name, petObj.exp)
		message.inputBox(who, functor(self.doAddExp, petObj.id), "增加异兽经验", content, TYPE_LIMIT_INT)
		
	def doAddExp(self, who, responseVal, petId):
		petObj = who.petCtn.getItem(petId)
		if not petObj:
			return
		expAdded = int(responseVal)
		petObj.rewardExp(expAdded, "petHelper")
		
	def inputSkillPoint(self, who, petObj):
		content = "异兽[#C02%s#n]的技能潜力点为%d, 请输入要增加的技能潜力点:" % (petObj.name, petObj.getSklPoint())
		message.inputBox(who, functor(self.doAddSkillPoint, petObj.id), "增加异兽技能潜力点", content, TYPE_LIMIT_INT)

	def doAddSkillPoint(self, who, responseVal, petId):
		petObj = who.petCtn.getItem(petId)
		if not petObj:
			return
		skillPoint = int(responseVal)
		petObj.addSklPoint(skillPoint, "petHelper")
		
	def inputSkill(self, who, petObj):
		skillIdList = petObj.fetch("skillList", [])
		skillInfo = ",".join([str(skillId) for skillId in skillIdList])
		content = "异兽[#C02%s#n]的现有技能:\n%s\n请输入要增加的技能:\n格式: 技能编号1,技能编号2,技能编号3..." % (petObj.name, skillInfo)
		message.inputBox(who, functor(self.doAddSkill, petObj.id), "设置异兽技能", content)

	def doAddSkill(self, who, responseVal, petId):
		petObj = who.petCtn.getItem(petId)
		if not petObj:
			return
		
		skillIdList = {}
		for skillId in responseVal.split(","):
			if not skillId:
				continue
			m = re.match("(\d+)=(\d+)", skillId)
			if m:
				skillId = int(m.group(1))
				level = int(m.group(2))
			else:
				skillId = int(skillId)
				level = 1
			skillIdList[skillId] = level
			
		if not skillIdList:
			message.tips(who, "格式错误")
			return
		
		for skillId, level in skillIdList.items():
			petObj.setSkill(skillId, level)
		
		petObj.reCalcAttr()
		message.tips(who, "设置异兽技能成功！")
	
from common import *
from props.defines import *
from qanda.defines import *
import message
import re