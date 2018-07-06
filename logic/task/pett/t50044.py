# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''文雀·意外'''
	intro = '''把杜仲交给文雀后，回去禀报仙子'''
	detail = '''把杜仲交给文雀后，回去与仙子交谈，汇报情况。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10208,1024)'''
#导表结束