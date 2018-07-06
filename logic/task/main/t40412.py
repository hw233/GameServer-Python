# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第三章·夺朱果'''
	intro = '''商议后，大家认为时间已经不多，击败$target，强夺朱果吧'''
	detail = '''商议后，大家认为时间已经不多，击败$target，强夺朱果吧'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2023,E(2023,2029)'''
#导表结束
	def onStartWar(self, w):
		if (w.isBoss() or w.isMonster()) and w.name == "山魈":
			w.addFunc("onNewRound", self.onNewRound)

	def onNewRound(self, w):
		if w.bout == 1:
			w.war.say(w, self.getText(7005))