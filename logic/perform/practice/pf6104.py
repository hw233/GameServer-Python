# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6104
	name = "人物抗封"
	applyList = {
		"抵抗封印":lambda SLV:2*SLV,
	}
#导表结束