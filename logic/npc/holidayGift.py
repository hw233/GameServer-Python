# -*- coding: utf-8 -*-
import npc.object

class cNpc(npc.object.cNpc):

	def doLook(self, who):
		content = self.getChat()
		content += '''
Q领取大礼'''
		message.selectBoxNew(who, self.responseLook, content, self)
		
	def responseLook(self, who, selectNo):
		if selectNo == 1:
			holiday.service.rpcHolidayUI(who)


from common import *
import holiday.service
import message