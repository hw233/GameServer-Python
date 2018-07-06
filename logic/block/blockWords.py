#-*- coding:UTF-8 -*-
import block
import ctn
import pst

class cWords(block.cBlock, pst.cEasyPersist):
	def __init__(self,iRoleId):
		self.iRoleId = iRoleId
		block.cBlock.__init__(self, '玩家闲话数据', iRoleId)
		pst.cEasyPersist.__init__(self, self._dirtyEventHandler)
		self.setIsStm(sql.WORDS_INSERT)
		self.setDlStm(sql.WORDS_DELETE)
		self.setUdStm(sql.WORDS_UPDATE)
		self.setSlStm(sql.WORDS_SELECT)
		self.worsList = {1:{},2:{}} #闲话

	def _dirtyEventHandler(self):#override
		factoryConcrete.wordsFtr.schedule2tail4save(self.iRoleId)

	def load(self,dData):#override
		pst.cEasyPersist.load(self,dData)
		self.worsList = dData.pop("words",{1:{},2:{}})

	def save(self):#override
		dData=pst.cEasyPersist.save(self)
		dData['words'] = self.worsList
		return dData

	def getWords(self, wordType, entityNo, event):
		'''获取闲话
		'''
		worsList = self.worsList[wordType].get(entityNo,{})
		if event not in worsList:
			return wordsData.getConfig(wordType, entityNo, event)
		return worsList[event]

	def setWords(self, wordType, entityNo, event, msg):
		'''设置闲话
		'''
		worsList = self.worsList[wordType].setdefault(entityNo,{})
		worsList[event] = msg
		self.markDirty()

	def delWords(self, wordType, entityNo):
		'''删除闲话
		'''
		if entityNo in self.worsList[wordType]:
			self.worsList[wordType].pop(entityNo)
			self.markDirty()

import factoryConcrete
import sql
import wordsData