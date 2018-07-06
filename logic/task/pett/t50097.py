# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''毕方·担忧'''
	intro = '''寻找唐百草，询问是否介怀'''
	detail = '''毕方担心之前自己现出原形吓到唐百草夫妇，请你回去询问唐百草是否嫌恶毕方。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10204,1056)'''
#导表结束