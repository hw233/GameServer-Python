# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("人物升级",)
	conditionList = (
		(1,"人物等级==50"),
	)
	conditionScope = ""
	eventList = (
		"达成成就(10105)",
	)
#导表结束