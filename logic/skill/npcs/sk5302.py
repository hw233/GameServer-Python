# -*- coding: utf-8 -*-
from skill.object import NpcSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 5302
	name = "龟甲秘术"
	performList = (5302,)
	score = 0
	applyList = {
		"magDamRatio":10,
	}
#导表结束
