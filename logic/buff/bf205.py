# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "江海凝光"
	type = BUFF_TYPE_SPECIAL
	applyList = {
		"物理防御加成":10,
	}
	replacable = False
#导表结束