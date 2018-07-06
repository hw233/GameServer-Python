# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("人物升级",)
	conditionList = (
		(1,"人物等级==15"),
		(2,"拥有任务类型(30000)==0"),
	)
	conditionScope = ""
	eventList = (
		"给予任务(30000)",
	)
#导表结束