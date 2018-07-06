# -*- coding: utf-8 -*-
import block
import pst
import jitKeeper
import factory
import centerService.factoryConcrete 
#角色摘要信息,可以离线获取,主要用于好友栏的显示,
#对于有些好友并不在线,但又需要知道一些好友的信息
#好友关系是多对多的,角色简要要信息会被多个玩家引用

class cResume(block.cBlock,pst.cEasyPersist):
	def __init__(self, roleId):#override
		block.cBlock.__init__(self,'角色简要数据',roleId)
		pst.cEasyPersist.__init__(self,self.__dirtyEventHandler)
		
		self.setIsStm(sql4center.RESUME_INSERT)
		self.setDlStm(sql4center.RESUME_DELETE)
		self.setUdStm(sql4center.RESUME_UPDATE)
		self.setSlStm(sql4center.RESUME_SELECT)
		
		self.id = roleId

	def __dirtyEventHandler(self):#数据发生变化了,加入到存盘调度队列
		centerService.factoryConcrete.resumeFtr.schedule2tail4save(self.id)

	def getConnPool(self):#
		return db4center.gConnectionPool

	def update(self, ep, **attrList):
		'''更新
		'''
		for attrName,attrValue in attrList.iteritems():
			if attrName == "roleId":
				continue
			self.set(attrName,attrValue)

		if not self.fetch("zoneName",""):
			self.set("zoneName",ep.sZoneName)


	def getMsg(self):
		msgObj = backEnd_center_pb2.resumeInfo()
		msgObj.roleId = self.id
		msgObj.level = self.fetch("level")
		msgObj.shape = self.fetch("shape")
		msgObj.school = self.fetch("school")
		msgObj.name = self.fetch("name","")
		msgObj.signature = self.fetch("signature","")
		msgObj.serviceName = self.fetch("zoneName","")
		msgObj.offlineTime = self.fetch("offlineTime")
		msgObj.guildName = self.fetch("guildName","")

		return msgObj

class cResumeKeeper(jitKeeper.cJITproductKeeper):
	pass

if 'gKeeper' not in globals():
	if 'centerService' in SYS_ARGV:
		gKeeper=cResumeKeeper(centerService.factoryConcrete.resumeFtr)
	
def getResumeFirst(roleId):
	resumeObj = gKeeper.getObjFromDB(factory.NO_ROW_INSERT_PRIME_KEY, roleId)
	return resumeObj

def getResume(roleId):
	resumeObj = gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE, roleId)
	return resumeObj

from common import *
import sql4center
import db4center
import backEnd_center_pb2
import collect