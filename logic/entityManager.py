#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

#实体管理器,不读策划数据表的,抽象类
#控制实体的生成与删除,所生成实体的生命期交给场景管理
#在这里维护记住全部实体Id呢,确保被正确地移除

class cEttMng(object):
	def __init__(self,oHolder):
		self.oHolder=weakref.ref(oHolder)
		self.eEttRemove=u.cEvent()
		self.sEttId=set() #全部的实体id

	def _createEtt(self,*tArgs,**dArgs):
		raise NotImplementedError,'请在子类override'

	def _initMember(self,oEtt,sName,iShape,iSceneId,x,y,*tArgs,**dArgs):#初始化成员变量
		oEtt.name = sName
		oEtt.shape = iShape
		oEtt.sceneId = iSceneId
		oEtt.x = x
		oEtt.y = y

	def _setupEtt(self,oEtt,iSceneId,x,y,*tArgs,**dArgs):#配置信息并注册到场景
		oScene=scene.gSceneProxy.getProxy(iSceneId)
		if not oScene:
			raise Exception,'管理器找不到场景.'
		oScene.addEntity(oEtt,x,y) #交给场景管理
		if not oScene.eEttRemove.contain(self._ettRemoveEventHandler):#要判断是否已加进去了,避免重复添加.
			oScene.eEttRemove+=self._ettRemoveEventHandler
		self._register(oEtt)#在这里只登记一些id,实体生命期还是交给场景管理的
	
	def _register(self,oEtt):#记录到id列表
		self.sEttId.add(oEtt.id)#用怪物id登记管理

	def makeEtt(self,sName,iShape,iSceneId,x,y,*tArgs,**dArgs):#对外接口
		oEtt=self._createEtt(*tArgs,**dArgs)
		self._initMember(oEtt,sName,iShape,iSceneId,x,y,*tArgs,**dArgs)#初始化成员变量
		self._setupEtt(oEtt,iSceneId,x,y,*tArgs,**dArgs)
		return oEtt
	
	def _ettRemoveEventHandler(self,oEtt,oAttacker):#捕捉到场景移除实体事件
		iUid=oEtt.id
		self.sEttId.discard(iUid)
		self.eEttRemove(oEtt,oAttacker)#触发同名的事件

	def getAllEttIdGroup(self):#获取所有实体的id
		return self.sEttId
	
	def removeAllEtt(self):#移除所有实体(可以分别对各个场景实例上调用removeAllEntity)
		for iUid in tuple(self.sEttId):
			oEtt=entity.gEntityProxy.getProxy(iUid)
			if not oEtt:
				continue			
			oHolderScene=oEtt.getHolderScene()
			if oHolderScene:
				oHolderScene.removeEntity(oEtt)
		#不清理id,在eEttRemove事件响应函数中清理

	def removeEtt(self,oEtt):#移除某个实体(可以直接在场景实例上调用removeEntity)
		iUid=oEtt.id
		oEtt=entity.gEntityProxy.getProxy(iUid)
		if not oEtt:
			return
		oScene=oEtt.getHolderScene()
		if oScene:
			oScene.removeEntity(oEtt)
		#不清理id,在eEttRemove事件响应函数中清理

	def getHolder(self):
		return self.oHolder()

#实体管理器,各种信息是从策划数据表中读出来的,抽象类
class cEttMngWithConfig(cEttMng):
	def __init__(self,oHolder):
		cEttMng.__init__(self,oHolder)
		self.dNoMapEtt={} #编号映射实体id

	def makeEttByNo(self,iNo,iSceneId=0,x=0,y=0,*tArgs,**dArgs):#对外接口		
		oEtt=self._createEttByNo(iNo,iSceneId,x,y,*tArgs,**dArgs)
		self._setupEtt(oEtt,oEtt.sceneId,x,y,*tArgs,**dArgs)
		return oEtt

	def _createEttByNo(self,iNo,*tArgs,**dArgs):#通过编号创建实体
		raise NotImplementedError,'请在子类override'

	def _register(self,oEtt):#override
		cEttMng._register(self,oEtt)		
		iNo=oEtt.no()#用怪物编号登记管理
		self.dNoMapEtt.setdefault(iNo,set()).add(oEtt.id)

	def _ettRemoveEventHandler(self,oEtt,oAttacker):#override
		iUid,iNo=oEtt.id,oEtt.no()
		if iNo in self.dNoMapEtt:
			self.dNoMapEtt[iNo].discard(iUid)
		cEttMng._ettRemoveEventHandler(self,oEtt,oAttacker)

	def getEttIdGroupByNo(self,iNo):#用编号获得某类型的全部实体id
		return self.dNoMapEtt.get(iNo,set())

	def removeEttByNo(self,iNo):#根据编号从场景上删除实体
		for iUid in tuple(self.getEttIdGroupByNo(iNo)):
			oEtt=entity.gEntityProxy.getProxy(iUid)
			if not oEtt:
				continue
			oHolderScene=oEtt.getHolderScene()
			if oHolderScene:
				oHolderScene.removeEntity(oEtt)
		#不清理id,在eEttRemove事件响应函数中清理

import npc
import weakref
import copy
import u
import c
import scene
import entity
#import goodsData
#import npcData
#import mstData
#import trapData

