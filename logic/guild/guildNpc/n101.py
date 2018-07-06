# -*- coding: utf-8 -*-
from guild.object import Npc as CustomNpc

TASK_ID = 30201

#导表开始
class Npc(CustomNpc):
	idx = 101
	name = "仙盟总管"
	typeName = "总管"
	pos = (61,36,6)
	shape = 4502
	shapeParts = [0, 1, 0, 0, 0, 0]
	colors = [0, 0, 0, 0, 0]
	chatList = (130200,)
#导表结束

	def doLook(self, who):
		selList = []
		content = self.getChat()
		if not task.hasTask(who, TASK_ID):
			content += "\nQ仙盟任务"
			selList.append(1)
		
		content += "\nQ剩余环数"
		selList.append(2)
		
		guildObj = self.guild
		if guildObj.getJob(who.id) == GUILD_JOB_CHAIRMAN:
			if guildObj.fetch("dismissApply"):
				content += "\nQ取消帮派解散"
				selList.append(4)
			if guildObj.fetch("dismissCheck"):
				content += "\nQ确认帮派解散"
				selList.append(3)

		content += "\nQ打个招呼"
		selList.append(5)

		message.selectBoxNew(who, functor(self.responseLook, selList), content, self)

	def responseLook(self, who, selectNo, selList):
		if selectNo < 1 or selectNo > len(selList):
			return
		sel = selList[selectNo-1]
		if sel == 1:
			self.takeTask(who)
		elif sel == 2:
			self.queryTask(who)
		elif sel == 3:
			self.confirmDismiss(who)
		elif sel == 4:
			self.cancelDismiss(who)

	def takeTask(self, who):
		if task.hasTask(who, TASK_ID):
			return
		if who.level < 20:
			message.tips(who, "领取任务需要等级＞=25")
			return
		if not task.guildt.canTakeGuildTask(who):
			message.tips(who, "今日可完成仙盟任务次数已达到上限，请明天再来吧")
			return
		
		bLastRing = False
		if who.taskCtn.fetch("guildRing") == 9:
			bLastRing = True
			
		taskObj = task.guildt.randGuildTask(who, self, bLastRing)

	def queryTask(self, who):
		maxCnt = getDatePart(partName="wday") * 20
		weekRing = who.week.fetch("guildRing")
		surplus = 140 - weekRing
		number = maxCnt - weekRing
		content = "掐指一算，你剩余的仙盟任务还有{}环，今日合共可完成{}环。".format(surplus, number)
		self.say(who, content)

	def cancelDismiss(self, who):
		'''取消帮派解散
		'''
		guild.service.dismissCancel(who)

	def confirmDismiss(self, who):
		'''确认帮派解散
		'''
		guild.service.dismissConfirm(who)

from common import *
from guild.defines import *
import message
import task
import guild.service
