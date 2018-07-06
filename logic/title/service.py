# -*- coding: utf-8 -*-
'''
称号服务
'''
import endPoint
import title_pb2


class cService(title_pb2.terminal2main):
	@endPoint.result
	def rpcActiveTitle(self, ep, who, reqMsg):return rpcActiveTitle(who, reqMsg)

	@endPoint.result
	def rpcAcquireTitle(self, ep, who, reqMsg):return rpcAcquireTitle(who, reqMsg)


def rpcActiveTitle(who, reqMsg):
	'''使用称谓
	'''
	iNo = reqMsg.iNo
	if iNo != 0 and not who.titleCtn.getItem(iNo):
		message.tips(who, "你还未获取该称谓")
		return
	if not iNo:
		bRet = who.titleCtn.takeOffTitle(iNo)
	elif iNo == who.titleCtn.iPutOning:
		message.tips(who, "设置称谓成功")
		return
	else:
		bRet = who.titleCtn.putOnTitle(iNo)
	if bRet:
		who.endPoint.rpcTitleUpdate(iNo)
		who.attrChange("title", "titleEffect")
		message.tips(who, "设置称谓成功")

def rpcAcquireTitle(who, reqMsg):
	'''获取称谓
	'''
	iNo = reqMsg.iNo
	oTitle = title.getTitle(iNo)
	if not oTitle:
		message.tips(who, "没有该称谓")
		return
	if not executeScript(who, oTitle.pathLink):
		message.tips(who, "获取称谓失败")

def rpcAddTitle(pid, oTitle):
	'''增加称谓
	'''
	who = getRole(pid)
	if not who:
		return
	msg = title_pb2.titleInfo()
	msg.iNo = oTitle.key
	iExpire = max(-1, oTitle.getExpire())
	if iExpire > 0:
		iExpire += int(getSecond())
	msg.iExpire = iExpire
	who.endPoint.rpcAddTitle(msg)

def rpcRemoveTitle(pid, oTitle):
	'''删除称谓
	'''
	who = getRole(pid)
	if not who:
		return
	who.endPoint.rpcRemoveTitle(oTitle.key)

def rpcTitleList(pid):
	'''角色所有称谓
	required int32 iNo=1;//称号编号
	optional bytes sName=2;//称号名字
	optional int32 iExpire=3; //过期时间(UTC秒数)
	optional bool bIsNew=4; //新获得的红点
	'''
	who = getRole(pid)
	if not who:
		return
	msg = title_pb2.titleList()
	msg.iWearTitle = who.titleCtn.iPutOning
	lTitles = []
	for titleId, oTitle in who.titleCtn.getAllItems():
		titleMsg = title_pb2.titleInfo()
		titleMsg.iNo = titleId
		iExpire = max(-1, oTitle.getExpire())
		if iExpire > 0:
			iExpire += int(getSecond())
		titleMsg.iExpire = iExpire
		lTitles.append(titleMsg)
	msg.titleInfo.extend(lTitles)
	who.endPoint.rpcTitleList(msg)

##称谓获取相关导航处理逻辑 begin##
def executeScript(who, script):
	'''执行脚本
	'''
	for pattern, handler in scriptHandlerList.iteritems():
		m = re.match(pattern, script)
		if not m:
			continue
		args = m.groups()
		handler(who, *args)
		return 1
	return 0

def goAndLookNpc(who, *args):
	'''寻找点击NPC
	'''
	if who.inTeam() and not who.getTeamObj().isLeader(who.id):
		message.tips(who,"组队状态下不能传送")
		return
	npcId = args[0]
	if npcId == "master":
		npcObj = npc.defines.getSchoolMaster(who.school)
		npcId = npcObj.idx
	else:
		npcId = int(npcId)
		npcObj = npc.getNpcByIdx(npcId)
	if not npcObj:
		message.tips(who, "NPC不存在")
		return
	if scene.isNearBy(who, npcObj):
		npcObj.trigger(who.endPoint,who)
		return
	scene.walkToPos(who, npcObj.sceneId, npcObj.x, npcObj.y, u.cFunctor(doLookNpc, npcId))

def doLookNpc(who,npcId):
	'''对话NPC
	'''
	npcObj = npc.getNpcByIdx(npcId)
	if npcObj:
		npcObj.trigger(who.endPoint,who)

def openUI(who, *args):
	'''使用物品
	'''
	msg = title_pb2.uiInfo()
	msg.iUINo = int(args[0])
	who.endPoint.rpcTitleOpenUI(msg)

# 脚本处理函数
scriptHandlerList = {
	"NPC\((\S+)\)":goAndLookNpc,
	"UI\((\S+)\)": openUI,
}
##称谓获取相关导航处理逻辑 end##


import re
from common import *
import message
import scene
import npc
import npc.defines
import u
import title
