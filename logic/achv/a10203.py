# -*- coding: utf-8 -*-
from achv.defines import *
from achv.object import Achievement as CustomAchievement

#导表开始
class Achievement(CustomAchievement):
	kind = ACHV_KIND_PROG
	id = 10203
	name = "亿万富翁"
	point = 15
	totalProgress = 100000000
	eventList = (
		"给予称谓(60151)",
	)
#导表结束