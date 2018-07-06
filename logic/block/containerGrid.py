#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import ctn
import block
import pst

#有格子号的物品容器(装备区,普通包裹,任务包裹)
#抽象类
class cGridContainer(ctn.cContainerBase,block.cCtnBlock):
	def __init__(self,iOwnerId,sChineseName):#override		
		block.cCtnBlock.__init__(self,sChineseName,iOwnerId)
		ctn.cContainerBase.__init__(self,iOwnerId)
		self.dPosMapProps={}#位置映射物品  {pos:obj}
		self.dPropsIdMapPos={}#物品id映射pos  {id:pos}

	def __repr__(self):#override
		l=[]
		for obj in self.getAllValues():
			l.append('<uId={},pos={},no={},name={},id={}>'.format(obj.key,self.getPropsPos(obj),obj.no(),obj.name,obj.id))
		return '\n'.join(l) if l else ctn.cContainerBase.__repr__(self)

	def _createAndLoadItem(self,iIndex,uData):#override
		iNo,iPos,dData=uData
		obj=props.create(iNo)
		obj.load(dData)
		return obj

	def _initItem4container(self,obj,uData=None):#override
		if obj.ownerId!=0:
			raise Exception,'{}拥有者id必须为0'.format(obj.name)	#不为0则可能被重复给予多个玩家	
		if uData is None:#是新增时调用过来的
			iPos=self.getPropsPos(obj)#可以add之前设好pos
			if iPos==0:#尚未指定位置
				iPos=self._getPos4AddProps(obj)
				if 0==iPos:#包裹已满 或 目标装备孔有装备
					return False
		else:
			iPos=uData[1]
		self.dPosMapProps[iPos]=obj
		self.dPropsIdMapPos[obj.id]=iPos
		return ctn.cContainerBase._initItem4container(self,obj,uData)

	def _saveItem(self,iIndex,obj):#override
		return obj.no(),self.getPropsPos(obj),obj.save()
		
	def _getPos4AddProps(self,oProps):#放入道具时选择目标格子号
		raise NotImplementedError,'请在子类override实现'
		
	def removeItem(self,obj):#override
		self.dPosMapProps.pop(self.getPropsPos(obj))
		self.dPropsIdMapPos.pop(obj.id)
		return ctn.cContainerBase.removeItem(self,obj)

	def getPropsByPos(self,iPos):#根据位置获取道具
		return self.dPosMapProps.get(iPos,None)
	
	@property
	def endPoint(self):
		raise NotImplementedError,'请在子类实现'

	def getPropsPos(self,oProps):
		return self.dPropsIdMapPos.get(oProps.id,0)

	def setPropsPos(self,oProps,iPos):
		self.dPropsIdMapPos[oProps.id]=iPos

import misc
import math
import props
import log
import c
import u
import findSort