# -*- coding: utf-8 -*-
import props.object

class cProps(props.object.cProps):
	taskId = 50251

	def onBorn(self, *tArgs, **dArgs):
		props.object.cProps.onBorn(self, *tArgs, **dArgs)
		taskObj = task.getTask(self.taskId)
		sceneId = taskObj.transIdxByGroup(9003)
		x, y = scene.randSpace(sceneId)
		self.set("pos", (sceneId, x, y))
		
	def desc(self):
		sceneId, x, y =  self.fetch("pos")
		sceneObj = scene.getScene(sceneId)
		return "%s(%d,%d)" % (sceneObj.name, x, y)
	
	def use(self,who):#override
		if not self.checkUse(who):
			return

		iSceneId,iX,iY = self.getPos()
		if not getattr(self, "openShortCut", 0) or not scene.isNearBy(who, (iSceneId,iX,iY)):
			scene.walkToPos(who, iSceneId, iX, iY, self.walkRespond)
			return False
		else:
			self.onPosUse(who)
			return True
		
	def walkRespond(self, who):
		self.openShortCut = 1
		who.endPoint.rpcShortcut(self.getMsg4Package(None,*self.MSG_FIRST))

	def onPosUse(self, who):
		if self.stack() <= 0:
			return
		who.propsCtn.addStack(self, -1)
		taskObj = task.newTask(who, None, self.taskId)
		taskObj.doScript(who, None, "TPM8002")
		return True

	def getPos(self):
		iSceneId,iX,iY = self.fetch("pos",(0,0,0))
		if not iSceneId:
			who = getRole(self.iOwnerId)
			if who:
				iSceneId,iX,iY = self.initPos(who)
				self.set("pos",(iSceneId,iX,iY))
		return iSceneId,iX,iY

	def checkUse(self, who):
		if task.hasTask(who, self.taskId):
			message.tips(who, "你已领取了#C04月儿岛任务#n")
			return 0
		return 1

from common import *		
import task
import message
import scene
	
