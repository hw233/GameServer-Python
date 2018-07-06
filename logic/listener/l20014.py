# -*- coding: utf-8 -*-
from listener.defines import *
from listener.object import Listener as CustomListener

#导表开始
class Listener(CustomListener):
	eventTypeList = ("升级门派技能",)
	conditionList = (
		(1,"所有门派技能等级>=80"),
	)
	conditionScope = ""
	eventList = (
		"达成成就(10303)",
	)
#导表结束