# -*- coding: utf-8 -*-

def walk(roleId, ti=-1):
	'''行走AI
	'''
	who = robot.getClientRole(roleId)
	if not who:
		return
	
	sceneId = who.sceneId
	if ti != 0 and rand(100) < rand(10): # 去找传送门
		if not hasattr(who, "lastSceneList"):
			who.lastSceneList = []

		destX, destY = findRandDoor(sceneId, who.lastSceneList)
		if destX and destY: # 找到传送门
# 			who.lastSceneList.append(sceneId) # 暂时不过滤
			if len(who.lastSceneList) > 2:
				del who.lastSceneList[0]
		else:
			destX, destY = scene.randSpace(sceneId)
	else:
		destX, destY = scene.randSpace(sceneId)

	pathList = scene.findPath(sceneId, who.x, who.y, destX, destY)
	if not pathList: # 找不到寻路线路，停止本AI
		who.removeAI("walk")
		return
		
	who.autoPathList = pathList[:-1]
	who.lastWalkStep = 0
	
	if ti == 0:
		autoWalk(roleId)
	else:
		if ti == -1:
			ti = rand(5, 30)
		who.startTimer(functor(autoWalk, roleId), ti, "walk")


def autoWalk(roleId):
	'''自动寻路
	'''
	who = robot.getClientRole(roleId)
	if not who:
		return
	if not who.autoPathList:
		who.removeAI("walk")
		return
	
	sceneId = who.sceneId
	destX, destY = who.autoPathList.pop()
	who.x = destX
	who.y = destY
		
	if (who.lastWalkStep % config.RPC_MOVE_INTERVAL) == 0 or not who.autoPathList or scene.isJump(sceneId, destX, destY):  # 第一步、最后一步和踊跃点一定要发移动包
		robot.sceneSvc.rpcMove(who)
	
	destSceneId, destX, destY = tryTriggerDoor(who)
	if destSceneId:  # 传送门就在旁边
		who.startTimer(functor(transfer, who.id, destSceneId, destX, destY), 2.5, "transfer")
		return
		
	who.lastWalkStep += 1
	who.startTimer(functor(autoWalk, roleId), config.WALK_INTERVAL, "walk")

def findRandDoor(sceneId, excludeSceneList):
	'''随机寻找传送门
	'''
	doorList = []
	for doorId, data in doorData.gdData.items():
		if data["目标场景编号"] in excludeSceneList:
			continue
		if data["场景编号"] != sceneId:
			continue
		doorList.append(doorId)

	if not doorList:
		return None, None
	doorId = doorList[rand(len(doorList))]
	data = doorData.gdData[doorId]
	return data["感应点"]

def tryTriggerDoor(who):
	'''尝试触碰传送门
	'''
	for data in doorData.gdData.values():
		if data["场景编号"] != who.sceneId:
			continue
		x, y = data["感应点"]
		if who.x == x and who.y == y:
			return data["目标场景编号"], data["目标x"], data["目标y"]
	
	return None, None, None

def transfer(roleId, sceneId, x, y):
	'''传送
	'''
	who = robot.getClientRole(roleId)
	if not who:
		return

	robot.sceneSvc.rpcRobotTransfer(who, sceneId, x, y)
	who.startTimer(functor(walk, roleId, 0), 3, "walk")

from common import *
import robot
import scene
import robot.sceneSvc
import config
import doorData
