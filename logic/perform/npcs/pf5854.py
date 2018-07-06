# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5814 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5854
	name = "高级指挥加速"
	configInfo = {
		"速度加成":5,
	}
#导表结束