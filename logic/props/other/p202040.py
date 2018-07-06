# -*- coding: utf-8 -*-
'''
改名(赠送)
'''
import props.object

class cProps(props.object.cProps):
	def use(self, who):#override
		#赠送的改名卡有使用限制
		if who.level > 40 and who.level > openLevel.getOpenLevel() - 10:
			message.tips(who, "等级≤40或者低于服务器等级上限10级时才可使用")
			return
		role.service.rpcReNameNotify(who, self.id, 3)


import message
import openLevel
import role.service
