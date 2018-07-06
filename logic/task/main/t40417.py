# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第三章·两矮'''
	intro = '''依武林盟众所说，到达山阴处果然发现$target'''
	detail = '''依武林盟众所说，到达山阴处果然发现$target'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2031,NI2032,E(2031,2040),E(2032,2041)'''
#导表结束