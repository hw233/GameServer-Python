# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第一章·小人'''
	intro = '''果然有$target被惊出来了，金蝉喊着要包围它'''
	detail = '''果然有$target被惊出来了，金蝉喊着要包围它'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1012,NI1013,E(1012,1048),E(1013,1049)'''
#导表结束