#-*-coding:utf-8-*-
import props.object

#根据唯一id把所带的编号信息解出来
def getNoByguId(iId):
	iDecCarry = iId%10
	iMod=10**(iDecCarry+1)
	return iId/iMod

class cProps(props.object.cProps):
	def shortcut(self,who):#快捷使用
		return 0

	def use(self,who):#override
		taskObj = who.taskCtn.getItem(30206)
		if not taskObj:
			return
		sceneId, x, y = taskObj.genPos()
		if not scene.isNearBy(who, (sceneId,x,y)):
			scene.walkToPos(who, sceneId, x, y, self.walkRespond)
			return False
		else:
			self.onPosUse(who)
			return True
		
	def walkRespond(self, who):
		who.endPoint.rpcShortcut(self.getMsg4Package(None,*self.MSG_FIRST))

	def onPosUse(self, who):
		pid = who.id
		guildObj = who.getGuildObj()
		name = guildObj.name
		guildId = guildObj.id
		tenet = guildObj.getTenet()
		hl = guildObj.getHyperLink(pid)
		content = "欢迎加入#C02{}#n仙盟，[仙盟编号：#C02{}#n]{}{}".format(name, getNoByguId(guildId), tenet, hl)
		message.currentRoleMessage(who.id, content)
		message.progressBar(who, self.responseUse, "宣读中...", 10001, 2, True)
		
	def responseUse(self, who, isDone):
		if not isDone:
			return
		if self.stack() <= 0:
			return
		who.propsCtn.addStack(self,-1)
		self.doEvent(who)

	def doEvent(self,who):
		taskObj = task.hasTask(who, 30201)
		if taskObj:
			script = taskObj.getEventInfo(2003)
			taskObj.doScript(who, None, script["点击"])
			# taskObj.set("step", 1)
			# taskObj.goAhead(who)


from common import *
import scene
import task
import message