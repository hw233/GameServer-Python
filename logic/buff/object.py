# -*- coding: utf-8 -*-

class Buff(object):
	name = ""
	type = 0
	applyList = {  # 附加效果
# 		"禁止法术": True,
# 		"禁止物理攻击": "1",
	}
	removable = True # 可否被解除
	replacable = True # 可否叠加
		
	def __init__(self, _id):
		self.id = _id
		self.bout = 0
		self.pos = 0
	
	def onNew(self, w, att, **args):
		'''新建
		'''
		pass
		
	def getTypePos(self):
		'''类型位置
		'''
		return self.type / 10
	
	def lost(self, w):
		'''失去
		'''
		self.cancelSetup(w)
		w.war.rpcWarBuff(idx=w.idx, id=self.id, bout=0)

	def setup(self, w):
		'''设置
		'''
		for name, val in self.applyList.iteritems():
			if isinstance(val, bool):
				self.setApply(w, name, val)
			else:
				val = int(self.transCode(val, w))
				self.addApply(w, name, val)

		self.onSetup(w)
		w.war.rpcWarBuff(idx=w.idx, id=self.id, bout=self.bout)
		
	def onSetup(self, w):
		'''设置时
		'''
		pass
	
	def cancelSetup(self, w):
		'''取消设置
		'''
		w.removeApplyByFlag("bf%d" % self.id)
		w.removeFuncByFlag("bf%d" % self.id)
		self.onCancelSetup(w)
		
	def onCancelSetup(self, w):
		pass
	
	def addApply(self, w, name, val):
		w.addApply(name, int(self.transCode(val, w)), "bf%d" % self.id)
		
	def setApply(self, w, name, val):
		w.setApply(name, self.transCode(val, w), "bf%d" % self.id)
		
	def addFunc(self, w, name, func):
		w.addFunc(name, func, "bf%d" % self.id)
		
	def transCode(self, code, w=None):
		import common
		return common.transCode(self, code, w)
	
	def getValueByVarName(self, varName, w=None):
		import perform.defines
		return perform.defines.getValueByVarName(varName, w)

	def newRound(self, w):
		'''回合开始时
		'''
		self.onNewRound(w)
		
	def onNewRound(self, w):
		pass
	
	def cleanRound(self, w):
		'''清除回合时
		'''
		self.onCleanRound(w)
		if self.bout != 99:
			self.bout -= 1
			if self.bout <= 0:
				self.lost(w)
			else:
				w.war.rpcWarBuff(idx=w.idx, id=self.id, bout=self.bout)
			
	def onCleanRound(self, w):
		pass
				
# 	def isPoison(self):
# 		'''是否毒
# 		'''
# 		return self.type == BUFF_TYPE_POISON
	

from buff.defines import *
import buff.defines
import types
