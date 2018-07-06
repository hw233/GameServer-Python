# -*- coding: utf-8 -*-
import ctn
import block

# 玩家状态容器
class cStateContainer(ctn.cContainerBase, block.cBlock):
	def __init__(self, iOwnerId):
		block.cBlock.__init__(self, '状态数据块', iOwnerId)
		ctn.cContainerBase.__init__(self, iOwnerId)
		self.setIsStm(sql.STATE_INSERT)
		self.setDlStm(sql.STATE_DELETE)
		self.setUdStm(sql.STATE_UPDATE)
		self.setSlStm(sql.STATE_SELECT)

	def _createAndLoadItem(self, iIndex, uData):
		if isinstance(uData, tuple):
			iNo, dData = uData
		else:
			iNo, dData = uData, {}
		obj = state.createAndLoad(iNo, dData)
		if not obj.isValid():
			return None
		return obj

	def _newItem(self, key):
		return state.new(key)

	def setup(self, obj, isLogin=False):
		who = self.getOwnerObj()
		if who and hasattr(obj, "setup"):
			obj.setup(who)

	def cancelSetup(self, obj):
		who = self.getOwnerObj()
		if who and hasattr(obj, "cancelSetup"):
			obj.cancelSetup(who)

	@property
	def endPoint(self):
		import mainService
		return mainService.getEndPointByRoleId(self.ownerId)

	def _rpcAddItem(self, stateObj):
		self.endPoint.rpcStateInfo(stateObj.getMsg())

	def _rpcRemoveItem(self, stateObj):
		self.endPoint.rpcStateInfoDel(stateObj.no)

	def _rpcRefresh(self):
		stateInfos = []
		for stateObj in self.getAllValues():
			stateInfos.append(stateObj.getMsg())
		stateInfoAll = state_pb2.stateInfoAll()
		stateInfoAll.stateInfoList.extend(stateInfos)
		self.endPoint.rpcStateInfoAll(stateInfoAll)

	def _dirtyEventHandler(self):
		factoryConcrete.stateFtr.schedule2tail4save(self.ownerId)

	# 更新状态值并刷新给客户端
	def updateItemByKey(self, iKey):
		obj = self.getItem(iKey)
		if not obj:
			return
		self.endPoint.rpcStateInfo(obj.getMsg())

import factoryConcrete
import sql
import state
import state_pb2
