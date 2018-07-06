#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇 mail:guicheng.liao@baoyugame.com

import doorData
import entity
import u

if 'gDoorProxy' not in globals():
	gDoorProxy=u.cKeyMapProxy()

if 'gdDoorModule' not in globals():
	gdDoorModule={}

if 'gdBuffDoor' not in globals():
	gdBuffDoor={}

def getBuffDoor(iNo):
	return gdBuffDoor.get(iNo)

class cDoor(entity.cEntity):#传送门
	def __init__(self,iNo):
		entity.cEntity.__init__(self)
		self.iNo=iNo
		self.sSerialized1=None
		gDoorProxy.addObj(self,self.id)
		self.iState=1

	def ettType(self):#override
		return entity.ETT_TYPE_DOOR

	def setNo(self, iNo):
		self.iNo=iNo
	
	def no(self):
		return self.iNo

	# def scNo(self):
	# 	return self.getConfig('ScNo',0)

	# def getX(self):
	# 	return self.getConfig('x',0)

	# def getY(self):
	# 	return self.getConfig('y',0)

	# def group(self):
	# 	return self.getConfig('group',{}).keys()

	def destScNo(self):
		return self.getConfig('目标场景编号',0)
	
# 	@property
# 	def shape(self):#overide
# 		return self.getConfig('shape', 0)

	def destX(self):
		return self.getConfig('目标x', 0)
	
	def destY(self):
		return self.getConfig('目标y', 0)

# 	@property
# 	def name(self):
# 		return self.getConfig('name','')

	def flip(self):
		return self.getConfig('flip',0)

	def state(self):
		return self.iState

	def type(self):
		raise NotImplementedError,'请在子类实现,返回自己的类型'

	def setState(self,iState):
		self.iState=iState
		self.sSerialized1=None

	def getConfig(self,sKey,uDefault=0):
		return doorData.getConfig(self.no(),sKey,uDefault)

	# def open(self):
	# 	for iRoleId in self.oHolderScene.getEntityIdsByType(entity.ETT_TYPE_ROLE):
	# 		ep=mainService.getEndPointByRoleId(iRoleId)
	# 		if ep:
	# 			ep.rpcClientGateOpen(iId=self.id,iState=1)

	def trigger(self,ep,who):#被触碰了
		print '你碰了个传送门'
		oScene=scene.getScene(self.destScNo())
		if not oScene:
			print '传送门不存在'
			return
		scene.doTransfer(who,oScene.id,self.destX(),self.destY())
		d = self.getConfig("面向", 0)
		if d:
			who.d = d
			who.attrChange('d')
	# def getSerialized1(self):#场景广播包
	# 	if self.sSerialized1 is None:

	# 		ettEnter=scene_pb2.entityEnter()
	# 		ettEnter.iEttId=self.id
	# 		ettEnter.iEttType=self.ettType()
	# 		ettEnter.iX=self.x
	# 		ettEnter.iY=self.y
	# 		ettEnter.iSceneId=self.getHolderScene().id

	# 		doorInfo=scene_pb2.doorInfo()
	# 		doorInfo.iNo = self.no()
	# 		doorInfo.iShape = self.shape
	# 		ettEnter.sSerializedEtt=doorInfo.SerializeToString()


	# 		self.sSerialized1=endPoint.makePacket('rpcEttEnter', ettEnter)
	# 	return self.sSerialized1

	# def getSerializedGroup(self):#override
	# 	return [self.getSerialized1(),]	

	def getEttBaseSerialized(self):#override
		if not self.sEnterSerialized:
			doorInfo=scene_pb2.doorInfo()
			doorInfo.iNo = self.no()
			doorInfo.iShape = self.shape
			self.sEnterSerialized  = doorInfo.SerializeToString()
		return self.sEnterSerialized 


def new(iNo):
	if iNo not in gdDoorModule:
		raise Exception,'编号为{}的door没有关联到gdDoorModule'.format(iNo)
	
	obj=gdDoorModule[iNo].cDoor(iNo)
	return obj

THIS_MODULE=__import__(__name__)


import instance
import scene_pb2

#把永久场景的door安装上去
def init():
	#return #临时屏蔽

	for doorNo, info in doorData.gdData.iteritems():#关联传送门类型
		if doorNo in gdDoorModule:#已经在哪里指定关联过了,不再自动关联
			continue
		gdDoorModule[doorNo] = THIS_MODULE

	for doorNo, info in doorData.gdData.iteritems():
		sceneId = info["场景编号"]
		x = info["传送点x"]
		y = info["传送点y"]
		if not scene.getScene(sceneId):
			continue
		doorObj = new(doorNo)
		doorObj.shape = info["造型"]
		scene.switchSceneForDoor(doorObj, sceneId, x, y)

def isNearByDoor(who):
	for doorObj in gDoorProxy.getAll().itervalues():
		if scene.isNearBy(who, doorObj):
			return True
	return False

import scene
import endPoint
import c
import mainService