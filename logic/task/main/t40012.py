# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·旧事'''
	intro = '''$target似乎知道些什么，向他了解蜀山的过去'''
	detail = '''$target似乎知道些什么，向他了解蜀山的过去'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N1009,E(1009,1015)'''
#导表结束