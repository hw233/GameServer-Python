#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

import props.object
class cProps(props.object.cProps):

	def shortcut(self,who):#快捷使用
			return 0

	def use(self, who):#override

		if not task.hasTask(who, 40212):
			return
		sceneId, x, y = 1140, 50, 24
		if not scene.isNearBy(who, (sceneId,x,y)):
			scene.walkToPos(who, sceneId, x, y, self.walkRespond)
			return False
		else:
			self.onPosUse(who)
			return True

	def walkRespond(self, who):
		who.endPoint.rpcShortcut(self.getMsg4Package(None,*self.MSG_FIRST))

	def onPosUse(self, who):
		message.progressBar(who, self.responseUse, "挖掘中...", 100350, 2, True)
		
	def responseUse(self, who, isDone):
		if not isDone:
			return
		if self.stack() <= 0:
			return
		who.propsCtn.subPropsByNo(203014, 1, self.name)
		#who.propsCtn.addStack(self,-1)
		self.doEvent(who)

	def doEvent(self,who):
		taskObj = task.hasTask(who, 40212)
		if taskObj:
			script = taskObj.getEventInfo(1047)
			taskObj.doScript(who, None, script["成功"])

		
from common import *
import scene
import task
import message