# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NONE
	icon = 0
	title = '''第三章·未完待续'''
	intro = '''当前主线任务已暂告一段落，新的剧情敬请期待'''
	detail = '''当前主线任务已暂告一段落，新的剧情敬请期待'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''$toast8000'''
#导表结束