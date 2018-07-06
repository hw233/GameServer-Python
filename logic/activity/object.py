# -*- coding: utf-8 -*-
import template
import pst
import block
import sql

class Activity(template.Template, pst.cEasyPersist, block.cBlock):
	'''活动
	'''
	
	def __init__(self, _id, name):
		template.Template.__init__(self)
		pst.cEasyPersist.__init__(self, self.__dirtyEventHandler)
		
		block.cBlock.__init__(self, "活动", _id)
		self.setIsStm(sql.ACTIVITY_INSERT)
		self.setDlStm(sql.ACTIVITY_DELETE)
		self.setUdStm(sql.ACTIVITY_UPDATE)
		self.setSlStm(sql.ACTIVITY_SELECT)
		
		self.id = _id
		self._name = name
		self.timerMgr = timer.cTimerMng()
		
	def init(self):
		'''初始化
		'''
		pass
		
	def __dirtyEventHandler(self):
		factoryConcrete.activityFtr.schedule2tail4save(self.id)
		
	@property
	def key(self):
		return self.id
		
	@property
	def name(self):
		return self._name
	
	@property
	def logName(self):
		return "activity/%s" % self.name
	
	def save(self):
		return pst.cEasyPersist.save(self)
	
	def load(self, data):
		pst.cEasyPersist.load(self, data)
		
	def getScriptHandler(self, script):
		for pattern, handler in gScriptHandlerList.iteritems():
			m = re.match(pattern, script)
			if not m:
				continue
			args = m.groups()
			return handler, args
		return template.Template.getScriptHandler(self, script)
		
	def addNpc(self, npcIdx, typeFlag="npc", who=None):
		npcObj = template.Template.addNpc(self, npcIdx, typeFlag, who)
		scene.switchSceneForNpc(npcObj, npcObj.sceneId, npcObj.x, npcObj.y, npcObj.d)
		return npcObj

	def newNpc(self, npcIdx, name, shape, who=None):
		'''创建Npc
		'''
		return Npc(self)
	
	def onRemoveNpc(self, npcObj):
		self.eventList.pop(npcObj.idx, None)
		npcObj.tryRemove()
		
	def startTimer(self, func, ti, flag, interval=0):
		'''定时器开始
		'''
		self.timerMgr.run(func, ti, interval, flag)
		
	def stopTimer(self, flag):
		'''定时器结束
		'''
		self.timerMgr.cancel(flag)
		
	def hasTimer(self, flag):
		'''是否有定时器
		'''
		return self.timerMgr.hasTimerId(flag)
			
	def testCmd(self, who, cmdIdx, *args):
		'''测试指令
		'''
		pass
	

import npc.object

class Npc(npc.object.NpcBase):
	'''活动npc
	'''
	
	def __init__(self, gameObj):
		npc.object.NpcBase.__init__(self)
		self.game = weakref.proxy(gameObj)
		
	def doLook(self, who):
		self.game.doEventScript(who, self, "点击")
		
	def tryRemove(self):
		if self.inWar():
			self.removed = True
			return
		self.remove()
		
	def remove(self):
		sceneObj = scene.getScene(self.sceneId)
		if sceneObj:
			sceneObj.removeEntity(self)
		
	def inWar(self):
		'''是否战斗中
		'''
		return getattr(self, "war", None)
	
	def enterWar(self, warObj):
		'''进入战斗
		'''
		self.war = weakref.proxy(warObj)
		self.attrChange("addon")
	
	def leaveWar(self):
		'''离开战斗
		'''
		if hasattr(self, "war"):
			del self.war
		self.attrChange("addon")
		
	def onWarEnd(self, warObj):
		if self.inWar():
			self.leaveWar()
		if hasattr(self, "removed"):
			self.tryRemove()
			
	def getAddon(self):
		'''附加状态
		'''
		import role.defines
		addon = 0
		if self.inWar():
			addon |= role.defines.ADDON_FIGHT
		return addon

# 脚本处理函数
gScriptHandlerList = {
}
		

import weakref
import timer
import scene
import factoryConcrete
import re