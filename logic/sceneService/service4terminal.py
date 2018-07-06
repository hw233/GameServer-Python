#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import terminal_scene_pb2
import endPoint
import misc

class cService(terminal_scene_pb2.terminal2scene):
	@endPoint.result
	def rpcRoleMove(self,ep,ett,reqMsg):return rpcRoleMove(ett,reqMsg)


def rpcRoleMove(ett, reqMsg):
	'''客户端发过来的移动包
	'''
	roleMove(reqMsg, True)

def rpcSSRoleMove(ctrlr,reqMsg):
	'''主服发过来的移动包
	'''
	roleMove(reqMsg, False)

def roleMove(reqMsg, notifyMain):
	'''处理移动包，notifyMain标示是否把移动包发到主服
	'''
	x,y = reqMsg.x,reqMsg.y
	iScriptEttId = reqMsg.iEttId
	# iSceneIncreaseId=reqMsg.iSceneIncreaseId
	iSceneId = reqMsg.sceneId
	# if x<0 or y<0:
	# 	ep.rpcTips('上传的座标非法')
	# 	return
	# toDo 检查x,y的合法性(目标x,y是否可行走,跟原来的座标相比,是否步子太大)
	# print 'rpcRoleMove,iScriptEttId={},x={},y={},iSceneId={}'.format(iScriptEttId,x,y,iSceneId)
	oRoleEtt=entity4ss.getEttByScriptId(iScriptEttId)
	if not oRoleEtt:
		print '不存在的实体,脚本层实体id=',iScriptEttId
		return
	if not checkMoveValid(oRoleEtt, iSceneId, x, y):
		return

	lTeamScriptEttid = []
	if oRoleEtt.inTeam():
		ssteamObj = oRoleEtt.getTeamObj()
		if not ssteamObj.isLeader(oRoleEtt.scriptEttId):	#不是队长
			return
		lTeamScriptEttid = ssteamObj.getInTeamList()

	oRoleEtt.setXY(x,y)	
	zfmPyEx.modEntityXY(oRoleEtt.engineEttId, x, y)
	if notifyMain:
		backEnd.gMainEp4ss.rpcRoleNewXY(iScriptEttId, x, y, iSceneId)#向主服务发送最新的角色坐标
	for iTeamEttId in lTeamScriptEttid:
		if iTeamEttId == oRoleEtt.scriptEttId:
			continue
		oEtt = entity4ss.getEttByScriptId(iTeamEttId)
		if not oEtt:
			continue
		oEtt.setXY(x,y)
		zfmPyEx.modEntityXY(oEtt.engineEttId, x, y)
		if notifyMain:
			backEnd.gMainEp4ss.rpcRoleNewXY(oEtt.iScriptEttId, x, y, iSceneId)


def checkMoveValid(oRoleEtt, iSceneId, x, y, iSceneIncreaseId=0):
	'''检查x,y的合法性
	'''
	# print "iSceneIncreaseId = ",iSceneIncreaseId,oRoleEtt.sceneIncreaseId
	# if iSceneIncreaseId != oRoleEtt.sceneIncreaseId:
	# 	pass
		# print "移动包切换场景递增ID不一致：{}|{}".format(iSceneIncreaseId, oRoleEtt.sceneIncreaseId)
		# return False
	if oRoleEtt.sceneId != iSceneId:
		# print "移动包场景ID不一致：{}|{}".format(oRoleEtt.sceneId, iSceneId)
		return False
	iSceneId = oRoleEtt.iSceneId
	oScene = sceneService.scene4ss.getSceneByScriptId(iSceneId)
	if not oScene:
		sLog = "error {} not oScene iSceneId={}".format(oRoleEtt.iScriptEttId, iSceneId)
		log.log("checkMoveValid", sLog)
		# print sLog
		return False

	resId = oScene.res
	mapDataList = scene.mapdata.gValidMapDataList
	if resId in mapDataList:
		iWidth,iHeight = scene.mapdata.gMapWidthHeight.get(oScene.res, (0, 0))
		if x <= 0 or x > iWidth or y <= 0 or y > iHeight:
		# if (x, y) not in mapDataList[resId]:
			sLog = "error {} ({},{}) not in mapDataList[{}]".format(oRoleEtt.iScriptEttId, x, y, resId)
			log.log("checkMoveValid", sLog)
			# if config.IS_INNER_SERVER:
			# 	if oRoleEtt.endPoint:
			# 		oRoleEtt.endPoint.rpcTips("客户端移动包非法：({},{})场景{},检查两端地图文件是否对应".format(x, y, resId))
			# print sLog
			return False
	else:
		sLog = "error {} not mapDataList resId={},iSceneId={}".format(oRoleEtt.iScriptEttId, resId, iSceneId)
		log.log("checkMoveValid", sLog)
		# if config.IS_INNER_SERVER:
		# 	if oRoleEtt.endPoint:
		# 		oRoleEtt.endPoint.rpcTips("客户端移动包非法：服务端场景资源{}不存在".format(resId))
		# print sLog
		return False

	if not oScene.isNotifyToC(oRoleEtt):
		return False
	return True

import c
import timeU
import u
import log
import sceneService.scene4ss
import backEnd
import zfmPyEx
import entity4ss
import scene.mapdata
import config
