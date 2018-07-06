# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''金鹏·回报'''
	intro = '''将灵药交给$target'''
	detail = '''把获得的灵药交给异兽仙子齐霞儿。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10208,1049)'''
#导表结束