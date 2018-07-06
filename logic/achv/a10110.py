# -*- coding: utf-8 -*-
from achv.defines import *
from achv.object import Achievement as CustomAchievement

#导表开始
class Achievement(CustomAchievement):
	kind = ACHV_KIND_COMMON
	id = 10110
	name = "笑傲江湖"
	point = 15
	eventList = (
		"给予称谓(60101)",
	)
#导表结束