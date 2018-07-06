# -*- coding: utf-8 -*-
'''宠物相关物品
'''
import props.object

class cProps(props.object.cProps):
	
	def isExp(self):
		'''是否异兽经验物品
		'''
		effectList = self.getEffect()
		return "异兽经验" in effectList
	
	def isLife(self):
		'''是否异兽寿命物品
		'''
		effectList = self.getEffect()
		return "寿命" in effectList
	
	def useForPet(self, who, petObj, count):
		effectList = self.getEffect()
		if "异兽经验" in effectList:
			if not petObj.checkRewardExp("宠物培养"):
				return
			val = int(effectList["异兽经验"])
			func = self.tryAddExp
			tips = "本异兽增加了{}经验"
			petObj.addExpResult = 0
		elif "寿命" in effectList:
			if petObj.isHolyPet():
				message.tips(who, "神兽为永生之体，无需增添寿命")
				return
			if not petObj.checkAddLife("宠物培养"):
				return
			val = int(effectList["寿命"])
			func = self.tryAddLife
			tips = "本异兽增加了{}寿命"
			petObj.addLifeResult = 0
		else:
			return
		
		result = 0
		count = min(count, self.stack())
		for i in xrange(count):
			if not func(who, petObj, count, val):
				break
			
		if hasattr(petObj, "addExpResult"):
			result = petObj.addExpResult
			del petObj.addExpResult
		elif hasattr(petObj, "addLifeResult"):
			result = petObj.addLifeResult
			del petObj.addLifeResult
		else:
			return
		message.tips(who, tips.format(result))
		
	def tryAddExp(self, who, petObj, count, exp):
		if not petObj.checkRewardExp("宠物培养", False):
			return 0
		who.propsCtn.addStack(self, -1)
		petObj.rewardExp(exp, "宠物培养", None)
		return 1
		
	def tryAddLife(self, who, petObj, count, life):
		if not petObj.checkAddLife("宠物培养", False):
			return 0
		who.propsCtn.addStack(self, -1)
		petObj.addLife(life, "宠物培养", None)
		return 1

import message