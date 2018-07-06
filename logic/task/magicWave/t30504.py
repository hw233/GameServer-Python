# -*- coding: utf-8 -*-
from task.defines import *
from task.magicWave.t30501 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30501
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''副本·玉娘子崔盈'''
	intro = '''与$target战斗'''
	detail = '''击败$target，完成试炼'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1004,E(1004,1004),STORY30504'''
#导表结束

	def onStartWar(self, w):
		'''登场闲话
		'''
		if w.isMonster():
			if w.name == "崔盈":# 闲话 进场叫嚣一番
				w.war.say(w, self.getText(2008), WORDS_STAR)

	def onAddWarrior(self, w):
		if w.isMonster():
			if w.name == "冰玉童子":#存活时：治疗、物理、法术减40%物伤
				w.addFunc("beforeDie", self.beforeDie)

			elif w.name == "火云童子":#存活时：治疗、物理、法术减40%法伤
				w.addFunc("beforeDie", self.beforeDie)

			elif w.name in ("金刀真人", "千手真人", "回春真人"):
				buff.addOrReplace(w, 504, 99)
				buff.addOrReplace(w, 505, 99)

	def beforeDie(self, w, att):
		if w.isMonster():
			if w.name == "冰玉童子":
				for vic in w.getFriendList():
					if vic == w:
						continue
					if vic.name in ("金刀真人", "千手真人", "回春真人"):
						buff.remove(vic, 505)

			elif w.name == "火云童子":
				for vic in w.getFriendList():
					if vic == w:
						continue
					if vic.name in ("金刀真人", "千手真人", "回春真人"):
						buff.remove(vic, 504)


import buff
from words.defines import *
