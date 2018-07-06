#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

import props.object
class cProps(props.object.cProps):

	def use(self, who):#override
		'''使用
		'''
		propsList = self.getConfig("效果")["组编号"]
		if who.propsCtn.leftCapacity() < len(propsList):
			message.tips(who,"包裹格子不足，为防止奖励丢失，请先清理背包")
			return False
		who.propsCtn.addStack(self,-1)

		for groupNum in propsList:
			propsDataList = giftBagData.getGemBagData(groupNum)
			propsId = common.chooseKey(propsDataList, key="权重")
			propsNo,amount,isBind = self.parserInfo(who, propsDataList[propsId])
			amount = self.calAmount(who, amount)
			launch.launchBySpecify(who,propsNo,amount,isBind,"宝石袋",None)
		return True

	def parserInfo(self, who, propsData):
		'''解析信息
		'''
		propsNo = propsData["物品"]
		amount = propsData["数量"]
		isBind = propsData.get("绑定",0)
		return propsNo,amount,isBind
	
	def calAmount(self, who, amount):
		'''银币袋子、元宝袋子每周前五个使用amount增加%10
		'''
		if self.idx not in amountRatio:
			return amount

		flag = "p{}".format(self.idx)
		if who.week.fetch(flag) < 5:
			who.week.add(flag, 1)
			ratio = amountRatio[self.idx]
			amount = amount * (100 + ratio) / 100

		return amount


amountRatio = {
	202061: 10, #银币袋子
	202062: 10, #元宝袋子
}

from props.defines import *
import common
import message
import launch
import giftBagData