# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6103
	name = "人物法防"
	applyList = {
		"被法术伤害结果加成":lambda SLV:-(2*SLV),
	}
#导表结束