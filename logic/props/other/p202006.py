#-*-coding:utf-8-*-
import props.object

class cProps(props.object.cProps):

	def use(self,who):#override
		iSceneId,iX,iY = self.getPos()
		if not getattr(self, "openShortCut", 0) or not scene.isNearBy(who, (iSceneId,iX,iY)):
			scene.walkToPos(who, iSceneId, iX, iY, self.walkRespond)
		else:
			self.onPosUse(who)
		
	def walkRespond(self, who):
		self.openShortCut = 1
		who.endPoint.rpcShortcut(self.getMsg4Package(None,*self.MSG_FIRST))

	def onPosUse(self, who):
		message.progressBar(who, self.responseUse, "挖宝中...", 202006, 2, False)
		
	def responseUse(self, who, isDone):
		if not isDone:
			return
		if self.stack() <= 0:
			return
		who.propsCtn.addStack(self,-1)
		self.doEvent(who)

	def doEvent(self,who):
		activityObj = activity.getActivity("fengyao")
		if activityObj:
			activityObj.onUseProps(who, self.no())

	def valueInfo(self):
		'''效果信息
		'''
		iSceneId,iX,iY = self.getPos()
		oScene = scene.getScene(iSceneId)
		msg = props_pb2.attrMsg()
		msg.name = 26
		msg.sValue = "{}({},{})".format(oScene.name,iX,iY)
		return msg

	def getPos(self):
		iSceneId,iX,iY = self.fetch("pos",(0,0,0))
		if not iSceneId:
			iSceneId,iX,iY = self.initPos()
		return iSceneId,iX,iY

	def initPos(self):
		activityObj = activity.getActivity("fengyao")
		iSceneId,iX,iY = activityObj.generateMapPos(self.ownerId,self.name)
		self.set("pos",(iSceneId,iX,iY))
		return iSceneId,iX,iY

from common import *
import scene
import activity
import props_pb2
import message