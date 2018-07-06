#-*-coding:utf-8-*-
#称号容器

import ctn
import block


class cTitleContainer(ctn.cContainerBase,block.cCtnBlock):
	def __init__(self, iOwnerId):
		block.cCtnBlock.__init__(self,'称号容器',iOwnerId)
		ctn.cContainerBase.__init__(self,iOwnerId)
		self.setIsStm(sql.TITLE_INSERT)
		self.setDlStm(sql.TITLE_DELETE)
		self.setUdStm(sql.TITLE_UPDATE)
		self.setSlStm(sql.TITLE_SELECT)

		self.iPutOning = 0

	def _dirtyEventHandler(self):#override
		factoryConcrete.titleCtnFtr.schedule2tail4save(self.ownerId)

	def getTitleName(self):
		if self.iPutOning:
			return self.getItem(self.iPutOning).name
		return ''

	def getTitleEffect(self):
		if self.iPutOning:
			return self.getItem(self.iPutOning).titleEffect
		return 0

	def putOnTitle(self, iNo):
		'''穿上称号
		'''
		obj = self.getItem(iNo)
		if not obj or iNo == self.iPutOning or not obj.isActive():
			return False
		self.iPutOning = iNo
		self.markDirty()
		return True

	def takeOffTitle(self, iNo):
		'''卸掉称号
		'''
		self.iPutOning = 0
		self.markDirty()
		return True

	def save(self):#override
		dData=ctn.cContainerBase.save(self)
		if self.iPutOning:
			dData['putOn'] = self.iPutOning
		return dData

	def load(self,dData):#override
		ctn.cContainerBase.load(self,dData)
		self.iPutOning = dData.pop('putOn', 0)
		if not self.getItem(self.iPutOning):
			self.iPutOning = 0

	def _createAndLoadItem(self,iIndex,uData):#override
		if isinstance(uData,(int,long)):
			iNo,dData=uData,{}
		else:
			iNo,dData=uData
		obj=title.create(iNo)
		obj.load(dData)
		if not obj.isActive():
			del obj
			return None
		return obj

	def _rpcAddItem(self,obj):#override
		title.service.rpcAddTitle(self.ownerId, obj)

	def _rpcRemoveItem(self,obj):#override
		title.service.rpcRemoveTitle(self.ownerId, obj)

	def _rpcRefresh(self):#override
		title.service.rpcTitleList(self.ownerId)

	def setup(self, obj, isLogin=False):#override
		who = self.getOwnerObj()
		if who and hasattr(obj, "setup"):
			obj.setup(who, isLogin)
		
	def cancelSetup(self, obj):#override
		who = self.getOwnerObj()
		if who and hasattr(obj, "cancelSetup"):
			obj.cancelSetup(who)

	def addItem(self,obj):#override
		if not obj.isActive():
			return False
		return ctn.cContainerBase.addItem(self, obj)

	def removeTitle(self, obj, bRepalce=False):
		if self.iPutOning == obj.key:
			self.iPutOning = 0
			who = self.getOwnerObj()
			if who:
				who.endPoint.rpcTitleUpdate(0)
				who.attrChange("title", "titleEffect")
		iKey=obj.key
		if iKey not in self.dKeyMapItem:
			return False
		obj = self.dKeyMapItem.pop(iKey)
		obj.eDirtyEvent-=self._dirtyEventHandler
		self.markDirty()
		if not bRepalce:#同组替换时客户端那边不想收到删除协议
			self._rpcRemoveItem(obj)
		self.cancelSetup(obj)
		return True


import sql
import title.service
import factoryConcrete
