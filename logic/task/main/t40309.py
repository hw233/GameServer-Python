# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第二章·杀与不杀'''
	intro = '''$target认为要杀掉他们，那究竟如何选择'''
	detail = '''$target认为要杀掉他们，那究竟如何选择'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1513,E(1513,1525)'''
#导表结束

	
	def onStartWar(self, w):
		if (w.isBoss() or w.isMonster()) and w.name == "左清虚":
			w.war.say(w, "这个是……蜀山、唐门一派的人？！")