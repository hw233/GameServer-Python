# -*- coding: utf-8 -*-
from perform.defines import *
from perform.school.pf1211 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6201
	name = "风雷弹"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	damage = lambda self,SLV:SLV*2+20
	power = 100
	configInfo = {
		"治疗":lambda SLV:SLV*2+150,
		"治疗威力":100,
		"目标数":5,
	}
#导表结束