#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import main_scene_pb2
import endPoint
import misc

class cService(main_scene_pb2.main2scene):
	@endPoint.result
	def rpcHotUpdate(self, ep, ctrlr, reqMsg):return rpcHotUpdate(ctrlr,reqMsg)

	@endPoint.result
	def rpcRegisterRole(self,ep,ctrlr,reqMsg):return rpcRegisterRole(ctrlr,reqMsg)

	@endPoint.result
	def rpcUnRegisterRole(self,ep,ctrlr,reqMsg):return rpcUnRegisterRole(ctrlr,reqMsg)
	
	@endPoint.result
	def rpcSSRoleMove(self,ep,ctrlr,reqMsg):return sceneService.service4terminal.rpcSSRoleMove(ctrlr,reqMsg)	

	@endPoint.result
	def rpcSSEntityMove(self,ep,ctrlr,reqMsg):return rpcSSEntityMove(ctrlr,reqMsg)

	@endPoint.result
	def rpcCreateEntity(self,ep,ctrlr,reqMsg):return rpcCreateEntity(ctrlr,reqMsg)

	@endPoint.result
	def rpcDeleteEntity(self,ep,ctrlr,reqMsg):return rpcDeleteEntity(ctrlr,reqMsg)

	@endPoint.result
	def rpcModEntityInfo(self,ep,ctrlr,reqMsg):return rpcModEntityInfo(ctrlr,reqMsg)

	@endPoint.result
	def rpcRemoveEntity(self,ep,ctrlr,reqMsg):return rpcRemoveEntity(ctrlr,reqMsg)

	@endPoint.result
	def rpcRemoveEntityByType(self,ep,ctrlr,reqMsg):return rpcRemoveEntityByType(ctrlr,reqMsg)

	@endPoint.result
	def rpcRemoveAllEntity(self,ep,ctrlr,reqMsg):return rpcRemoveAllEntity(ctrlr,reqMsg)

	@endPoint.result
	def rpcCreateScene(self,ep,ctrlr,reqMsg):return rpcCreateScene(ctrlr,reqMsg)

	@endPoint.result
	def rpcRemoveScene(self,ep,ctrlr,reqMsg):return rpcRemoveScene(ctrlr,reqMsg)

	@endPoint.result
	def rpcBroadcastByXY(self,ep,ctrlr,reqMsg):return rpcBroadcastByXY(ctrlr,reqMsg)

	@endPoint.result
	def rpcBroadcastByEntity(self,ep,ctrlr,reqMsg):return rpcBroadcastByEntity(ctrlr,reqMsg)

	@endPoint.result
	def rpcSwitchScene(self,ep,ctrlr,reqMsg):return rpcSwitchScene(ctrlr,reqMsg)

	@endPoint.result
	def rpcModSSTeamInfo(self, ep, ctrlr, reqMsg):return sceneService.team4ss.rpcModSSTeamInfo(ctrlr,reqMsg)

	@endPoint.result
	def rpcDelSSTeam(self, ep, ctrlr, reqMsg):return sceneService.team4ss.rpcDelSSTeam(ctrlr,reqMsg)

	@endPoint.result
	def rpcSendToClient(self, ep, ctrlr, reqMsg):return rpcSendToClient(ctrlr,reqMsg)

def rpcRegisterRole(ctrlr, reqMsg):
	'''注册角色
	'''
	epId = reqMsg.epId
	roleId = reqMsg.roleId
	ep = sceneService.gEndPointKeeper.getObj(epId)
	if not ep:
		print "rpcRegisterRole被call,没有找到iConnId={}".format(epId)
		return
	# sceneService.sceneServerLog("service4main", "rpcRegisterRole roleId={}".format(roleId))
	ep.setAssociativeRole(roleId)

def rpcUnRegisterRole(ctrlr, reqMsg):
	'''注销角色
	'''
	roleId = reqMsg.iValue
	ep = sceneService.gRoleIdMapEndPoint.getProxy(roleId)
	if not ep:
		# print "rpcUnRegisterRole,没有找到iConnId={}".format(roleId)
		return
	# sceneService.sceneServerLog("service4main", "rpcUnRegisterRole roleId={}".format(roleId))
	ep.resetAssociativeRole()

