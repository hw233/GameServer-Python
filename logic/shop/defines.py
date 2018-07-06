# -*- coding: utf-8 -*-

npcIdx2ShopType = {
	(10203,):1,
	(10204,):2,
	(10201,):3,
	(10216,):4,
}

def getShopTypeByNpcIdx(npcIdx):
	'''根据商店npc获取商品类型
	'''
	for npcIdxList, shopType in npcIdx2ShopType.iteritems():
		if npcIdx in npcIdxList:
			return shopType
	return 0

def getNpcIdxByShopType(shopType):
	'''根据商品类型获取商店npc
	'''
	for npcIdxList, _shopType in npcIdx2ShopType.iteritems():
		if shopType == _shopType:
			return npcIdxList[0]
	return 0

def getNpcByPropsNo(propsNo):
	'''根据物品编号寻找商店npc
	'''
	import npc
	shopType = getShopTypeByPropsNo(propsNo)
	if not shopType:
		return None
	npcIdx = getNpcIdxByShopType(shopType)
	return npc.getNpcByIdx(npcIdx)

def getShopTypeByPropsNo(propsNo):
	'''根据物品编号寻找商品类型
	'''
	data = shopData.hasProps(propsNo)
	if not data:
		return 0
	return data["商品商人"]

import shopData