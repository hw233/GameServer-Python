# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_ITEM
	icon = 0
	title = '''第三章·续命'''
	intro = '''丁引分了点朱果，快点拿去给$target食用'''
	detail = '''丁引分了点朱果，快点拿去给$target食用'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''R1493,N2024,L(203016,1),E(2024,2031)'''
#导表结束