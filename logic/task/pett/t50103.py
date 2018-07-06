# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''句芒·金姝'''
	intro = '''被拒绝后，金姝叫你过去'''
	detail = '''正准备离开，鸠盘婆大弟子金姝却叫你过去，似乎有话要跟你说。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1020,E(1020,1061)'''
#导表结束