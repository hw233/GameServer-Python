# -*- coding: utf-8 -*-
import npc.object

class cNpc(npc.object.cNpc):
	def doLook(self, who):
		content = self.getChat()
		selList = []

		actObj = activity.instance.getActivity()
		minLevel = 999
		for _,info in actObj.instanceData.iteritems():
			level = info.get("显示等级", 0)
			if level < minLevel:
				minLevel = level
		
		if who.level >= minLevel:
			content += "\nQ选择副本"
			selList.append(1)

			content += "\nQ便捷组队"
			selList.append(2)

		message.selectBoxNew(who, functor(self.responseLook, selList), content, self)
		
	def responseLook(self, who, selectNo, selList):
		if selectNo < 1 or selectNo > len(selList):
			return
		sel = selList[selectNo-1]

		if sel == 1:
			openUIPanel.rpcOpenUIPanel(who, 59)
		elif sel == 2:
			self.speedyTeam(who)

	def speedyTeam(self, who):
		'''打开便捷组队界面
		'''
		team.platformservice.quickMakeTeam(who, team.platform.INSTANCE_TASK_NPC)


from common import *
import message
import activity.instance
import team
import openUIPanel