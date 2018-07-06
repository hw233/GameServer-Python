# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·灵云'''
	intro = '''金蝉的二姐$target到来了，与她交谈'''
	detail = '''金蝉的二姐$target到来了，与她交谈'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''STORY40011,N1016,NI1014,NI1015,E(1016,1055),E(1014,1056),E(1015,1057)'''
#导表结束