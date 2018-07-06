# -*-coding:utf-8-*-
# 作者:马昭@曹县闫店楼镇
import u
import c
import keeper
import scene_pb2

ETT_TYPE_ROLE = scene_pb2.INFO_ROLE # 玩家
ETT_TYPE_DOOR = scene_pb2.INFO_DOOR # 传送门
ETT_TYPE_NPC = scene_pb2.INFO_NPC # npc

if 'gEntityId' not in globals():
	gEntityId = c.MAX_ROLE_ID  # 从最大的角色id之上递增

def newEntityId():
	global gEntityId
	gEntityId += 1
	return gEntityId

if 'gEntityProxy' not in globals():
	gEntityProxy = u.cKeyMapProxy()

# 实体基类(npc,怪物,传送点,血瓶,地上的道具等等场景上的实体)
class cEntity(object):
	shape = 0
	name = ""
	sceneId = 0
	x = 0
	y = 0
	d = 0 # 面向
	title = ""
		
	def __init__(self, oHolderScene=None):
		self.oHolderScene = weakref.proxy(oHolderScene.this()) if oHolderScene else None
		self.id = newEntityId()
		self.sEnterSerialized = ''
		gEntityProxy.addObj(self, self.id)

	def this(self):
		return self

	def setHolderScene(self, oHolderScene):  # 设置持有我的场景对象
		self.oHolderScene = weakref.proxy(oHolderScene.this())
	
	def getHolderScene(self):  # 获取持有我的场景对象
		return self.oHolderScene

	def ettType(self):
		raise NotImplementedError, '子类要override这个函数'

# 	@property
# 	def id(self):
# 		return self.id

# 	@property
# 	def name(self):
# 		return self.sName
# 	
# 	@name.setter
# 	def name(self, name):
# 		self.sName = name
# 		
# 	@property
# 	def sceneId(self):
# 		return self.iSceneId
# 	
# 	@sceneId.setter
# 	def sceneId(self, sceneId):
# 		self.iSceneId = sceneId

# 	def setSceneId(self,iSceneId):
# 		self.iSceneId=iSceneId

# 	def sceneId(self):#场景id
# 		return self.iSceneId

# 	@property
# 	def sceneNo(self):#场景编号
# 		if not self.iSceneId:
# 			return 0
# 		oScene=scene.gSceneProxy.getProxy(self.iSceneId)
# 		return oScene.id if oScene else 0
		
# 	def setX(self,x):
# 		self.x=x
# 		return self #可以链式调用
# 
# 	def getX(self):
# 		return self.x
# 
# 	def setY(self,y):
# 		self.y=y
# 		return self #可以链式调用
# 
# 	def getY(self):
# 		return self.y
# 
# 	def setZ(self,z):
# 		self.z=z
# 		return self #可以链式调用
# 
# 	def getZ(self):
# 		return self.z
	
# 	@property
# 	def shape(self):
# 		return self.iShape
# 
# 	@shape.setter
# 	def shape(self, shape):
# 		self.iShape = shape

	def trigger(self, ep, who):  # 被触碰了
		pass

	def getEttSerialized(self):	# 获取实体信息序列化后的字节流
		raise NotImplementedError, '请在子类override.'

	def getSerializedGroup(self):  # 获取实体增加包,返回值是可迭代类型,因为可能有多个
		raise NotImplementedError, '请在子类override.'

	def getLeaveMsgSerialized(self):  # 序列化后的离开消息(离开场景时广播给周围的玩家)
		if not getattr(self, 'sLeaveMsgSerialized', None):  # 防止重复序列化
			self.sLeaveMsgSerialized = self._makeLeaveMsgSerialized()
		return self.sLeaveMsgSerialized

	def _makeLeaveMsgSerialized(self):  # 必要时,子类可以override此方法
		oLeaveMsg = scene_pb2.entityLeave()
		oLeaveMsg.iEttId = self.id
# 		oLeaveMsg.iEttType = self.ettType()
		sPacket = endPoint.makePacket('rpcEttLeave', oLeaveMsg)
		return sPacket

	def sendAttrChange(self, *tNeedSend):  # 属性变化，进行广播,tNeedSend是属性名字(成员变量名，或成员函数名)
		if not self.oHolderScene:  # 这个实体都没有放入场景里，属性变化就没有必要广播
			return
		oMsg = self._getAttrChangeMsg()
		for sAttrName in tNeedSend:
			uAttr = getattr(self, sAttrName, None)
			if not uAttr:
				raise Exception, '{}属性不存在'.format(sAttrName)
			if callable(uAttr):  # 是一个成员方法
				uAttr = uAttr()  # call一下，得到value

			sProtoBuffFieldName = self._getFieldNameByAttrName(sAttrName)
			setattr(oMsg, sProtoBuffFieldName, uAttr)
		
		sPacket = endPoint.makePacket('rpcEttAttrChange', oMsg)
		self.oHolderScene.broadcastByXY(self.x, self.y, sPacket)

	def _getAttrChangeMsg(self):  # 返回一个msg
		raise NotImplementedError, '请在子类override'

	def _getFieldNameByAttrName(self, sAttrName):  # 根据属性名返回proto消息定义的域名
		raise NotImplementedError, '请在子类override'


import weakref
import scene
import misc
import endPoint
