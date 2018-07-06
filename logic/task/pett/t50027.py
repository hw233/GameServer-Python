# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_FIGHT
	icon = 1
	title = '''灵蜂女·挟持'''
	intro = '''击败心术不正之人，救出灵蜂女'''
	detail = '''这人受伤是假的！他为了得到能够治愈病痛的灵蜜，设计抓住了灵蜂女，得赶紧把她救下！'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1003,E(1003,1011)'''
#导表结束