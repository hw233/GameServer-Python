# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_FIGHT
	icon = 1
	title = '''第二章·放火（二）'''
	intro = '''火势还嫌不够猛烈，四处找找还能点着些什么'''
	detail = '''火势还嫌不够猛烈，四处找找还能点着些什么'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''ANLEI(1524,1537,1130)'''
#导表结束