# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "御蝎秘术"
	type = BUFF_TYPE_BUFF
	applyList = {
		"抗封":True,
	}
#导表结束