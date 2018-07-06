# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "媚术·守"
	type = BUFF_TYPE_BUFF
	applyList = {
		"被物理伤害结果加成":-10,
		"被法术伤害结果加成":-10,
	}
#导表结束