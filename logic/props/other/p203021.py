#-*-coding:utf-8-*-
import props.object

class cProps(props.object.cProps):
	def use(self,who):#override
		taskObj = task.hasTask(who, 30601)
		if taskObj and taskObj.timerMgr.hasTimerId("timeOut"):
			scene.walkGuard(who, 2010)
			return
		iSceneId,iX,iY = self.getPos()
		if not scene.isNearBy(who, (iSceneId,iX,iY)):
			if not scene.tryTransfer(who, iSceneId, iX, iY):
				return
			txt = "使用成功，开始计时"
			message.tips(who, txt)
			message.message(who, txt)
			who.triggerWarTime = getSecond()
			# scene.walkToPos(who, iSceneId, iX, iY, self.walkRespond)
			
			self.doEvent(who)
			return True
		else:
			self.onPosUse(who)
			return True
		
	def walkRespond(self, who):
		self.onPosUse(who)

	def onPosUse(self, who):
		self.doEvent(who)
		return True

	def doEvent(self,who):
		taskObj = task.hasTask(who, 30601)
		if not taskObj:
			return
		taskObj.setTime(20*60)
		taskObj.timerMgr.run(taskObj.timeOut, 20*60, 0, "timeOut")
		if not taskObj.getAnlei():
			taskObj.setAnlei(who, None, 1002, 1006, [2010])
		taskObj.onTriggerWar = functor(taskObj.triggerWar)  # 挂上触发暗雷函数
		if not who.stateCtn.getItem(107):
			state.addState(who, 107, 1200)
		scene.walkGuard(who, 2010)
		task.service.refreshTask(who, taskObj)

	def getPos(self):
		sceneId = 2010
		x, y = scene.randSpace(sceneId)
		return sceneId, x, y


from common import *
import scene
import task
import props_pb2
import message
import state
import task.service
