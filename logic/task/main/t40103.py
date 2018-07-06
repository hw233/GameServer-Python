# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第二章·大师兄'''
	intro = '''在桥的另一端……是$target？'''
	detail = '''在桥的另一端……是$target？'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N2003,NI2004,E(2003,2003),E(2004,2004)'''
#导表结束