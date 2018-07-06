#-*-coding:utf-8-*-

import props.object
class cProps(props.object.cProps):
	def use(self,who):#override
		iAdd=self.getConfig('universal1',0)
		if not isinstance(iAdd,(int,long)):
			raise Exception,'经验丹的"通用字段1"必须是一个整数'
		
		if hasattr(who, "eatAmount"):
			eatAmount = who.eatAmount
			del who.eatAmount
		else:
			eatAmount = 1

		for i in xrange(eatAmount):
			if who.level==who.getMaxLevel():
				message.tips(who, '经验已达到最大值')
				return False
			who.propsCtn.addStack(self,-1)
			who.rewardExp(iAdd,'expPill')
		return True

import roleAttrData
import message