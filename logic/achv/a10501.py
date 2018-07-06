# -*- coding: utf-8 -*-
from achv.defines import *
from achv.object import Achievement as CustomAchievement

#导表开始
class Achievement(CustomAchievement):
	kind = ACHV_KIND_PROG
	id = 10501
	name = "得道多助"
	point = 5
	totalProgress = 10
#导表结束