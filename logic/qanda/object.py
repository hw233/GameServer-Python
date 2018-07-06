# -*- coding: utf-8 -*-

def _newId(who):
	if not hasattr(who, "responseId"):
		who.responseId = rand(100, 500)
	who.responseId += 1
	return who.responseId

class ResponseHandler(object):
	'''响应处理函数
	'''
	
	def __init__(self, who):
		self.ownerId = who.id
		self.id = _newId(who)
		self.reponseFunc = None # 响应函数
		self.responseCheckFunc = None # 响应检查函数
		
	def setup(self, reponseFunc, responseCheckFunc=None):
		'''设置
		'''
		if type(reponseFunc) == types.MethodType: # 实例方法
			reponseFunc = functor(reponseFunc)
		self.reponseFunc = reponseFunc
		
		if responseCheckFunc:
			if type(responseCheckFunc) == types.MethodType: # 实例方法
				responseCheckFunc = functor(responseCheckFunc)
			self.responseCheckFunc = responseCheckFunc
	
	def handle(self, who, *args):
		'''处理
		'''
		if not self.checkHandle(who, *args):
			return
		reponseFunc = self.reponseFunc
		self.reponseFunc = None
		self.responseCheckFunc = None
		reponseFunc(who, *args)
		
	def checkHandle(self, who, *args):
		if self.responseCheckFunc and not self.responseCheckFunc(who, *args):
			return 0
		return 1
	
	
from common import *
import types
import u