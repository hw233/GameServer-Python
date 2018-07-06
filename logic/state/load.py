# -*- coding: utf-8 -*-

if "moduleList" not in globals():
	moduleList  = {}

def getModule(stateId):
	if stateId not in moduleList:
		raise Exception("找不到编号为%s的状态" % stateId)
	return moduleList[stateId]

#状态配置导表开始
import state.st101
import state.st102
import state.st103
import state.st104
import state.st105
import state.st106
import state.st107

moduleList[101] = state.st101
moduleList[102] = state.st102
moduleList[103] = state.st103
moduleList[104] = state.st104
moduleList[105] = state.st105
moduleList[106] = state.st106
moduleList[107] = state.st107
#状态配置导表结束