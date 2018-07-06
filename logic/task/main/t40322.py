# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NONE
	icon = 0
	title = '''第二章·玉匣'''
	intro = '''检查玉匣，看看蜀山秘宝是否还在'''
	detail = '''检查玉匣，看看蜀山秘宝是否还在'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''R1492'''
#导表结束
#
	def goAhead(self, who):
		'''前往
		'''
		sceneId, x, y = 1130, 20, 47
		scene.walkToPos(who, sceneId, x, y, self.walkRespond)

	def walkRespond(self, who):
		propsNo = 203015
		propsObj = who.propsCtn.hasPropsByNo(propsNo)
		if not propsObj:
			launch.launchBySpecify(who, int(propsNo),1, False, self.name)
			propsObj = who.propsCtn.hasPropsByNo(propsNo)
		who.endPoint.rpcShortcut(propsObj.getMsg4Package(None,*propsObj.MSG_FIRST))

import scene
import launch