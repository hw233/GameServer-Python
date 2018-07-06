# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "唐门弟子"
	type = BUFF_TYPE_SPECIAL
	applyList = {
		"抵抗封印":10,
	}
#导表结束