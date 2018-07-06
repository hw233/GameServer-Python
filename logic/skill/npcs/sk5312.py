# -*- coding: utf-8 -*-
from skill.object import NpcSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 5312
	name = "天狐媚术"
	performList = (5312,)
	score = 0
	applyList = {
		"lifeRatio":10,
	}
#导表结束
