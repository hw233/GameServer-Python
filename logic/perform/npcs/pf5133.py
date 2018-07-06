# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5133
	name = "慧眼"
	applyList = {
		"破隐":True,
	}
	configInfo = {
		"概率":30,
	}
#导表结束
#可以看见隐形单位，有30%几率将对方打出隐形状态

	def onSetup(self, w):
		self.addFunc(w, "onAttack", self.onAttack)
		
	def onAttack(self, att, vic, vicCast, dp, attackType):
		if dp <= 0:
			return
		if not vic.hasApply("隐身"):
			return
		if rand(100) >= self.configInfo["概率"]:
			return
		
		# 清除隐身的buff
		removeList = []
		for buffList in vic.buffList.itervalues():
			for buffObj in buffList:
				if not buffObj:
					continue
				if not buffObj.applyList.get("隐身"):
					continue
				removeList.append(buffObj.id)
				
		for buffId in removeList:
			buff.remove(vic, buffId)
		
		# 清除其他隐身效果	
		vic.removeApply("隐身")


from common import *
import buff