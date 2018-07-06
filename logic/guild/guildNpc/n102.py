# -*- coding: utf-8 -*-
from guild.object import Npc as CustomNpc

#导表开始
class Npc(CustomNpc):
	idx = 102
	name = "盟战接引"
	typeName = "帮战"
	pos = (75,29,6)
	shape = 4502
	shapeParts = [0, 1, 0, 0, 0, 0]
	colors = [0, 0, 0, 0, 0]
	chatList = (130201,)
#导表结束

	def doLook(self, who):
		content = self.getChat()
		content += '''
Q进入仙盟大战'''
		message.selectBoxNew(who, self.responseLook, content, self)
			
	def responseLook(self, who, selectNo):
		if selectNo == 1:
			actObj = activity.getActivity("guildFight")
			if actObj:
				actObj.enterScene(who, self)
			

import activity
import message