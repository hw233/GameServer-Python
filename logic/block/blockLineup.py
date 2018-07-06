# -*- coding: utf-8 -*-
import ctn
import block

# 玩家的阵法容器
class cLineupContainer(ctn.LevelContainer, block.cCtnBlock):
	
	def __init__(self, iOwnerId):
		block.cCtnBlock.__init__(self, '阵法数据块', iOwnerId)
		ctn.LevelContainer.__init__(self, iOwnerId)

		self.setIsStm(sql.LINEUP_INSERT)
		self.setDlStm(sql.LINEUP_DELETE)
		self.setUdStm(sql.LINEUP_UPDATE)
		self.setSlStm(sql.LINEUP_SELECT)

	def _createAndLoadItem(self, iIndex, uData):
		iNo, dData = uData
		return lineup.createLineupAndLoad(iNo, dData)
	
	def _newItem(self, lineupId):
		return lineup.createLineup(lineupId)
	
	def setup(self, obj, isLogin=False):
		who = self.getOwnerObj()
		if who and hasattr(obj, "setup"):
			obj.setup(who)
		
	def cancelSetup(self, obj):
		who = self.getOwnerObj()
		if who and hasattr(obj, "cancelSetup"):
			obj.cancelSetup(who)
		
	def setItemLevel(self, lineupObj, level):
		ctn.LevelContainer.setItemLevel(self, lineupObj, level)
		self.cancelSetup(lineupObj)
		self.setup(lineupObj)

	def _rpcAddItem(self, lineupObj):
		who = self.getOwnerObj()
		lineup.service.rpcLineupAdd(who, lineupObj)

	def _rpcRemoveItem(self, lineupObj):
		who = self.getOwnerObj()
		lineup.service.rpcLineupDelete(who, lineupObj.id)
		
	def _rpcSetLevel(self, lineupObj):
		who = self.getOwnerObj()
		lineup.service.rpcLineupMod(who, lineupObj, "level")

	def _dirtyEventHandler(self):
		factoryConcrete.lineupFtr.schedule2tail4save(self.ownerId)
		
	def addExp(self, lineupId, exp):
		lineupObj = self.getItem(lineupId)
		if not lineupObj: # 必须先学习才能增加经验
			return
		
		levelMax = lineupObj.getLevelMax()
		if lineupObj.level >= levelMax:
			return
		
		exp = lineupObj.getExp() + exp
		while exp >= lineupObj.getExpNext():
			exp = exp - lineupObj.getExpNext()
			lineupObj.level += 1
			if lineupObj.level >= levelMax:
				break
			
		lineupObj.setExp(exp)
		
		who = self.getOwnerObj()
		lineup.service.rpcLineupMod(who, lineupObj, "level", "exp")
		

from common import *
import sql
import factoryConcrete
import lineup
import lineup.service
