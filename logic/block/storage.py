#-*-coding:utf-8-*-

import ctn
import block

SOTRAGE_COUNT = 25  #一个仓库的容量

class cStorage(ctn.cContainerBase,block.cCtnBlock):

	def __init__(self,iOwnerId):#override
		block.cCtnBlock.__init__(self,"仓库",iOwnerId)
		ctn.cContainerBase.__init__(self,iOwnerId)
		self.setIsStm(sql.STORAGE_INSERT).setDlStm(sql.STORAGE_DELETE)		
		self.setUdStm(sql.STORAGE_UPDATE).setSlStm(sql.STORAGE_SELECT)

	def _dirtyEventHandler(self):#override
		factoryConcrete.storageFtr.schedule2tail4save(self.iOwnerId)

	def _createAndLoadItem(self,iIndex,uData):#override
		iNo,dData=uData
		obj=props.create(iNo)
		obj.load(dData)
		return obj

	def _saveItem(self,iIndex,obj):#override
		return obj.no(),obj.save()

	def _rpcAddItem(self,obj):
		self.endPoint.rpcAdd2Storage(obj.getMsg4Item(self,*obj.MSG_FIRST))

	def _rpcRemoveItem(self,obj):#override
		self.endPoint.rpcDel2Storage(obj.id)

	def _rpcRefresh(self):#不下发给客户端
		self.endPoint.rpcStorageInfo(self.getMsg())
		return

	def capacity(self):
		'''容量
		'''
		return (2 + self.fetch("count"))*SOTRAGE_COUNT

	def leftCapacity(self):
		'''剩余容量
		'''
		return self.capacity() - self.itemCount()

	@property
	def endPoint(self):
		return mainService.getEndPointByRoleId(self.ownerId)

	def getConfig(self,iNo,sKey):
		return storageData.getConfig(iNo,sKey)

	def getName(self,iNo):
		'''仓库名称
		'''
		return self.getConfig(iNo,"仓库名称")

	def getCostCash(self,iNo):
		'''消耗银币
		'''
		return self.getConfig(iNo,"消耗银币")

	def getMsg(self):
		msg = props_pb2.storageMsg()
		lst = []
		for iNo in xrange(1,self.fetch("count")+3):
			nameMsg = msg.nameList.add()
			nameMsg.iNo = iNo
			nameMsg.sName = self.getName(iNo)
		for obj in self.getAllValues():
			lst.append(obj.getMsg4Item(self,*obj.MSG_FIRST))
		msg.allItem.extend(lst)
		return msg

	def addStack(self,obj,iAmount):#增加或扣除某个物品的叠加数量
		iBalance=obj.stack()+iAmount
		if iBalance<0:
			raise Exception,'扣除{}扣成负数了,{}个'.format(obj.name,iBalance)
		elif iBalance>obj.maxStack():
			raise Exception,'{}叠加数量超过{}个'.format(obj.name,iBalance)
		obj.setStack(iBalance)
		if iBalance==0:
			obj.setStack(iBalance)
			self.removeItem(obj)
			#todo 记log跟踪道具流向
		else:
			self.markDirty()
			self.endPoint.rpcMod2Storage(obj.getMsg4Item(self,'stack'))

import mainService
import props
import factoryConcrete
import sql
import props_pb2
import storageData