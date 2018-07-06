# -*- coding: utf-8 -*-
import keeper

__all__ = ["getWarMgr", ]

if "gWarMgr" not in globals():
	gWarMgr = keeper.cKeeper()
	
def getWarMgr():
	'''战斗管理器
	'''
	global gWarMgr
	return gWarMgr


# 失败选项，可以调整顺序
level2Option = (
	{"option":1, "level":0},  # 录像
	{"option":2, "level":0},  # 宠物
	{"option":3, "level":30},  # 修炼
	{"option":4, "level":45},  # 强化
)


def failBox(who, npcObj):
	pid = who.id
	npcId = npcObj.id
	gevent.spawn(failBox2, pid, npcId)
	
def failBox2(pid, npcId):
	who = getRole(pid)
	npcObj = getNpc(npcId)
	if not who or not npcObj:
		return

	options = []
	for v in level2Option:
		if who.level >= v["level"]:
			options.append(v["option"])

	pid = who.id
	npcId = npcObj.id
	msg = {
		"options":options,
	}
	bFail, resMsg = who.endPoint.rpcWarFailBox(**msg)
	if bFail:
		return
	who = getRole(pid)  # 玩家可能掉线，需要重新获取
	if not who:
		return
	if not getNpc(npcId):
		return
	
	iRes = resMsg.iValue
	if iRes == 1:
		npcObj.lookRecord(who)
	elif iRes == 2:
		pass
	elif iRes == 3:
		pass
	elif iRes == 4:
		pass

		
from common import *
import gevent
import config