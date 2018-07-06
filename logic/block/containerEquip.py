#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import containerGrid

COUNT = 20  #一套方案的格子数

#玩家的装备容器
class cEquipContainer(containerGrid.cGridContainer):

	def __init__(self,iOwnerId):#override
		containerGrid.cGridContainer.__init__(self,iOwnerId,'装备容器')
		self.setIsStm(sql.EQUIP_INSERT)
		self.setDlStm(sql.EQUIP_DELETE)
		self.setUdStm(sql.EQUIP_UPDATE)
		self.setSlStm(sql.EQUIP_SELECT)
		self.iScheme = 1  #当前方案
		
	def _dirtyEventHandler(self):#override
		factoryConcrete.equipCtnFtr.schedule2tail4save(self.ownerId)

	def load(self,dData):#override				
		containerGrid.cGridContainer.load(self,dData)
		self.iScheme = dData.pop("sche",1)

	def save(self):#override
		dData=containerGrid.cGridContainer.save(self)	
		dData["sche"] = self.iScheme	
		return dData
	
	@property
	def endPoint(self):
		return mainService.getEndPointByRoleId(self.ownerId)

	def _rpcAddItem(self,obj):#override
		self.endPoint.rpcAddEquip(obj.getMsg4Item(self,*obj.MSG_ALL))

	# override
	def _rpcRefresh(self):
		#默认实现是逐个下发,性能较差.子类可以override,进行优化处理,比如:全部子项拼成一个网络包下发
		# print "===cEquipContainer======_rpcRefresh====="
		allMsg=props_pb2.equipAllItem()
		allMsg.iCurScheme = self.iScheme
		for obj in self.getAllWearEquip():
			itemMsg = allMsg.allItem.add()
			obj.setItemMsg(itemMsg, self, *obj.MSG_ALL)
		self.endPoint.rpcAllEquip(allMsg)
		
	def setup(self, obj, isLogin=False):
		who = self.getOwnerObj()
		if who and hasattr(obj, "setup"):
			obj.setup(who, isLogin)
		
	def cancelSetup(self, obj):
		who = self.getOwnerObj()
		if who and hasattr(obj, "cancelSetup"):
			obj.cancelSetup(who)

	def callSetup4allItem(self):#对全部成员对象调用setup,在角色实例加载成功后调用.
		for obj in self.getAllWearEquip():
			self.setup(obj, True)

	def _rpcRemoveItem(self,obj):#override
		self.endPoint.rpcDelEquip(obj.id)
		
	def _getPos4AddProps(self,oProps):#override 穿着装备时自动选择目标位置		
		return oProps.wearPos() + (self.iScheme-1)*COUNT

	def getEquipByWearPos(self,iWearPos):#根据穿着位置获取道具
		iPos = iWearPos + (self.iScheme-1)*COUNT
		return self.getPropsByPos(iPos)

	def getAllWearEquip(self):  #获得穿着的装备
		iBegin = (self.iScheme-1)*COUNT+1
		for iPos in xrange(iBegin,iBegin+COUNT):
			oProps = self.dPosMapProps.get(iPos,None)
			if oProps:
				yield oProps
				
	def getAllWearEquipByValid(self):  #获得穿着且生效的装备
		iBegin = (self.iScheme-1)*COUNT+1
		for iPos in xrange(iBegin,iBegin+COUNT):
			oProps = self.dPosMapProps.get(iPos,None)
			if not oProps:
				continue
			if not oProps.isWearValid():
				continue
			yield oProps

	def setScheme(self,iScheme):#设置方案
		self.iScheme = iScheme
		self.markDirty()
		
	def onBorn(self,*tArgs,**dArgs):#override
		self.set('noLogin',1)#标识尚未登录过

import productKeeper
import factoryConcrete

import jitKeeper
import config

#用于查看离线玩家的装备信息.一段时间后不访问,自动从容器上移除
if 'gKeeper' not in globals():
	KEEP_SECOND=30 if config.IS_INNER_SERVER else 60*5
	# gKeeper=productKeeper.cJITproductKeeper(factoryConcrete.equipCtnFtr,KEEP_SECOND)	临时屏蔽,测试jitKeeper
	gKeeper=jitKeeper.cJITproductKeeper(factoryConcrete.equipCtnFtr)

import sql
import misc
import props_pb2
import props
import log
import c
import u
import mainService
import role