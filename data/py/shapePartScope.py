# -*- coding: utf-8 -*-
from common import *
from role.defines import *

def getShapePartByRand(shape, shapePartType):
	'''获取造型部位的随机套装
	'''
	shapePartList = gdData.get(shape)
	if not shapePartList:
		return 1
	shapePartName = shapePartDesc[shapePartType]
	scope = shapePartList.get(shapePartName, 0)
	if scope in (0, 1,):
		return scope
	return rand(1, scope)


#导表开始
gdData={
	1111:{"身躯":1,"头发":1,"衣服":1,"武器":1,"影子":1,"帽子":0,"武器特效":0},
	1121:{"身躯":1,"头发":1,"衣服":1,"武器":1,"影子":1,"帽子":0,"武器特效":0},
	1211:{"身躯":1,"头发":1,"衣服":1,"武器":1,"影子":1,"帽子":0,"武器特效":0},
	1221:{"身躯":1,"头发":1,"衣服":1,"武器":1,"影子":1,"帽子":0,"武器特效":0},
	1311:{"身躯":1,"头发":1,"衣服":1,"武器":1,"影子":1,"帽子":0,"武器特效":0},
	1321:{"身躯":1,"头发":1,"衣服":1,"武器":1,"影子":1,"帽子":0,"武器特效":0},
	1411:{"身躯":1,"头发":1,"衣服":1,"武器":1,"影子":1,"帽子":0,"武器特效":0},
	1421:{"身躯":1,"头发":1,"衣服":1,"武器":1,"影子":1,"帽子":0,"武器特效":0},
	1511:{"身躯":1,"头发":1,"衣服":1,"武器":1,"影子":1,"帽子":0,"武器特效":0},
	1521:{"身躯":1,"头发":1,"衣服":1,"武器":1,"影子":1,"帽子":0,"武器特效":0},
	1611:{"身躯":1,"头发":0,"衣服":1,"武器":1,"影子":1,"帽子":0,"武器特效":0},
	1621:{"身躯":1,"头发":1,"衣服":1,"武器":1,"影子":1,"帽子":1,"武器特效":0},
}
#导表结束