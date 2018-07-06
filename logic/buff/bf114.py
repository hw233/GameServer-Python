# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "隐身闭气"
	type = BUFF_TYPE_BUFF
	applyList = {
		"隐身":True,
	}
#导表结束