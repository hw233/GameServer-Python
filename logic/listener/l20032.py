# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("摆摊提现",)
	conditionList = (

	)
	conditionScope = ""
	eventList = (
		"增加成就进度(10204,货币值)",
		"增加成就进度(10205,货币值)",
		"增加成就进度(10206,货币值)",
	)
#导表结束