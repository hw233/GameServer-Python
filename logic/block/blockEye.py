# -*- coding: utf-8 -*-
import ctn
import block

# 玩家的阵眼容器
class cEyeContainer(ctn.cContainerBase, block.cCtnBlock):
	
	def __init__(self, iOwnerId):
		block.cCtnBlock.__init__(self, '阵法数据块', iOwnerId)
		ctn.cContainerBase.__init__(self, iOwnerId)

		self.setIsStm(sql.EYE_INSERT)
		self.setDlStm(sql.EYE_DELETE)
		self.setUdStm(sql.EYE_UPDATE)
		self.setSlStm(sql.EYE_SELECT)

	def _dirtyEventHandler(self):
		factoryConcrete.eyeFtr.schedule2tail4save(self.ownerId)

	def _rpcAddItem(self,obj):
		who = self.getOwnerObj()
		lineup.service.rpcEyeAdd(who, obj)

	def _rpcRemoveItem(self, obj):
		who = self.getOwnerObj()
		lineup.service.rpcEyeDelete(who, obj.id)

	def _createAndLoadItem(self, iIndex, uData):
		eyeId, data = uData
		return lineup.createEyeAndLoad(eyeId, data)

import sql
import factoryConcrete
import lineup
import lineup.service