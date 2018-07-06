# -*- coding: utf-8 -*-
import npc.object

class cNpc(npc.object.cNpc):
	needLv = 25
	def doLook(self, who):
		content = self.getChat()
		content += "\nQ领取秘册任务"
		message.selectBoxNew(who, self.responseLook, content, self)
		
	def responseLook(self, who, selectNo):
		if selectNo == 1:
			self.giveTask(who)
			
	def giveTask(self, who):
		if who.level < self.needLv:
			self.say(who, "需要{}级才能领取秘册任务".format(self.needLv))
			return
		if task.hasTask(who, task.map.TASK_MAP_PARENT_ID):
			self.say(who, "天机不可过多泄露，你身上已有秘册任务，快去完成吧。")
			return
		if who.day.fetch("mapRing") >= 10:
			self.say(who, "秘册因逢际遇而得，你今天已经与它缘尽了，明天再来吧。")
			return
		if not who.isSingle():
			self.say(who, "秘册任务不可组队进行")
			return
		
		taskObj = task.newTask(who, self, task.map.TASK_MAP_PARENT_ID)
		taskObj.doScript(who, self, "D8001")


from common import *
import message
import task
import task.map
