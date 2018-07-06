# -*- coding: utf-8 -*-
from achv.defines import *
from achv.object import Achievement as CustomAchievement

#导表开始
class Achievement(CustomAchievement):
	kind = ACHV_KIND_PROG
	id = 10205
	name = "摆摊能手"
	point = 10
	totalProgress = 1000000
#导表结束