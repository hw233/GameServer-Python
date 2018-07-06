# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''云狐·回返'''
	intro = '''送云狐回山后，回去告诉仙子'''
	detail = '''送走云狐后，回去向仙子汇报。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10208,1032)'''
#导表结束