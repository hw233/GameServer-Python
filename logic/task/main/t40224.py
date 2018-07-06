# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第一章·斩蛇'''
	intro = '''既然$target被激怒回来，那就不能错失机会，斩妖除魔吧！'''
	detail = '''既然$target被激怒回来，那就不能错失机会，斩妖除魔吧！'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1026,E(1026,1071)'''
#导表结束