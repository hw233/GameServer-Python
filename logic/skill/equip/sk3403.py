# -*- coding: utf-8 -*-
from skill.object import EquipSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 3403
	name = "同尘"
	performList = (3403,)
	score = 30
	applyList = {
		"hpMax":lambda LV:100+LV*2,
	}
#导表结束
