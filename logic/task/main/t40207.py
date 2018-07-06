# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·去留'''
	intro = '''在村中心，$target正在等你'''
	detail = '''在村中心，$target正在等你'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1005,NI1006,NI1007,E(1005,1027),E(1006,1028),E(1007,1029)'''
#导表结束