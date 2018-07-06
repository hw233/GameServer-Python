# -*-coding:utf-8-*-
# 作者:马昭@曹县闫店楼镇
import u
import c
import entity
import keeper

if 'geTriggerNpc' not in globals():
	geTriggerNpc = u.cEvent()

if 'gNPCproxy' not in globals():
	gNPCproxy = u.cKeyMapProxy()

def newByType(iType):
	if iType not in gdNpcModule:
		raise Exception, '类型为{}的npc没有关联到gdNpcModule.'.format(iType)
	obj = gdNpcModule[iType].cNpc()
	return obj

def newByIdx(idx):
	'''根据编号生成固定npc
	'''
	info = npcData.gdData.get(idx)
	if not info:
		raise Exception, "找不到编号为{}的固定npc".format(idx)
	
	iType = info.get('类型', 100)
	npcObj = newByType(iType)
	npcObj.idx = idx
	npcObj.name = info["名字"]
	shape, shapeParts = template.transShapeStr(info["造型"])
	npcObj.shape = shape
	npcObj.shapeParts = shapeParts
	if info.get("染色"):
		colors = template.transColorsStr(info["染色"])
		npcObj.colors = colors
	npcObj.title = info.get("称号", "")
	if info.get("职业"):
		npcObj.school = info["职业"]
	if info.get("动作"):
		npcObj.action = info["动作"]
	if info.get("旁边"):
		npcObj.nearByPos = info["旁边"]	
	return npcObj

def getNpc(_id):
	return gNPCproxy.getProxy(_id)

def getNpcByIdx(npcIdx):
	return gdCacheNpc.get(npcIdx)

if 'gdCacheNpc' not in globals():
	gdCacheNpc = {}

if 'gdNpcModule' not in globals():
	gdNpcModule = {}

import npc.exchange
import npc.makeDataHelper
import npc.fightHelper
import npc.packageHelper
import npc.propsHelper
import npc.master
import npc.demon
import npc.map
import npc.shopNpc
import npc.petTask
import npc.petHelper
import npc.holidayGift
import npc.dyeNpc
import npc.race
import npc.mapExchange
import npc.escort
import npc.transfer
import npc.answerNpc
import npc.treasure
import npc.exchangeHolyPet
import npc.fairyland
import npc.testHelper
import npc.instanceNpc
import npc.ringTask
import npc.betFlower
import npc.exchangeEye


gdNpcModule[10] = npc.fightHelper  # 战斗npc
gdNpcModule[11] = npc.petHelper  # 异兽npc
gdNpcModule[12] = npc.propsHelper  # 物品测试npc
gdNpcModule[13] = npc.testHelper  # 功能测试npc
gdNpcModule[100] = npc.object  # 默认的固定npc
gdNpcModule["导师"] = npc.master  # 默认的固定npc
gdNpcModule["降魔"] = npc.demon   #降魔的固定npc
gdNpcModule["宝图"] = npc.map   #宝图任务的固定npc
gdNpcModule["商店"] = npc.shopNpc	#商店npc
gdNpcModule["染色"] = npc.dyeNpc	#染色npc
gdNpcModule["宠物任务"] = npc.petTask #宠物任务的固定npc
gdNpcModule["节日礼物"] = npc.holidayGift # 节日礼物领取npc
gdNpcModule["竞技场"] = npc.race # 节日礼物领取npc
gdNpcModule["交易"] = npc.exchange # 交易
gdNpcModule["五宝"] = npc.mapExchange # 五宝兑换
gdNpcModule["运镖"] = npc.escort # 运镖
gdNpcModule["传送"] = npc.transfer # 传送NPC
gdNpcModule["每日答题"] = npc.answerNpc # 每日答题
gdNpcModule["探宝"] = npc.treasure
gdNpcModule["兑换神兽"] = npc.exchangeHolyPet # 兑换宠物
gdNpcModule["试炼幻境"] = npc.fairyland # 试炼幻境
gdNpcModule["副本"] = npc.instanceNpc # 竹林除妖
gdNpcModule["任务链"] = npc.ringTask # 入世修行
gdNpcModule["投注献花"] = npc.betFlower # 投注献花
gdNpcModule["兑换阵眼"] = npc.exchangeEye # 兑换阵眼
# 把永久场景的npc安装上去
def init():
	for idx, info in npcData.gdData.iteritems():
		if getNpcByIdx(idx):
			continue
		npcObj = newByIdx(idx)
		gdCacheNpc[idx] = npcObj
				
		sceneId, x, y, d = info["坐标"]
		scene.switchSceneForNpc(npcObj, sceneId, x, y, d)
		
#====================================
#固定NPC所在点不刷出临时NPC
if 'gSceneNpcPosData' not in globals():
	gSceneNpcPosData = {}

def initSceneNpcPos():
	'''固定NPC坐标数据
	'''
	global gSceneNpcPosData
	gSceneNpcPosData = {}
	for _,dData in npcData.gdData.iteritems():
		sceneId,x,y,_ = dData.get("坐标", (0,0,0,0))
		gSceneNpcPosData.setdefault(sceneId, []).append((x, y))

def inSceneNpcAround(sceneId, x, y, distance=3):
	'''判断tPos是否在固定NPC坐标正负3个坐标点内
	'''
	npcPosList = gSceneNpcPosData.get(sceneId, [])
	for xB, yB in npcPosList:
		if pow(x - xB, 2) + pow(y - yB, 2) <= pow(distance, 2):
			return True
	return False
#====================================

import types
import scene
import npcData
import endPoint
import misc
import scene_pb2
import taskData
import block.blockTask
import taskData
import common_pb2
import task_pb2
import event
import task
import launchData
import launchMng
import equipData
import propsData
import config
import template