def rpcCreateScene(ctrlr,reqMsg):
	'''创建场景
	'''
	iScriptSceneId = reqMsg.iSceneId
	iWidth = reqMsg.iWidth
	iHeight = reqMsg.iHeight
	iRes = reqMsg.iRes
	iBroadcastRole = reqMsg.iBroadcastRole
	#iSceneId=reqMsg.iSceneId
	#iMapRes=reqMsg.iMapRes #用于读取可行走区域信息,验证玩家移动包合法性
	if sceneService.scene4ss.getSceneByScriptId(iScriptSceneId):
		raise Exception,'id={}的场景已经存在'.format(iScriptSceneId)
	# sceneService.sceneServerLog("service4main", "rpcCreateScene iScriptSceneId={},iWidth={},iHeight={}".format(iScriptSceneId, iWidth, iHeight))
	sceneService.scene4ss.new(iScriptSceneId, iWidth, iHeight, iRes, iBroadcastRole)
	# return True

def rpcRemoveScene(ctrlr,reqMsg):
	'''删除场景
	'''
	iScriptSceneId = reqMsg.iValue
	oScene = sceneService.scene4ss.getSceneByScriptId(iScriptSceneId)
	if not oScene:#场景不存在
		return
	# sceneService.sceneServerLog("service4main", "rpcRemoveScene iScriptSceneId={},engineSceneId={}".format(iScriptSceneId, oScene.engineSceneId))
	zfmPyEx.deleteScene(oScene.engineSceneId)

def rpcRemoveEntity(ctrlr,reqMsg):
	'''从场景移除实体
	'''
	iScriptSceneId = reqMsg.iSceneId
	iScriptEttId = reqMsg.iEttId
	oScene = sceneService.scene4ss.getSceneByScriptId(iScriptSceneId)
	if not oScene:#场景不存在
		return
	# sceneService.sceneServerLog("service4main", "rpcRemoveEntity iScriptSceneId={},iScriptEttId={}".format(iScriptSceneId, iScriptEttId))
	oScene.removeEntity(iScriptEttId)

def rpcRemoveEntityByType(ctrlr,reqMsg):
	'''移除某个场景的某类型的实体
	'''
	iScriptSceneId = reqMsg.iSceneId
	iEttType = reqMsg.iEttType
	oScene = sceneService.scene4ss.getSceneByScriptId(iScriptSceneId)
	if not oScene:#场景不存在
		return
	# sceneService.sceneServerLog("service4main", "rpcRemoveEntityByType iScriptSceneId={},iEttType={}".format(iScriptSceneId, iEttType))
	oScene.removeEntityByType(iEttType)

def rpcRemoveAllEntity(ctrlr,reqMsg):
	'''移除掉全部场景实体
	'''
	iScriptSceneId = reqMsg.iValue
	oScene = sceneService.scene4ss.getSceneByScriptId(iScriptSceneId)
	if not oScene:#场景不存在
		return
	# sceneService.sceneServerLog("service4main", "rpcRemoveAllEntity iScriptSceneId={}".format(iScriptSceneId))
	oScene.removeAllEntity()

def rpcCreateEntity(ctrlr,reqMsg):
	'''创建实体
	'''
	iScriptEttId=reqMsg.iEttId
	iEttType=reqMsg.iEttType
	sBaseSerialized=reqMsg.sBaseSerialized
	oEntity=sceneService.entity4ss.getEttByScriptId(iScriptEttId)
	if oEntity:#实体已经存在
		return
	# sceneService.sceneServerLog("service4main", "rpcCreateEntity iScriptEttId={},iEttType={}".format(iScriptEttId, iEttType))
	oEntity=sceneService.entity4ss.new(iScriptEttId,iEttType, sBaseSerialized)
	oEntity.setXY(reqMsg.x, reqMsg.y)
	# return True

def rpcDeleteEntity(ctrlr,reqMsg):
	'''删除实体
	'''
	iScriptEttId=reqMsg.iValue
	oEntity=sceneService.entity4ss.getEttByScriptId(iScriptEttId)
	if not oEntity:#实体已经存在
		return
	# sceneService.sceneServerLog("service4main", "rpcDeleteEntity iScriptEttId={},engineEttId={}".format(iScriptEttId, oEntity.engineEttId))
	zfmPyEx.deleteEntity(oEntity.engineEttId)

