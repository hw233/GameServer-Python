# -*- coding: utf-8 -*-
'''问答模块
'''

def setupResponseHandler(who, responseFunc, responseCheckFunc=None):
	'''设置响应处理函数
	'''
	handler = newResponseHandler(who)
	handler.setup(responseFunc, responseCheckFunc)
	return handler.id

def newResponseHandler(who):
	'''新建响应处理函数
	'''
	if not hasattr(who, "responseHandlerList"):
		who.responseHandlerList = {}
	handler = qanda.object.ResponseHandler(who)
	who.responseHandlerList[handler.id] = handler
	return handler

def popResponseHandler(who, handlerId):
	'''获取并删除回应处理函数
	'''
	if not hasattr(who, "responseHandlerList"):
		return None
	return who.responseHandlerList.pop(handlerId, None)

import qanda.object