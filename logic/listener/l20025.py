# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("开宝图",)
	conditionList = (
		(1,"事件名==放妖"),
	)
	conditionScope = ""
	eventList = (
		"增加成就进度(20301,1)",
	)
#导表结束