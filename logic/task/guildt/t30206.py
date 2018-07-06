# -*- coding: utf-8 -*-
from task.defines import *
from task.guildt.t30201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''仙盟-宣读公告'''
	intro = '''宣读仙盟公告'''
	detail = '''到目的坐标宣读仙盟公告'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''I(203001,1)'''
#导表结束

	def release(self):#override
		'''释放
		'''
		customTask.release(self)
		# 删除任务物品
		who = self.getOwnerObj()
		if who:
			who.propsCtn.removePropsByNo(203001)

	def isDone(self):
		if self.fetch("step") == 1:
			return True
		return False

	def genPos(self):
		pos = self.fetch("pos")
		if pos:
			return pos
		pos = (1130, 79, 77)
		lst = self.getGroupInfo(9011)
		if lst:
			pos = lst[rand(len(lst))]
		self.set("pos", pos)
		return pos

	def goAhead(self, who):#override
		'''前往
		'''
		if self.isDone(): # 完成的任务会找npc回复
			self.doScript(who, None, "GNpc")
			return
		pos = self.genPos()
		self.goAheadPos(who, pos[0], pos[1], pos[2])

	def goAheadPos(self, who, *args):
		'''前往指定坐标
		'''
		sceneId = int(args[0])
		x = int(args[1])
		y = int(args[2])
		scene.walkToPos(who, sceneId, x, y, self.walkRespond)

	def walkRespond(self, who):
		propsNo = 203001
		propsObj = who.propsCtn.hasPropsByNo(propsNo)
		if not propsObj:
			launch.launchBySpecify(who, propsNo, 1, False, self.name)
			propsObj = who.propsCtn.hasPropsByNo(propsNo)
		#who.endPoint.rpcShortcut(propsObj.getMsg4Package(None,*propsObj.MSG_FIRST))
		propsObj.use(who)
		


import scene
import launch
import npc
from common import *
