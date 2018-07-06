# -*- coding: utf-8 -*-
from task.defines import *
from task.bamboo.t30401 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30401
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''竹林除妖'''
	intro = '''战胜$target'''
	detail = '''原来是赤尸神君在祸害百姓，赶紧制止他'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1008,E(1008,1008)'''
#导表结束

	def onAddWarrior(self, w):
		if w.isMonster() and w.name == "赤尸神君":
			w.attCnt = 0
			w.addFunc("onNewRound", self.onNewRound)
			
	def onNewRound(self, w):
		if w.isMonster() and w.name == "赤尸神君":
			if w.isDead():#死亡就不加了
				return
			if w.attCnt:
				#每回合累加5%伤害
				w.addApply("物理伤害结果加成", 5)
				w.addApply("法术伤害结果加成", 5)
				#计算作用在哪些小怪
				targetList = []
				for vic in w.getFriendList():
					if vic == w:
						continue
					if vic.isMonster() and vic.name == "僵尸":
						if vic.hp > 1:
							targetList.append(vic)
				if targetList:
					w.war.say(w, self.getText(2002))
					hpMax = w.getHPMax()
					val = int(hpMax/3)		#最多加1/3的血
					if w.hp + val > hpMax:
						val = hpMax - w.hp
					avgHp = val / len(targetList)	#每个僵尸怪物平均扣血量
					addHp = 0
					for vic in targetList:
						#至少剩下1点血
						hp = min(avgHp, vic.hp-1)
						vic.addHP(-hp)
						addHp += hp
					w.addHP(int(addHp))		#赤尸神君加血
			w.attCnt += 1


from common import *
import war.commands
import activity.instance
import scene

