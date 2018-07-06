# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("仙盟强盗胜利",)
	conditionList = (

	)
	conditionScope = ""
	eventList = (
		"增加成就进度(40201,1)",
	)
#导表结束