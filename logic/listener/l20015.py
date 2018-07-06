# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("学习阵法",)
	conditionList = (

	)
	conditionScope = ""
	eventList = (
		"达成成就(10401)",
	)
#导表结束