# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "天寒日暮"
	type = BUFF_TYPE_SPECIAL
	applyList = {
		"法术防御加成":-10,
	}
	replacable = False
#导表结束