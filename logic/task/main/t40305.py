# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·佛门方丈'''
	intro = '''追云叟还要拖拉地讨论人选，不如先行一步去找$target吧'''
	detail = '''追云叟还要拖拉地讨论人选，不如先行一步去找$target吧'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''NI1510,E(10106,1517),E(1510,1518)'''
#导表结束