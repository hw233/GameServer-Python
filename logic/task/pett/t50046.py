# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''文雀·得救'''
	intro = '''解救文雀后，回报仙子'''
	detail = '''原来文雀吃了杜仲后虚软无力，才被修士抓住。解救文雀后，回去与仙子对话。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10208,1026)'''
#导表结束