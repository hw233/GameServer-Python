# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''金鹏·方法'''
	intro = '''面见妙一真人'''
	detail = '''面见妙一真人，询问医治金鹏之法。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10101,1041)'''
#导表结束