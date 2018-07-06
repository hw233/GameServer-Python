# -*- coding: utf-8 -*-
from task.defines import *
from task.magicWave.t30501 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30501
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''副本·火云童子'''
	intro = '''与$target战斗'''
	detail = '''击败$target，寻找玉娘子踪迹'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1002,E(1002,1002),STORY30502'''
#导表结束
	
	def onStartWar(self, w):
		'''登场闲话
		'''
		if w.isMonster():
			if w.name == "冰玉童子":# 闲话 进场告知减伤效果
				w.war.say(w, self.getText(2002), WORDS_STAR)
			elif w.name == "火云童子":# 闲话 进场告知减伤效果
				w.war.say(w, self.getText(2004), WORDS_STAR)

	def onAddWarrior(self, w):
		if w.isMonster():
			if w.name == "冰玉童子":#存活时：治疗、物理、法术减40%物伤
				w.addFunc("beforeDie", self.beforeDie)
			
			elif w.name == "火云童子":#存活时：治疗、物理、法术减40%法伤
				w.addFunc("beforeDie", self.beforeDie)

			elif w.name in ("金刀真人", "千手真人", "回春真人"):
				buff.addOrReplace(w, 502, 99)
				buff.addOrReplace(w, 503, 99)

		
	def beforeDie(self, w, att):
		if w.isMonster():
			if w.name == "冰玉童子":
				# 闲话 死亡告知效果消失
				w.war.say(w, self.getText(2003), WORDS_MONSTER_DEAD)
				for vic in w.getFriendList():
					if vic == w:
						continue
					if vic.name in ("金刀真人", "千手真人", "回春真人"):
						buff.remove(vic, 503)

			elif w.name == "火云童子":
				# 闲话 死亡告知效果消失
				w.war.say(w, self.getText(2005), WORDS_MONSTER_DEAD)
				for vic in w.getFriendList():
					if vic == w:
						continue
					if vic.name in ("金刀真人", "千手真人", "回春真人"):
						buff.remove(vic, 502)


import buff
from words.defines import *
