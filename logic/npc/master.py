# -*- coding: utf-8 -*-
import npc.object

class cNpc(npc.object.cNpc):
	
	def doLook(self, who):
		chat = self.getChat()
		taskObj = task.getTask(30001)
		minLv = min(taskObj.ringTask.keys()) if taskObj else 0
		if who.school != self.school or minLv > who.level:
			if chat:
				self.say(who, chat)
			return
				
		txtList= []
		selList = []
		if chat:
			txtList.append(chat)

		if not task.hasTask(who, 30001):
			txtList.append("Q领取师门任务")
			selList.append(1)
		
		content = "\n".join(txtList)
		if selList:
			message.selectBoxNew(who, functor(self.responseLook, selList), content, self)
		else:
			self.say(who, content)
		
	def responseLook(self, who, selectNo, selList):
		if selectNo < 1 or selectNo > len(selList):
			return
		sel = selList[selectNo-1]
		if sel == 1:
			self.giveTask(who)
			
	def giveTask(self, who):
		if task.hasTask(who, 30001):
			message.tips(who, "你已有任务")
			return
		if who.day.fetch("schoolRing") >= 20:
			message.tips(who, "今天完成师门任务次数已达上限")
			return
		if task.school.randSchoolTask(who, self):
			message.tips(who, "领取师门任务成功")
		else:
			message.tips(who, "没有适合的师门任务可以接取")

from common import *
import message
import task
import task.school