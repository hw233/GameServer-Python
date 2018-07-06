# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("仙盟战胜利",)
	conditionList = (

	)
	conditionScope = ""
	eventList = (
		"达成成就(40301)",
	)
#导表结束