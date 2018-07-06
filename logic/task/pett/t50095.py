# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''毕方·地痞'''
	intro = '''教训想要抢走羽衣的地痞'''
	detail = '''唐百草说羽衣是她义女所织，这时城里的地痞们出现，想要抢走羽衣。教训他们。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1017,E(1017,1054)'''
#导表结束