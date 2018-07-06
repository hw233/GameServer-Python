# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "九幽聚法"
	type = BUFF_TYPE_BUFF
	applyList = {
		"法术伤害结果加成":15,
	}
#导表结束