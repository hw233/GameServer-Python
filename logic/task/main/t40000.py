# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NONE
	icon = 0
	title = '''角色升级'''
	intro = '''达到$level级开启新剧情'''
	detail = '''达到$level级开启新剧情'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = ''''''
#导表结束

	def transString(self, content, pid=0):
		'''转化字符串
		'''
		who = None
		if pid:
			who = getRole(pid)

		if who:
			if '$level' in content:
				content = content.replace("$level", str(who.level/10*10+10))

		return customTask.transString(self, content, pid)

from common import *