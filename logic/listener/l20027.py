# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("创建仙盟",)
	conditionList = (

	)
	conditionScope = ""
	eventList = (
		"达成成就(40101)",
	)
#导表结束