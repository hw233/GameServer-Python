# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NONE
	icon = 0
	title = '''第二章·未待续完'''
	intro = '''当前主线任务已暂告一段落，新的剧情敬请期待'''
	detail = '''当前主线任务已暂告一段落，新的剧情敬请期待'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = ''''''
#导表结束

	def goAhead(self, who):
		'''前往
		'''
		message.tips(who, self.getText(8000, who.id))

import message
