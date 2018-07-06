# -*- coding: utf-8 -*-
import ctn
import block

# 成就容器
class AchvContainer(ctn.cContainerBase, block.cCtnBlock):
	
	def __init__(self, ownerId):
		block.cCtnBlock.__init__(self, '成就数据块', ownerId)
		ctn.cContainerBase.__init__(self, ownerId)

		self.setIsStm(sql.ACHV_INSERT)
		self.setDlStm(sql.ACHV_DELETE)
		self.setUdStm(sql.ACHV_UPDATE)
		self.setSlStm(sql.ACHV_SELECT)

	def _dirtyEventHandler(self):
		factoryConcrete.achvFtr.schedule2tail4save(self.ownerId)

	@property
	def endPoint(self):
		return mainService.getEndPointByRoleId(self.ownerId)

	def _rpcAddItem(self, achvObj):
		who = self.getOwnerObj()
		achv.service.rpcAchvAdd(who, achvObj)

	def _rpcRemoveItem(self, achvObj):
		who = self.getOwnerObj()
		achv.service.rpcAchvDelete(who, achvObj.id)

	def _createAndLoadItem(self, iIndex, uData):
		achvId, data = uData
		return achv.createAchvAndLoad(achvId, data)

	#override
	def _rpcRefresh(self):
		#默认实现是逐个下发,性能较差.子类可以override,进行优化处理,比如:全部子项拼成一个网络包下发
		allMsg=achv_pb2.achvMsgAll()
		lTemp = []
		for obj in self.getAllValues():
			lTemp.append(achv.service.getAchvMsg(obj))
		allMsg.achvMsgList.extend(lTemp)
		self.endPoint.rpcAchvAll(allMsg)
		

import mainService
import sql
import factoryConcrete
import achv_pb2
import achv
import achv.service