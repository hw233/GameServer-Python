# -*- coding: utf-8 -*-

def init():
	import buff.load

if "gBuffList" not in globals():
	gBuffList = {}
	
def new(bfId):
	'''创建 buff
	'''
	moduleList = buff.load.getModuleList()
	return moduleList[bfId].Buff(bfId)

def get(bfId):
	'''获取buff
	'''
	global gBuffList
	if bfId not in gBuffList:
		bfObj = new(bfId)
		gBuffList[bfId] = bfObj
	return gBuffList[bfId]

def add(vic, bfId, bout, att=None, **args):
	'''增加buff
	'''
	bfObj = get(bfId)
	if not bfObj:
		return None
	if has(vic, bfId):
		return None
	if not _checkAdd(vic, bfObj, att):
		return None
	
	for func in vic.getFuncList("onAddBuff"):
		bout = func(vic, bfObj, bout, att)
	if bout == 0:
		return None
	
	pos = _newOrReplacePos(vic, bfObj)
	typePos = bfObj.getTypePos()

	bfObj = new(bfId)
	bfObj.bout = bout
	bfObj.pos = pos
	bfObj.onNew(vic, att, **args)
	bfObj.setup(vic)
	vic.buffList[typePos][pos] = bfObj
	return bfObj

def _checkAdd(vic, bfObj, att=None):
	if not vic.inWar(): # 已踢出战场
		return 0
	if vic.isLineupEye(): # 阵眼不能加buff
		return 0
	
	warObj = vic.war
	
	# 冲突检查
	# toDo...
	
	if bfObj.getTypePos() != BUFF_TYPEPOS_SPECIAL and vic.hasApply("禁止buff"):
		return 0
# 	if bfObj.isPoison() and vic.hasApply("免疫毒"):
# 		return 0
	
# 	# 抗封处理
# 	if bfObj.type == BUFF_TYPE_SEAL:
# 		if vic.hasApply("抗封"):
# 			warObj.printDebugMsg("\t[%s]抗封成功" % vic.name)
# 			return 0
# 		ratio = vic.queryApplyAll("抗封率")
# 		if ratio:
# 			if rand(100) < ratio:
# 				warObj.printDebugMsg("\t[%s]抗封成功,抗封率%d%%" % (vic.name, ratio))
# 				return 0
# 			else:
# 				warObj.printDebugMsg("\t[%s]抗封失败,抗封率%d%%" % (vic.name, ratio))

	return 1

def _newOrReplacePos(w, bfObj):
	typePos = bfObj.getTypePos()
	buffList = w.buffList[typePos]
	for pos,obj in enumerate(buffList):
		if not obj:
			return pos

	if typePos != BUFF_TYPEPOS_SPECIAL:	# 随机替换
		pos = rand(len(buffList))
		buffList[pos].lost(w)
		buffList[pos] = None
	else:  #　增加
		buffList.append(None)
		pos = len(buffList) - 1
	return pos
	
def addOrReplace(vic, bfId, bout, att=None, **args):
	'''替换buff，如果没有此buff，则增加
	'''
	bfObj = has(vic, bfId)
	if bfObj:
		if not bfObj.replacable: # 不可叠加
			return None
		if not _checkAdd(vic, bfObj, att):
			return None
		bfObj.bout = bout
		vic.war.rpcWarBuff(idx=vic.idx, id=bfObj.id, bout=bfObj.bout)
		return bfObj
	
	return add(vic, bfId, bout, att, **args)

def fork(vic, bfObj, att=None):
	'''复制
	'''
	bfId = bfObj.id
	bout = bfObj.bout
	if has(vic, bfId):
		return None
	
	for func in vic.getFuncList("onAddBuff"):
		bout = func(vic, bfObj, bout, att)
	if bout == 0:
		return None
		
	pos = _newOrReplacePos(vic, bfObj)
	typePos = bfObj.getTypePos()
	bfObj.setup(vic)
	vic.buffList[typePos][pos] = bfObj
	return bfObj

def remove(w, bfId):
	'''移除buff
	'''
	bfObj = get(bfId)
	if not bfObj:
		return
	if not bfObj.removable: # 不可解除
		return
	
	buffList = w.buffList[bfObj.getTypePos()]
	for pos,obj in enumerate(buffList):
		if obj and obj.id == bfId:
			buffList[pos] = None
			obj.lost(w)
			return
		

def has(w, bfId):
	'''是否有同编号buff
	'''
	typePos = get(bfId).getTypePos()
	for bfObj in w.buffList[typePos]:
		if bfObj and bfObj.id == bfId:
			return bfObj
	return None

from common import *
from buff.defines import *
import buff.load
import buff.object
