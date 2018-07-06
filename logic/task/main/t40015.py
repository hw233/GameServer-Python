# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_FIGHT
	icon = 1
	title = '''第一章·巡逻'''
	intro = '''刚刚的家伙一哄而散，四处巡逻一下以免他们回来'''
	detail = '''刚刚的家伙一哄而散，四处巡逻一下以免他们回来'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''ANLEI(1011,1018,1140)'''
#导表结束