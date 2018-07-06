# -*- coding: utf-8 -*-
from task.defines import *
from task.magicWave.t30501 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30501
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''副本·圣姑幻影'''
	intro = '''与$target战斗'''
	detail = '''击败$target，寻找玉娘子踪迹'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1003,E(1003,1003),STORY30503'''
#导表结束

	def onStartWar(self, w):
		'''登场闲话
		'''
		if w.isMonster():
			if w.name == "魅魂":#闲话 进场告知被封
				w.war.say(w, self.getText(2006), WORDS_STAR)

	def onAddWarrior(self, w):
		if w.isMonster():
			if w.name == "圣姑幻影":
				#存活时：血魔被全封,状态表编号111
				w.addFunc("beforeDie", self.beforeDie)
			elif w.name == "魅魂":
				w.addFunc("beforeDie", self.beforeDie)
				buff.addOrReplace(w, 111, 99)

			
	def beforeDie(self, w, att):
		if w.isMonster():
			if w.name == "圣姑幻影":
				#解除封印时候告知解封
				for vic in w.getFriendList():
					if vic.name in ("魅魂",):
						vic.war.say(vic, self.getText(2007), WORDS_BUFF_REMOVE)
						buff.remove(vic, 111)


import buff
from words.defines import *
