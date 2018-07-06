#-*- coding:UTF-8 -*-
import block
import ctn
import pst

class cBuffContainer(ctn.cContainerBase,block.cCtnBlock):
	def __init__(self,iRoleId):
		ctn.cContainerBase.__init__(self,iRoleId)
		block.cCtnBlock.__init__(self,'Buff数据块',iRoleId)
		self.iOnwerId=iRoleId
		self.setIsStm(sql.BUFF_INSERT)
		self.setDlStm(sql.BUFF_DELETE)
		self.setUdStm(sql.BUFF_UPDATE)
		self.setSlStm(sql.BUFF_SELECT)
		self.timerMng=timer.cTimerMng()#定时器
		self.dTimerIds={}

	def _createAndLoadItem(self,iIndex,uData):#override
		if isinstance(uData,tuple):
			iNo,dData=uData
		else:
			iNo=uData
			dData={}
		return buff.createAndLoad(iNo,dData)	#create task object and return

	def _dirtyEventHandler(self):#override
		factoryConcrete.buffCtnFtr.schedule2tail4save(self.ownerId)
		
	@property
	def endPoint(self):
		import mainService
		return mainService.getEndPointByRoleId(self.ownerId)

	def _rpcAddItem(self,obj):
		return

	def _rpcRefresh(self):
		return

	def _rpcRemoveItem(self,obj):
		return

	def addItem(self,obj):#override
		iNo=obj.key
		if iNo in self.dKeyMapItem:
			self.cancelTimer(iNo)#取消该buff原来的定时器
			self.dKeyMapItem[iNo].resetDuration()#重置buff或者叠加buff时间
			who=role.gKeeper.getObj(self.ownerId)
			if who:
				self.dKeyMapItem[iNo].setup(who)
			return
		for oBuff in self.getAllValues():
			if oBuff.kind()==obj.kind():
				self.cancelTimer(oBuff.key)
				self.removeItem(oBuff)
		return ctn.cContainerBase.addItem(self,obj)

	def startTimer(self,iNo,uFunc,iInterval):
		self.dTimerIds[iNo]=self.timerMng.run(uFunc,iInterval)

	def cancelTimer(self,iNo):
		iTimerId=self.dTimerIds.get(iNo,0)
		if iTimerId:
			self.timerMng.cancel(iTimerId)
			self.dTimerIds.pop(iNo,None)

import factoryConcrete
import sql
import timer
import timeU
import buff
import role