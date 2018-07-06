# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第三章·保护'''
	intro = '''一群$target看见余英男冻僵的躯体，准备大快朵颐，快去保护'''
	detail = '''一群$target看见余英男冻僵的躯体，准备大快朵颐，快去保护'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2017,NI2018,NI2019,E(2017,2023),E(2018,2024),E(2019,2025)'''
#导表结束