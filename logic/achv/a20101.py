# -*- coding: utf-8 -*-
from achv.defines import *
from achv.object import Achievement as CustomAchievement

#导表开始
class Achievement(CustomAchievement):
	kind = ACHV_KIND_PROG
	id = 20101
	name = "师傅请吩咐"
	point = 5
	totalProgress = 100
#导表结束