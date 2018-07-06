# -*- coding: utf-8 -*-

class ApplyMgr(object):
	'''附加效果
	'''
	
	def __init__(self):
		self.applyList = {}
		
	def query(self, name):
		'''获取附加效果(累加)
		'''
		val = 0
		if name in self.applyList:
			for i in self.applyList[name].itervalues():
				val += i
		return val
	
	def has(self, name):
		if name in self.applyList:
			for i in self.applyList[name].itervalues():
				if i:
					return i
		return 0
	
	def queryList(self, name):
		'''获取附加效果列表
		'''
		lst = []
		if name in self.applyList:
			for val in self.applyList[name].itervalues():
				lst.append(val)
		return lst
	
	def add(self, name, val, flag="flag"):
		'''增加效果
		'''
		if name not in self.applyList:
			self.applyList[name] = {}
		self.applyList[name][flag] = self.applyList[name].get(flag, 0) + val
		
	def set(self, name, val, flag="flag"):
		'''设置效果
		'''
		if name not in self.applyList:
			self.applyList[name] = {}
		self.applyList[name][flag] = val
		
	def remove(self, name, flag="flag"):
		'''移除效果
		'''
		if name in self.applyList:
			if flag in self.applyList[name]:
				del self.applyList[name][flag]
				if len(self.applyList[name]) == 0:
					del self.applyList[name]
				
	def removeByFlag(self, flag):
		'''根据标识移除效果
		'''
		nameList = self.applyList.keys()
		for name in nameList:
			if flag in self.applyList[name]:
				del self.applyList[name][flag]
				if len(self.applyList[name]) == 0:
						del self.applyList[name]
						
	def removeByPrefix(self, prefix):
		'''根据标识前缀移除效果
		'''
		nameList = self.applyList.keys()
		for name in nameList:
			flagList = self.applyList[name].keys()
			for flag in flagList:
				if flag.startswith(prefix):
					del self.applyList[name][flag]
					if len(self.applyList[name]) == 0:
						del self.applyList[name]
						
	def clear(self):
		'''清除
		'''
		self.applyList = {}


