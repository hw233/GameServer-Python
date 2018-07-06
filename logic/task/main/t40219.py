# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_ITEM
	icon = 0
	title = '''第一章·药草'''
	intro = '''寻购买$props以防毒蛇瘴气'''
	detail = '''寻购买$props以防毒蛇瘴气'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1018,L(221104,1),E(1018,1063)'''
#导表结束