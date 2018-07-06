#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import main_scene_pb2
import endPoint
import misc

class cService(main_scene_pb2.scene2main):
	@endPoint.result
	def rpcHelloMain_iAmScene(self,ep,ctrlr,reqMsg):return rpcHelloMain_iAmScene(self,ep,ctrlr,reqMsg)

	@endPoint.result
	def rpcRoleNewXY(self,ep,ctrlr,reqMsg):return rpcRoleNewXY(self,ep,ctrlr,reqMsg)

def rpcRoleNewXY(self,ep,ctrlr,reqMsg):#场景服务发过来的座标
	iRoleId=reqMsg.iEttId
	iX=reqMsg.x
	iY=reqMsg.y
	iSceneId=reqMsg.sceneId
	who=role.gKeeper.getObj(iRoleId)
	if not who:
		return
	if who.sceneId != iSceneId:
		# print "移动包场景ID不一致：{}|{}".format(who.sceneId, iSceneId)
		return
	who.x = iX
	who.y = iY
	
	if who.inTeam() and not who.getTeamObj().isLeader(who.id): # 在队的只有队长才能移动
		return
	
	scene.anlei.triggerWar(who) # 触发暗雷战斗


def rpcHelloMain_iAmScene(self,ep,ctrlr,reqMsg):#	
	print 'rpcHelloMain_iAmScene 被call'
	ep.rpcHelloScene_iAmMain()
	return True


if 'gbOnce' not in globals():
	gbOnce=True
	if 'mainService' in SYS_ARGV:
		pass

from common import *
import c
import timeU
import u
import log
import role
import scene.anlei