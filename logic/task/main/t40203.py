# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

weaponsData={
	1111:100000,
	1121:100050,
	1211:100100,
	1221:100150,
	1311:100200,
	1321:100250,
	1411:100300,
	1421:100350,
	1511:100400,
	1521:100450,
	1611:100500,
	1621:100550,
}

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·武器'''
	intro = '''$target招你过去，与其谈谈'''
	detail = '''$target招你过去，与其谈谈'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''B(1003,school)'''
#导表结束

	def customEvent(self, who, npcObj, eventName, *args):
		if eventName == "weapon":
			launch.launchBySpecify(who, weaponsData.get(who.shape), 1, False, self.name)

import launch