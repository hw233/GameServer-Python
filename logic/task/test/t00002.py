# -*- coding: utf-8 -*-
from task.defines import *
from task.test.t00001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 1
	targetType = TASK_TARGET_TYPE_FIGHT
	icon = 1
	title = '''测试暗雷战斗'''
	intro = '''去$scene收集$props'''
	detail = '''师门$props消耗过大，去$scene收集一些。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''L(9001,1),ANLEI(1001,1002,9003)'''
#导表结束