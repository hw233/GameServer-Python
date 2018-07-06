# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第一章·余寇'''
	intro = '''向$target问清楚情况，只是前方好像有点骚动'''
	detail = '''向$target问清楚情况，只是前方好像有点骚动'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1001,NI1002,E(1001,1022),E(1002,1023)'''
#导表结束
	def setupWar(self, warObj, who, npcObj):
		'''战斗设置,设置为手动战斗
		'''
		warObj.setAutoFight(False)
	def onStartWar(self, w):
		warObj = w.war
		if (w.isBoss() or w.isMonster()) and w.name == "林难敌":
			warObj.say(w, "区区马贼也敢猖狂？！我们武林盟弟子不会坐视不理！")

	def onAddWarrior(self, w):
		if (w.isBoss() or w.isMonster()) and w.name == "沈胜男":
			w.addFunc("onEndRound", self.onEndRound)

	def onEndRound(self, w):
		if (w.isBoss() or w.isMonster()) and w.name == "沈胜男" and w.bout == 1:
			w.war.say(w, "优昙神尼算出一年之后，众生或会遭浩劫……这可算其中的灾难？")
