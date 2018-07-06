# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "步步回春"
	type = BUFF_TYPE_BUFF
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onAttacked", self.onAttacked)
		
	def onCancelSetup(self, w):
		if not hasattr(self, "performObj"):
			return
		if self.bout <= 0:
			self.cure(w)
			
	def config(self, pfObj, att, targetCount, times):
		self.performObj = pfObj
		self.attacker = att
		self.targetCount = targetCount
		self.times = times
		
	def onAttacked(self, att, vic, vicCast, dp, attackType):
		'''被攻击时
		'''
		if not hasattr(self, "performObj"):
			return
		self.cure(vic)
		
		self.times -= 1
		if self.times > 0:
			self.transferToFriend(vic)
		else:
			buff.remove(vic, self.id)
	
	def cure(self, w):
		'''治疗
		'''
		if w.isDead():
			return
		
		att = self.attacker
		dp = self.performObj.calCure(att, w, w, self.targetCount)
		w.addHP(dp, w)
		
	def transferToFriend(self, w):
		'''转移给己方
		'''
		performObj = self.performObj
		att = self.attacker
		for vic in w.getFriendList():
			if vic == w:
				continue
			if buff.has(vic, self.id):
				continue
			bfObj = buff.addOrReplace(vic, self.id, self.bout, w)
			if bfObj:
				buff.remove(w, self.id)
				bfObj.config(performObj, att, self.targetCount, self.times)
				break

from common import *
import buff