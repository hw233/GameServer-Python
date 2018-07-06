# -*- coding: utf-8 -*-
import props.medicine

class cProps(props.medicine.cProps):
	'''等级药
	'''
	
	def onBorn(self,*tArgs,**dArgs):
		props.medicine.cProps.onBorn(self,*tArgs,**dArgs)
		quality = dArgs.get("quality", 0)
		if quality:
			self.set("quality", quality)

	@property
	def kind(self):
		'''类型
		'''
		return props.defines.ITEM_MEDICINE_LEVEL
	
	def getConfig(self, sKey,uDefault=0):
		return levelmedicineData.getConfig(self.no(), sKey,uDefault)
			
	@property
	def level(self):
		'''等级
		'''
		return self.getConfig("等级")

	def desc(self):
		'''服务器描述
		'''
		sDesc = self.getConfig("服务端描述")
		if not sDesc:
			return ""

		dEffect = self.getEffect()
		if dEffect:
			if "$hp" in sDesc:
				sDesc = sDesc.replace("$hp",str(dEffect["生命"]))
			if "$mp" in sDesc:
				sDesc = sDesc.replace("$mp",str(dEffect["真气"]))

		return sDesc

	def valueInfo(self):
		'''效果信息
		'''
		if self.level!=3:
			return None
		msg = props_pb2.attrMsg()
		msg.name = 25
		msg.sValue = str(self.fetch("quality"))
		return msg
	
	@property
	def quality(self):
		'''品质
		'''
		return self.fetch("quality")

from common import *
import message
import props.defines
import levelmedicineData
import props_pb2