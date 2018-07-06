# -*- coding: utf-8 -*-
import npc.object

class cNpc(npc.object.cNpc):
	def doLook(self, who):
		content = self.getChat()
		selList = []
		content += "\nQ降魔任务"
		selList.append(1)
		if who.level >= 20:
			content += "\nQ便捷组队"
			selList.append(2)
		message.selectBoxNew(who, functor(self.responseLook, selList), content, self)
		
	def responseLook(self, who, selectNo, selList):
		if selectNo < 1 or selectNo > len(selList):
			return
		sel = selList[selectNo-1]
		if sel == 1:
			self.takeTask(who)
		elif sel == 2:
			self.speedyTeam(who)

	def takeTask(self, who):
		'''降魔任务
		'''
		taskObj = task.getTask(30101)
		if not taskObj:
			return
		if not taskObj.taskAddCheck(who, self):
			return
		if task.hasTask(who, 30101):
			return
		task.newTask(who, self, 30101, demonNpc=True)

	def speedyTeam(self, who):
		'''打开便捷组队界面
		'''
		team.platformservice.quickMakeTeam(who, team.platform.DEMON_TASK_NPC)


from common import *
import message
import task
import team.platformservice
import team.platform

