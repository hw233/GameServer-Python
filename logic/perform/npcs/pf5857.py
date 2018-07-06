# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5817 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5857
	name = "高级指挥减伤"
	configInfo = {
		"被物理伤害结果":-40,
		"被法术伤害结果":-40,
	}
#导表结束