# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "魔宫弟子"
	type = BUFF_TYPE_SPECIAL
	applyList = {
		"法术伤害结果加成":10,
	}
#导表结束