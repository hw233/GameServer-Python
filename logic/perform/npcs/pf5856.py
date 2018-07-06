# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5816 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5856
	name = "高级指挥防护"
	configInfo = {
		"被物理伤害结果加成":-5,
		"被法术伤害结果加成":-5,
	}
#导表结束