# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("放弃任务",)
	conditionList = (
		(1,"任务类型==30001"),
	)
	conditionScope = ""
	eventList = (
		"中断成就进度(20101)",
	)
#导表结束