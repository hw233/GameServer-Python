# -*- coding: utf-8 -*-
'''五宝兑换
'''
import npc.object

needList = {202001:1, 202002:1, 202003:1, 202004:1, 202005:1}  # 所需物品
exchangeList = {202007:1} # 兑换物品

class cNpc(npc.object.cNpc):

	def doLook(self, who):
		content = self.getChat()
		content += '''
Q兑换五珠'''
		message.selectBoxNew(who, self.responseLook, content, self)
		
	def responseLook(self, who, selectNo):
		if selectNo == 1:
			self.exchange(who)

	def exchange(self, who):
		'''兑换五珠
		'''
		for propsNo, amount in needList.iteritems():
			if not who.propsCtn.hasPropsByNo(propsNo):
				self.say(who, "唔，没集齐五颗龙珠，那天机也不可泄露，请回吧")
				return
		for propsNo, amount in needList.iteritems():
			who.propsCtn.subPropsByNo(propsNo, amount, "兑换五珠")
		for propsNo, amount in exchangeList.iteritems():
			launch.launchBySpecify(who, propsNo, amount, False, "兑换五珠")
		message.tips(who,"兑换大衍藏宝秘册成功")

from common import *
import message
import launch
