# -*- coding: utf-8 -*-
'''
阵眼虚拟物品
'''


import props.virtual

class cProps(props.virtual.cProps):
	'''虚拟物品
	'''

	def __init__(self,iNo):
		props.virtual.cProps.__init__(self,iNo)
		self.eyeObj = None

	def setEye(self, eyeObj):
		self.eyeObj = eyeObj

	def use(self, who):
		if not self.eyeObj:
			return
		who.eyeCtn.addItem(self.eyeObj)

	def setStallCD(self , iDayNo):
		if self.eyeObj:
			self.eyeObj.set("stall", iDayNo)

	def save(self):
		dData = props.virtual.cProps.save(self)
		if self.eyeObj:
			dData["eye"] = (self.eyeObj.key,self.eyeObj.save())
		return dData

	def load(self, dData):
		props.virtual.cProps.load(self,dData)
		uData = dData.pop("eye")
		if uData:
			iId,dData = uData
			self.eyeObj = lineup.createEyeAndLoad(iId,dData)

	def setTreasureShopMsg(self, msgObj):
		'''获得摆摊信息
		'''
		msgObj.eye.CopyFrom(lineup.service.packetEyeMsg(self.eyeObj))

import lineup
import lineup.service

