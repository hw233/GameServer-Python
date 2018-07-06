# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NONE
	icon = 0
	title = '''第一章·最初'''
	intro = '''最初'''
	detail = '''最初'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''STORY(40000,1000)'''
#导表结束

	def onStartWar(self, w):
		pass

	def onAddWarrior(self, w):
		w.setApply("禁止逃跑", True)
		if w.side == TEAM_SIDE_2 and (w.isMonster() or w.isBoss()):
			w.addFunc("onNewRound", self.onNewRound)
			# w.addFunc("onEndRound", self.onEndRound)
		if w.isRole():
			self.setRoleInfo(w)

	def onNewRound(self, w):
		warObj = w.war
		if w.isDead():
			return
		if warObj.bout == 3:
			w.phyDam = w.phyDam * 100
			w.magDam = w.magDam * 100
			w.phyDef = w.phyDef * 100
			w.magDef = w.magDef * 100
			
		if w.name == "明修罗":
			if warObj.bout == 1:
				warObj.say(w, self.getText(7001))
			elif warObj.bout == 2:
				warObj.say(w, self.getText(7002))
			elif warObj.bout == 3:
				warObj.say(w, self.getText(7003))
		
	def onEndRound(self, w):
		pass

	def setRoleInfo(self,w):
		info =  self.getConfigInfo()
		w.phyCrit = info["物理暴击"]
		w.magCrit = info["法术暴击"]
		w.phyReCrit = info["物理抗暴"]
		w.magReCrit = info["法术抗暴"]
		w.hpMax = info["生命上限"]
		w.hp = info["生命上限"]
		w.mpMax = info["真气上限"]
		w.mp = info["真气上限"]
		w.phyDam = info["物理伤害"]
		w.magDam = info["法术伤害"]
		w.phyDef = info["物理防御"]
		w.magDef = info["法术防御"]
		w.spe = info["速度"]
		w.cure = info["治疗强度"]
		w.sealHit = info["封印命中"]
		w.reSealHit = info["抵抗封印"]

	def setupWar(self, warObj, who, npcObj):
		'''战斗设置
		'''
		warObj.noLost = True
		warObj.setAutoFight(False)

from war.defines import *