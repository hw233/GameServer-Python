# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''云狐·治疗'''
	intro = '''给云狐上药后，送云狐回山'''
	detail = '''给云狐上药后，云狐的态度似乎略有缓和，与它交谈后送它回山吧。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1008,E(1008,1031)'''
#导表结束