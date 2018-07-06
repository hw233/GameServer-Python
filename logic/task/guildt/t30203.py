# -*- coding: utf-8 -*-
from task.defines import *
from task.guildt.t30201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30201
	targetType = TASK_TARGET_TYPE_FIGHT
	icon = 1
	title = '''仙盟-守卫巡逻'''
	intro = '''在仙盟领地巡逻'''
	detail = '''近日仙盟常丢失物件，看来是飞贼作乱，你去守卫巡逻一下。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''ANLEI(1001,1003,guild)'''
#导表结束