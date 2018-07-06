# -*- coding: utf-8 -*-
'''
染色NPC
'''
import npc.object

class cNpc(npc.object.cNpc):

	def doLook(self, who):
		content = self.getChat()
		content += '''
Q我要染色'''
		message.selectBoxNew(who, self.responseLook, content, self)
		
	def responseLook(self, who, selectNo):
		if selectNo == 1:
			dye.service.rpcDyeUI(who)


from common import *
import dye.service
import message