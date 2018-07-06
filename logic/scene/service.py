#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import scene_pb2
import endPoint

#场景服务
class cService(scene_pb2.terminal2main):
	@endPoint.result
	def rpcEntityTrigger(self,ep, who, reqMsg): return rpcEntityTrigger(self,ep, who, reqMsg)

	@endPoint.result
	def rpcWorldTransfer(self,ep, who, reqMsg): return rpcWorldTransfer(self,ep, who, reqMsg)
	
	@endPoint.result
	def rpcActivateScene(self,ep,who,reqMsg):return rpcActivateScene(self,ep,who,reqMsg)

	@endPoint.result
	def rpcRoleMove(self,ep, who, reqMsg): rpcRoleMove(self,ep, who, reqMsg)	#
	
	@endPoint.result
	def rpcRobotTransfer(self, ep, who, reqMsg): rpcRobotTransfer(self, ep, who, reqMsg)

	@endPoint.result
	def rpcBackSchool(self, ep, who, reqMsg): rpcBackSchool(self, who)

def rpcWorldTransfer(self,ep,who,reqMsg):#用世界地图传送
	iSceneNo=reqMsg.iValue
	oScene = scene.getScene(iSceneNo)
	if not oScene:
		ep.rpcTips('编号{}场景不存在'.format(iSceneNo))
		return
	if who.inWar():
		return
	if who.inTeam() and not who.getTeamObj().isLeader(who.id): # 在队的只有队长才能传送
		return
	if oScene.kind != SCENE_TYPE_REAL:
		writeLog("scene","角色:{}用世界地图传送时上传了一个非实场景id:{}".format(who.id,oScene.id))
		return
	if not scene.tryTransfer(who, oScene.id, None, None):
		return

def rpcRoleMove(self,ep,who,reqMsg):
#	print "rpcRoleMove", "roleId:%d" % who.id, "%d %d,%d,%d" % (who.sceneId, reqMsg.sceneId, reqMsg.x, reqMsg.y)
	oScene = who.sceneObj
	sceneId = reqMsg.sceneId
	x = reqMsg.x
	y = reqMsg.y
	if not oScene or sceneId != oScene.id:
		return
	if who.inTeam() and not who.getTeamObj().isLeader(who.id): # 在队的只有队长才能移动
		return
	iWidth,iHeight = scene.mapdata.gMapWidthHeight.get(oScene.res, (0, 0))
	if x <= 0 or x > iWidth or y <= 0 or y > iHeight:
	#if not scene.validPos(sceneId, x, y):
		sLog = "error {} ({},{}) not in mapDataList[{}]".format(sceneId, x, y, oScene.res)
		log.log("checkMoveValid", sLog)
		# print sLog
		# who.endPoint.rpcTips("客户端移动包非法：({},{})场景{},检查两端地图文件是否对应".format(x, y, oScene.res))
		return
		
	#设置最新的x,y
	#现在还收得到负数的座标,稍后拦掉
	# if reqMsg.x<0 or reqMsg.y<0:
	# 	ep.rpcTips('上传的座标非法')
	# 	return
	# who.x = reqMsg.x
	# who.y = reqMsg.y
	# #转发给周围的其他玩家
	# #print who.id,u.trans('移动了..'),reqMsg.x,reqMsg.y
	# oScene.roleMove(who,reqMsg)
	
	pidList = [who.id]
	if who.inTeam():
		pidList = who.getTeamObj().getInTeamList()
	for pid in pidList:
		obj = getRole(pid)
		if obj:
			obj.x = reqMsg.x
			obj.y = reqMsg.y
		# reqMsg.iEttId = pid
		# if pid != who.id: # 通知队员本人移动
		# 	obj.endPoint.rpcRoleMoveSelf(reqMsg)
		# oScene.roleMove(obj, reqMsg)
	
	scene.anlei.triggerWar(who) # 触发暗雷战斗
	backEnd.gSceneEp4ms.rpcSSRoleMove(reqMsg)

def rpcPos(self,ep,who,reqMsg):#测试用的
	import role_pb2
	msg=role_pb2.roleAttr()
	msg.iRoleId=who.id
	msg.iX=who.x
	msg.iY=who.y
	return msg
	
def rpcEntityTrigger(self,ep, who, reqMsg):
	iEttId = reqMsg.iValue
	oEtt = entity.gEntityProxy.getProxy(iEttId)
	if not oEtt:
		return
	if not scene.isNearBy(who, oEtt, 30):
		message.tips(who, "距离太远了")
		return
	if who.inTeam() and not who.getTeamObj().isLeader(who.id): # 在队的只有队长才能点击实体
		return
	oEtt.trigger(ep, who)

#卡机激活
def rpcActivateScene(self,ep, who, reqMsg):
	oScene = scene.gSceneProxy.getProxy(who.sceneId)
	if not oScene:
		who.rpcTips('脱离卡死失败')
		return	
	scene.switchScene(who.id, oScene.id, *oScene.landingPoint())
	ep.rpcTips('脱离卡死成功')

def rpcRobotTransfer(self, ep, who, reqMsg):
	if not config.IS_INNER_SERVER:
		return
	if not who.isRobot():
		return
	
	sceneId = reqMsg.sceneId
	x = reqMsg.x
	y = reqMsg.y
	scene.tryTransfer(who, sceneId, x, y)
	
def rpcBackSchool(self, who):
	if who.inEscort():
		message.tips(who, "运镖中不能传送")
		return
	elif who.inTreasure():
		message.tips(who, "探宝中不能传送")
		return
	teamObj = who.inTeam()
	if teamObj and not teamObj.isLeader(who.id): # 在队，只有队长才能操作
		message.tips(who, "队伍中无法传送")
		return
	npcObj = npc.defines.getSchoolMaster(who.school)
	if not hasattr(npcObj, "nearByPos"):
		return
	sceneId, x, y = npcObj.nearByPos
	if not scene.tryTransfer(who, sceneId, x, y):
		return

from common import *
from scene.defines import *
import common_pb2
import log
import c
import u
import misc
import role
import mainService
import factoryConcrete
import factory

import scene
import team
import timeU
import entity
import backEnd
import sceneData
import launchMng
import props
import door
import doorData
import block.blockTask
import scene.anlei
import message
import config
import scene.mapdata
import npc.defines