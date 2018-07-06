# -*- coding: utf-8 -*-
'''
仙盟资金
'''
import props.virtual


class cProps(props.virtual.cProps):
	def use(self, who):
		val = self.getValue()
		guildObj = who.getGuildObj()
		if not guildObj:
			return
		ret = guildObj.addFund(val)
		if ret > 0:
			message.message(who, "你的仙盟资金增加了#R<{},12,2>#n".format(ret))
		else:
			message.message(who, "你的仙盟每日增加资金已达上限")


import message
