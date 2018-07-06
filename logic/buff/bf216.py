# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "四座无言"
	type = BUFF_TYPE_SPECIAL
	applyList = {
		"法术伤害结果加成":-5,
		"":True,
		"治疗结果加成":-5,
	}
	replacable = False
#导表结束