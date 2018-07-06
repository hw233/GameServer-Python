# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·莽苍变'''
	intro = '''唐门$target匆匆赶来，似乎有什么事要说'''
	detail = '''唐门$target匆匆赶来，似乎有什么事要说'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1554,NI1553,NI1552,NI1551,E(1554,1576),E(1553,1577),E(1552,1575),E(1551,1569)'''
#导表结束
	
	def customEvent(self, who, npcObj, eventName, *args):
		if eventName == "weapon":
			info = self.getConfigInfo()
			launch.launchBySpecify(who, info[who.shape], 1, False, self.name)

import launch