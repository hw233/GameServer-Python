# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·英男'''
	intro = '''下蜀山的路上你遇到一名旅者，心灵一动，似乎所需就是眼前人'''
	detail = '''下蜀山的路上你遇到一名旅者，心灵一动，似乎所需就是眼前人'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1017,E(1017,1058)'''
#导表结束