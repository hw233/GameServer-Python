# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''云狐·援救'''
	intro = '''$target请你解救云狐'''
	detail = '''仙子察觉云狐被抓到城中，请你前去解救它，送它回山。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10208,1027)'''
#导表结束