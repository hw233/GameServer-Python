# -*- coding: utf-8 -*-
from task.defines import *
from task.bamboo.t30401 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30401
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''竹林除妖'''
	intro = '''战胜$target'''
	detail = '''找到了僵尸们的头领，快消灭僵尸头领'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1006,E(1006,1004)'''
#导表结束
	

	def onAddWarrior(self, w):
		'''主怪物僵尸头领出手攻击了3次后，会在下一回合开始前增加一个BUFF“狂暴”，伤害增加50%
		'''
		if w.isMonster() and w.name == "僵尸头领":
			w.attCnt = 0	#记录出手攻击次数
			w.addFunc("onEndRound", self.onEndRound)

	def onEndRound(self, w):
		if w.isMonster() and w.name == "僵尸头领":
			w.attCnt += 1
			if w.attCnt == 3:
				w.addApply("物理伤害结果加成", 50)
				w.addApply("法术伤害结果加成", 50)
				w.war.say(w, self.getText(2001))
			








