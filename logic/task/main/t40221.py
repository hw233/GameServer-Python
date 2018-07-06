# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第一章·妖蛇'''
	intro = '''$target破关而出，正往这里扑来，赶快迎击'''
	detail = '''$target破关而出，正往这里扑来，赶快迎击'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1024,E(1024,1066)'''
#导表结束