# -*- coding: utf-8 -*-
'''
虚拟物品相关
'''
import props.object

class cProps(props.object.cProps):
	'''虚拟物品
	'''
	def onBorn(self,*tArgs,**dArgs):
		props.object.cProps.onBorn(self,*tArgs,**dArgs)
		value = dArgs.get("value", 0)
		if value > 0:
			self.set("value", value)

	def isVirtual(self):#是不是虚拟道具.(虚拟道具指元宝,银币,声望,贡献度等等.进包裹前会解开,变成数值)
		return True

	def setValue(self, iValue):
		'''设置道具附带的值
		'''
		self.set("value", iValue)

	def getValue(self):
		'''获取道具设置的值
		'''
		return self.fetch("value")
