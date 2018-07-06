# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·异兽'''
	intro = '''追上了难民了，$target正在等你'''
	detail = '''追上了难民了，$target正在等你'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1001,NI1002,NI1003,E(1001,1019),E(1002,1020),E(1003,1021)'''
#导表结束

	def customEvent(self, who, npcObj, eventName, *args):
		if eventName.startswith("addpet"):
			m = re.match("addpet(\d+)", eventName)
			if not m:
				return
			petId = int(m.group(1))
			petObj = who.petCtn.hasPetByIdx(petId)
			if not petObj:
				petObj = pet.new(petId,0)
				petObj = pet.addPet(who, petObj)#添加宠物
			who.petCtn.setCarry(petObj, True)#携带宠物
			#who.petCtn.setFighter(petObj, True)#参战宠物
			openUIPanel.openPetRewardUi(who, petObj.id)
			pass

import re
import pet
import pet.service
import openUIPanel