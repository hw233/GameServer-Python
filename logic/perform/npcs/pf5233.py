# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5133 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5233
	name = "高级慧眼"
	applyList = {
		"破隐":True,
	}
	configInfo = {
		"概率":50,
	}
#导表结束