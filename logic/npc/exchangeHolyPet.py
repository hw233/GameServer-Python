# -*- coding: utf-8 -*-
'''宠物兑换
'''
import npc.object


class cNpc(npc.object.cNpc):

	def doLook(self, who):
		content = self.getChat()
		content += '''
Q兑换'''
		message.selectBoxNew(who, self.responseLook, content, self)
		
	def responseLook(self, who, selectNo):
		if selectNo == 1:
			who.endPoint.rpcPetHolyExchangeShow()
		
import message
