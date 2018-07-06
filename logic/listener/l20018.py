# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("打造装备",)
	conditionList = (

	)
	conditionScope = ""
	eventList = (
		"达成成就(10601)",
	)
#导表结束