def rpcSwitchScene(ctrlr,reqMsg):
	'''主服务要求切换场景
	'''
	iScriptEttId = reqMsg.iEttId
	x = reqMsg.x
	y = reqMsg.y
	iScriptSceneId = reqMsg.iSceneId
	# sSwitchSerialized = reqMsg.sSwitchSerialized
	# iSceneIncreaseId = reqMsg.iSceneIncreaseId
	oScene = sceneService.scene4ss.getSceneByScriptId(iScriptSceneId)
	if not oScene:#场景不存在
		return False

	oEntity=sceneService.entity4ss.getEttByScriptId(iScriptEttId)
	if not oEntity:
		return False
	# sceneService.sceneServerLog("service4main", "rpcSwitchScene iScriptEttId={},iScriptSceneId={},x={},y={}".format(iScriptEttId, iScriptSceneId, x, y))
	# oEntity.switchScene(sSwitchSerialized,x,y)
	oScene.addEntity(oEntity,x,y)
	return True

def rpcBroadcastByXY(ctrlr,reqMsg):
	'''以x,y为中心广播一个网络包
	'''
	iScriptSceneId = reqMsg.iSceneId
	oScene = sceneService.scene4ss.getSceneByScriptId(iScriptSceneId)
	if not oScene:#场景不存在
		return
	# sceneService.sceneServerLog("service4main", "rpcBroadcastByXY iScriptEttId={},iScriptSceneId={},x={},y={}".format(reqMsg.iEttId, iScriptSceneId, reqMsg.x, reqMsg.y))
	sPacket = reqMsg.sPacket
	x = reqMsg.x
	y = reqMsg.y
	uIgnoreId = reqMsg.uIgnoreId
	oScene.broadcastByXY(x, y, sPacket, uIgnoreId)

def rpcBroadcastByEntity(ctrlr,reqMsg):
	'''以某实体为中心广播一个网络包
	'''
	pass

def rpcModEntityInfo(ctrlr,reqMsg):
	'''修改实体信息
	'''
	# sceneService.sceneServerLog("service4main", "rpcModEntityInfo iScriptEttId={}".format(iScriptEttId))
	iScriptEttId=reqMsg.iEttId
	sBaseSerialized=reqMsg.sBaseSerialized
	oEntity=sceneService.entity4ss.getEttByScriptId(iScriptEttId)
	if not oEntity:#实体不存在
		return
	oEntity.setBaseSerialized(sBaseSerialized)

	#广播属性改变包
	sPacket = reqMsg.sChangePacket
	uIgnoreId = reqMsg.uIgnoreId
	oScene = sceneService.scene4ss.getSceneByScriptId(oEntity.iSceneId)
	if not oScene:#场景不存在
		return
	oScene.broadcastByXY(oEntity.x, oEntity.y, sPacket, uIgnoreId)

def rpcSSEntityMove(ctrlr, reqMsg):
	'''非角色移动
	'''
	iScriptEttId=reqMsg.iEttId
	x,y = reqMsg.x,reqMsg.y
	iScriptEttId = reqMsg.iEttId
	iSceneId = reqMsg.sceneId
	oEntity = sceneService.entity4ss.getEttByScriptId(iScriptEttId)
	if not oEntity:#实体不存在
		return
	if oEntity.iSceneId != iSceneId:
		return
	oEntity.setXY(x, y)	
	zfmPyEx.modEntityXY(oEntity.engineEttId, x, y)

def rpcHotUpdate(ctrlr, reqMsg):
	import hotUpdate
	modPath = reqMsg.sValue
	hotUpdate.update(modPath)

	log.log("rpcHotUpdate", modPath)

def rpcSendToClient(ctrlr,reqMsg):
	'''通过场景服发包给客户端
		主要用于切换场景后的发包，客户端依赖场景ID处理逻辑
	'''
	roleId=reqMsg.roleId
	sSerialized=reqMsg.sSerialized
	ep = sceneService.gRoleIdMapEndPoint.getProxy(roleId)
	if not ep:
		return
	ep.send(sSerialized)

	

import c
import timeU
import u
import log
import sceneService.scene4ss
import sceneService.entity4ss
import sceneService
import zfmPyEx
import sceneService.team4ss
import sceneService.service4terminal