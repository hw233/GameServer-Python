#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import ctn
import block

#玩家的临时背包
class cNumenBag(ctn.cContainerBase,block.cCtnBlock):
	def __init__(self,iOwnerId):#override
		block.cCtnBlock.__init__(self,"临时背包",iOwnerId)
		ctn.cContainerBase.__init__(self,iOwnerId)
		self.setIsStm(sql.NUMEN_BAG_INSERT).setDlStm(sql.NUMEN_BAG_DELETE)		
		self.setUdStm(sql.NUMEN_BAG_UPDATE).setSlStm(sql.NUMEN_BAG_SELECT)

	def _dirtyEventHandler(self):#override
		factoryConcrete.numenBagFtr.schedule2tail4save(self.iOwnerId)

	@property
	def endPoint(self):
		return mainService.getEndPointByRoleId(self.ownerId)

	def _createAndLoadItem(self,iIndex,uData):#override
		iNo,dData=uData
		obj=props.create(iNo)
		obj.load(dData)
		return obj

	def _saveItem(self,iIndex,obj):#override
		return obj.no(),obj.save()
	
	def addItem(self,obj):
		if not ctn.cContainerBase.addItem(self, obj):
			return False
		
		who = self.getOwnerObj()
		if who:
			who.set("numenBag", 1)

		return True

	def removeItem(self,obj):#移除子项
		if not ctn.cContainerBase.removeItem(self, obj):
			return False
		
		if not self.itemCount():
			who = self.getOwnerObj()
			if who:
				who.delete("numenBag")

		return True

	def _rpcRefresh(self):
		#默认实现是逐个下发,性能较差.子类可以override,进行优化处理,比如:全部子项拼成一个网络包下发
		# print "===cNumenBag======_rpcRefresh====="
		allMsg=props_pb2.numenBagAllItem()
		for obj in self.getAllValues():
			itemMsg = allMsg.allItem.add()
			obj.setItemMsg(itemMsg, self, *obj.MSG_FIRST)
		self.endPoint.rpcAll2NumenBag(allMsg)

	def _rpcAddItem(self,obj):
		self.endPoint.rpcAdd2NumenBag(obj.getMsg4Item(self,*obj.MSG_FIRST))

	def _rpcRemoveItem(self,obj):#override
		self.endPoint.rpcDel2NumenBag(obj.id)

	def addStack(self,obj,iAmount):#增加或扣除某个物品的叠加数量
		iBalance=obj.stack()+iAmount
		if iBalance<0:
			raise Exception,'扣除{}扣成负数了,{}个'.format(obj.name,iBalance)
		elif iBalance>obj.maxStack():
			raise Exception,'{}叠加数量超过{}个'.format(obj.name,iBalance)
		obj.setStack(iBalance)
		if iBalance==0:
			self.removeItem(obj)
			#todo 记log跟踪道具流向
		else:
			self.markDirty()
			self.endPoint.rpcMod2NumenBag(obj.getMsg4Item(self,'stack'))


def getNumenBag(iRoleId):
	return numenBagKeeper.getObjFromDB(factory.NO_ROW_INSERT_PRIME_KEY,iRoleId)

import jitKeeper
class cNumenBagKeeper(jitKeeper.cJITproductKeeper):
	pass

import factoryConcrete

if 'numenBagKeeper' not in globals():
	numenBagKeeper=cNumenBagKeeper(factoryConcrete.numenBagFtr)

import mainService
import props
import sql
import props_pb2
import factory
from common import *