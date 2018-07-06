# -*- coding: utf-8 -*-
from task.defines import *
from task.demon.t10101 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 10101
	targetType = TASK_TARGET_TYPE_FIGHT
	title = '''厉魔任务'''
	intro = '''灭杀$target'''
	detail = '''灭杀$target'''
	initScript = '''N1002,E(1002,1002)'''
#导表结束