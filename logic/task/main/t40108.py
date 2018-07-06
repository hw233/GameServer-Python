# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·再上蜀山'''
	intro = '''$target在蜀山山脚，与她说话'''
	detail = '''师妹$target在蜀山山脚，与她说话'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N2007,E(2007,2009)'''
#导表结束