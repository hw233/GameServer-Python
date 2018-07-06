# -*- coding: utf-8 -*-
'''
地图资源的坐标数据
地图资源：多张地图会使用同一个地图资源，所以坐标数据是相同的
地图全部数据：二维数组
地图有效坐标数据: 字典，(x,y)为key，x和y都从1开始
'''
import codecs
import os

MAP_PATH = "map/" # 地图文件目录
MAP_EXT = ".map" # 地图文件扩展名
JUMP_EXT = ".jump" # 跳跃点文件扩展名
BAN_EXT = ".ban" # 屏蔽坐标文件扩展名

if "gValidMapDataList" not in globals():
	gMapDataList = {} # 地图全部数据
	gValidMapDataList = {} # 地图有效坐标数据
	gJumpDataList = {} # 跳跃点坐标数据,只有部分地图有跳跃点数据
	gRandMapDataList = {} # 可以生成随机坐标的数据
	gBanMapDataList = {} # 需要屏蔽的随机坐标数据
	gMapWidthHeight = {} # 地图的宽高

def loadMapData():
	'''加载地图有效、阻挡和跳跃点数据
	'''
	print "loading map resource data..."
	global gMapDatddaList, gValidMapDataList

	for resId, dataList in readAndTransDataList(MAP_EXT):
		mapData, validMapData = dataList
		gMapDataList[resId] = mapData
		gValidMapDataList[resId] = validMapData
		
		width = len(mapData[0])
		height = len(mapData)
		gMapWidthHeight[resId] = (width, height)

	for resId, jumpData in readAndTransDataList(JUMP_EXT):
		gJumpDataList[resId] = jumpData
		
	for resId, banData in readAndTransDataList(BAN_EXT):
		gBanMapDataList[resId] = banData
		
	for resId, mapData in gValidMapDataList.items():
		gRandMapDataList[resId] = {}
		banList = gBanMapDataList.get(resId)
		for pos, val in mapData.items():
			if banList and pos in banList:
				continue
			gRandMapDataList[resId][pos] = val
			

def readAndTransDataList(fileType):
	'''从文件中读取数据并转换
	'''
	for fileName in os.listdir(MAP_PATH):
		resId, extName = os.path.splitext(fileName)
		if extName != fileType:
			continue

		srcData = readFile(MAP_PATH + fileName)
		func = dataTransHandler.get(fileType)
		if not func:
			raise Exception("未知的文件类型")
		
		data = func(srcData)
		yield int(resId), data


#===============================================================================
# 数据转换处理相关
#===============================================================================
def transMapData(srcData):
	'''转成可用的地图数据
	'''
	mapData = [] # 全部坐标数据
	validMapData = {} # 有效坐标数据
	for y, line in enumerate(srcData):
		lst = line.split(",")
		lst = [int(i) for i in lst]
		mapData.append(lst)
		for x, val in enumerate(lst):
			if val != 0: # 有效坐标
				validMapData[(x+1, y+1)] = val
	return mapData, validMapData

def transJumpData(srcData):
	'''转成可用的跳跃点数据
	'''
	jumpData = {}
	for line in srcData:
		line = line.replace("|", ",")
		lst = line.split(",")
		lst = [int(i) for i in lst]
		jumpData[(lst[0], lst[1])] = (lst[2], lst[3])
	return jumpData

def transBanData(srcData):
	'''转成屏蔽坐标数据
	'''
	banData = {}
	for line in srcData:
		lst = line.split(",")
		lst = [int(i) for i in lst]
		banData[(lst[0], lst[1])] = 1
	return banData

def readFile(mapFile):
	'''读取文件
	'''
	f = open(mapFile)
	for line in f:
		line = line.strip()
		if line[:3] == codecs.BOM_UTF8:
			line = line[3:]
		if line:
			yield line
	f.close()
	
# 数据转换处理	
dataTransHandler = {
	MAP_EXT: transMapData,
	JUMP_EXT: transJumpData,
	BAN_EXT: transBanData,
}



def getJumps(resId, srcX, srcY, destX, destY):
	'''获取两个区域间的跳跃点
	同个区域返回原坐标和目的坐标
	'''
	if resId not in gJumpDataList: # 此场景没有跳跃点
		return (srcX, srcY), (destX, destY)

	jumpData = gJumpDataList[resId]
	validMapData = gValidMapDataList[resId]
	srcAreaId = validMapData[(srcX, srcY)]
	destAreaId = validMapData[(destX, destY)]
	if srcAreaId != destAreaId: # 不同区域，需要找跳跃点
		for srcJump, destJump in jumpData.items():
			if validMapData[srcJump] == srcAreaId and validMapData[destJump] == destAreaId:
				return srcJump, destJump
	else:
		return (srcX, srcY), (destX, destY)
	return None, None

	
#===============================================================================
# 测试相关
#===============================================================================
def printMapData(mapData):
	"""
	打印搜索后的地图
	"""
	for line in mapData:
		print ''.join([str(i) for i in line])
		
#########################################################
def markPath(mapData, lst):
	markSymbol(mapData, lst, "*")
	
def markSearched(mapData, lst):
	markSymbol(mapData, lst, " ")
	
def markSymbol(mapData, lst, symbl):
	for x, y in lst:
		mapData[y][x] = symbl
	
def markSrcDest(mapData, srcX, srcY, destX, destY):
	mapData[srcY][srcX] = "S"
	mapData[destY][destX] = "D"
	
	
if __name__ == "__main__":
	import walkpath
	import common

	MAP_PATH = "../../map/"
	loadMapData()
	
	resId = 1030
	posList = gValidMapDataList[resId].keys()
	srcPos = (15, 82)#posList[common.rand(len(posList))]
	destPos = (98, 31)#posList[common.rand(len(posList))]
	srcX, srcY = srcPos
	destX, destY = destPos
	mapData = gMapDataList[resId]
	print "(%d,%d) to (%d,%d)" % (srcX, srcY, destX, destY)
	
	obj = walkpath.AStar(mapData, srcX-1, srcY-1, destX-1, destY-1)
	obj.findPath()
	searched = obj.getSearched()
	path = obj.path
	print "path length: %d" % (len(path))
	print "searched squares count:%d" % (len(searched))
	
	markSearched(mapData, searched) # 标记已搜索区域
	markPath(mapData, path) # 标记路径
	markSrcDest(mapData, srcX-1, srcY-1, destX-1, destY-1) # 标记开始、结束点
	printMapData(mapData)
