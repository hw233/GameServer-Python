# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第三章·旁门'''
	intro = '''通知武林盟后也四处搜索一番，却迎面遇见$target'''
	detail = '''通知武林盟后也四处搜索一番，却迎面遇见$target'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2025,NI2026,E(2025,2032),E(2026,2033)'''
#导表结束
	def onStartWar(self, w):
		if (w.isBoss() or w.isMonster()) and w.name == "旁门者甲":
			w.addFunc("onNewRound", self.onNewRound)

	def onNewRound(self, w):
		if w.bout == 1:
			w.war.say(w, self.getText(7006))