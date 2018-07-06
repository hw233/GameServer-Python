# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第三章·决心'''
	intro = '''好不容易才逃出来，$target一副满怀心事的样子'''
	detail = '''好不容易才逃出来，$target一副满怀心事的样子'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2010,E(2010,2014)'''
#导表结束