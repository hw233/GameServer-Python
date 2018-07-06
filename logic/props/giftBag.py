#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

import props.object
class cProps(props.object.cProps):
	
	@property
	def level(self):
		return self.getConfig("等级")

	def use(self, who):#override
		'''使用
		'''
		if who.level<self.level:
			message.tips(who, '等级不足')
			return False

		propsList = []
		propsAmountList = {}
		rewardList = giftBagData.getBagData(self.no())
		for propsData in rewardList:
			propsNo,amount,isBind,dArgs = self.parserInfo(who, propsData)
			propsList.append( (propsNo,amount,isBind,dArgs) )
			propsAmountList[propsNo] = amount

		if not who.propsCtn.validCapacity(propsAmountList):
			message.tips(who,"包裹格子不足，为防止奖励丢失，请先清理背包")
			return False

		who.propsCtn.addStack(self,-1)
		for propsNo,amount,isBind,dArgs in propsList:
			launch.launchBySpecify(who,propsNo,amount,isBind,"等级礼包",None,**dArgs)

		return True

	def parserInfo(self, who, propsData):
		'''解析信息
		'''
		amount = propsData["数量"]
		isBind = propsData.get("绑定",0)
		propsNo = propsData["物品"]
		effect = propsData.get("效果")
		if propsNo < 10000:
			propsNo,effect = self.transByBranch(who,propsNo,propsData["条件类型"])

		return propsNo,amount,isBind,self.transEffect(effect)
			
	def transByBranch(self, who, branchNo, flag):
		'''根据分支转换
		'''
		condition = self.getBranchCondition(who,flag)
		branchDataList = giftBagData.getBranchData(branchNo)
		for branchData in branchDataList:
			if branchData["条件"] == condition:
				return branchData["物品"],branchData.get("效果")
		raise PlannerError("礼包分支{}找不到{}为{}的数据".format(branchNo,flag,condition))

	def getBranchCondition(self, who, flag):
		'''获得分支条件
		'''
		if flag == "造型":
			return who.fetch("shape",1111)
		elif flag == "性别":
			return who.gender
		return 0

	def transEffect(self, effect):
		'''转换效果
		'''
		if not effect:
			return {}
		effectList = {}
		for desc,attr in baseDescAttr.iteritems():
			value  = effect.get(desc)
			if value:
				baseAttr = effectList.setdefault("baseAttr",{})
				baseAttr[attr] = value
		for desc,attr in addDescAttr.iteritems():
			value  = effect.get(desc)
			if value:
				addAttr = effectList.setdefault("addAttr",{})
				addAttr[attr] = value
		for desc,attr in otherDescAttr.iteritems():
			value  = effect.get(desc)
			if value:
				effectList[attr] = value

		return effectList
		
from props.defines import *
import common
import message
import launch
import giftBagData
import u