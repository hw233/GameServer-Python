# -*- coding: utf-8 -*-
from skill.object import NpcSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 5108
	name = "增寿"
	performList = (5108,)
	score = 60
	applyList = {
		"hpMax":lambda LV:LV*2.5+30,
	}
#导表结束
