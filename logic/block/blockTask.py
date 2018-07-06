# -*-coding:utf-8-*-
# 作者:马昭@曹县闫店楼镇

import ctn
import block

# 玩家的任务容器
class cTaskContainer(ctn.cContainerBase, block.cCtnBlock):
	def __init__(self, iOwnerId):  # override
		ctn.cContainerBase.__init__(self, iOwnerId)
		block.cCtnBlock.__init__(self, '任务数据块', iOwnerId)
		self.setIsStm(sql.TASK_INSERT)
		self.setDlStm(sql.TASK_DELETE)
		self.setUdStm(sql.TASK_UPDATE)
		self.setSlStm(sql.TASK_SELECT)
		self.finishList = []  # 已完成任务列表,提交之后的任务会记录在这里,存盘

	def _createAndLoadItem(self, iIndex, uData):  # override
		if isinstance(uData, tuple):
			iNo, dData = uData
		else:
			iNo = uData
			dData = {}
		return task.createAndLoad(self.ownerId, iNo, dData)  # create task object and return

	def _dirtyEventHandler(self):  # override
		factoryConcrete.taskCtnFtr.schedule2tail4save(self.ownerId)
		
	@property
	def endPoint(self):
		import mainService
		return mainService.getEndPointByRoleId(self.ownerId)

	def _rpcAddItem(self, taskObj):
		who = getRole(self.ownerId)
		if who:
			task.service.rpcTaskAdd(who, taskObj)

	#override
	def _rpcRefresh(self):
		#默认实现是逐个下发,性能较差.子类可以override,进行优化处理,比如:全部子项拼成一个网络包下发
		who = getRole(self.ownerId)
		if who:
			task.service.rpcTaskAll(who)

	def _rpcRemoveItem(self, taskObj):
		who = getRole(self.ownerId)
		if who:
			task.service.rpcTaskDel(who, taskObj)

	def onBorn(self, *tArgs, **dArgs):
		pass

	def load(self, dData):  # override
		ctn.cContainerBase.load(self, dData)
		self.finishList = dData.pop('finishList', [])

	def save(self):  # override
		dData = ctn.cContainerBase.save(self)
		dData["finishList"] = self.finishList
		return dData
			
	def removeItem(self, taskObj):
		taskObj.release()
		ctn.cContainerBase.removeItem(self, taskObj)
		
	def setup(self, obj, isLogin=False):
		who = self.getOwnerObj()
		if who and hasattr(obj, "setup"):
			obj.setup(who)
		
	def cancelSetup(self, obj):
		who = self.getOwnerObj()
		if who and hasattr(obj, "cancelSetup"):
			obj.cancelSetup(who)

	# 将任务添加到已完成列表
	def addFinish(self, taskId):
		self.finishList.add(taskId)
		self.markDirty()

	def isFinished(self, taskId):
		return taskId in self.finishList


from common import *
import sql
import factoryConcrete
import task
import task.service
