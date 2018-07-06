#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#宠物基类

def new(idx, level, star=1, **args):
	petObj = pet.object.Pet()
	petObj.set("idx", idx)
	data = petData.getConfig(idx)
	petObj.onBorn(data, level, star, **args)
	return petObj

def createAndLoad(data):
	obj = pet.object.Pet()
	obj.load(data)
	obj.reCalcAttr(False)
	return obj
	
def addPet(who, petObj):
	'''增加宠物
	'''
	if not checkAddPet(who, petObj):
		return None
	who.petCtn.addItem(petObj)
	rank.updatePetScoreRank(who, petObj)
	return petObj
	
def checkAddPet(who, petObj, tips=True):
	if who.petCtn.itemCount() >= who.petCtn.itemCountMax():
		if tips:
			message.tips(who, "你身上的异兽已满")
		return 0
# 	if who.level < petObj.getCarryLevel():
# 		if tips:
# 			message.tips(who, "你的等级未达到携带等级")
# 		return 0
	return 1

def getPetName(idx):
	'''获取宠物原始名称
	'''
	data = petData.getConfig(idx)
	if data:
		return data["名称"]
	return "宠物%s" % idx

if 'gdCacheProps' not in globals():
	gdCachePet = {}

def getCachePet(petNo, level=0, *tArgs, **dArgs):  # 有时需要访问信息,生成一个对象放在内存中,避免每次都生成,提高性能
	obj = gdCachePet.get(petNo)
	if level or tArgs or dArgs  or not obj:  # 有特殊参数的要每次都生成
		obj = new(petNo, level, *tArgs, **dArgs)
		if not level and not tArgs and not dArgs:  # 只缓存不带附加参数的对象
			gdCachePet[petNo] = obj
	return obj

from common import *
import pet.object
import u

import timeU
import pet_pb2
import c
import props
import petData
import message
import rank
