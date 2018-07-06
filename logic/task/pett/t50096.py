# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''毕方·实情'''
	intro = '''返回询问毕方'''
	detail = '''教训完地痞后，询问毕方为何要帮助唐百草。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1018,E(1018,1055)'''
#导表结束