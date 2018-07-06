# -*- coding: utf-8 -*-
from skill.object import NpcSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 5309
	name = "凤舞回元"
	performList = (5309,)
	score = 0
	applyList = {
		"speRatio":15,
	}
#导表结束