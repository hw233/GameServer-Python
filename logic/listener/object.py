# -*- coding: utf-8 -*-


class Listener(object):
	'''监听器
	'''
	eventTypeList = [] # 监听的事件类型
	conditionList = () # 触发条件
	conditionScope = "" # 条件范围
	eventList = () # 达成条件后触发的事件
	
	def __init__(self, _id):
		self.id = _id
		
	def checkCondition(self, who, **kwargs):
		'''检查条件
		'''
		if self.conditionScope: # 根据范围检查条件
			return self.checkConditionByScope(who, **kwargs)
		
		for idx, conditionStr in self.conditionList:
			if conditionStr.startswith("$"): # 自定义的条件
				conditionName = conditionStr[1:]
				result = self.checkCustomCondition(who, conditionName, **kwargs)
			else:
				result = listener.defines.checkCondition(who, conditionStr, **kwargs)
			if not result: # 只要有条件不成立，直接返回
				return 0
			
		return 1
	
	def checkConditionByScope(self, who, **kwargs):
		'''根据范围检查条件
		'''
		resultList = {}
		conditionScope = self.conditionScope 
		for idx, conditionStr in self.conditionList:
			if conditionStr.startswith("$"): # 自定义的条件
				conditionName = conditionStr[1:]
				result = self.checkCustomCondition(who, conditionName, **kwargs)
			else:
				result = listener.defines.checkCondition(who, conditionStr, **kwargs)
			resultList[idx] = result
			conditionScope = conditionScope.replace(str(idx), str(result))
		return eval(conditionScope)
	
	def checkCustomCondition(self, who, conditionName, **kwargs):
		'''检查自定义条件
		'''
		return 0
	
	def triggerEvent(self, who, **kwargs):
		'''触发事件
		'''
		kwargs["eventId"] = self.id
		for eventStr in self.eventList:
			if eventStr.startswith("$"): # 自定义的事件
				eventName = eventStr[1:]
				self.triggerCustomEvent(who, eventName, **kwargs)
			else:
				listener.defines.triggerEvent(who, eventStr, **kwargs)
		
	def triggerCustomEvent(self, who, eventName, **kwargs):
		'''触发自定义事件
		'''
		pass


import listener.defines