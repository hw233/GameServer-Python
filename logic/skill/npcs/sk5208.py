# -*- coding: utf-8 -*-
from skill.object import NpcSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 5208
	name = "高级增寿"
	performList = (5208,)
	score = 120
	applyList = {
		"hpMax":lambda LV:LV*5+60,
	}
#导表结束
