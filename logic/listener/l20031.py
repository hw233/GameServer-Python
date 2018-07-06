# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("增加银币",)
	conditionList = (
		(1,"人物等级>=8"),
	)
	conditionScope = ""
	eventList = (
		"增加成就进度(10201,货币值)",
		"增加成就进度(10202,货币值)",
		"增加成就进度(10203,货币值)",
	)
#导表结束