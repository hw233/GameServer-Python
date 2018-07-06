#-*- coding: utf-8 -*-
from props.defines import *
import props.object

class cProps(props.object.cProps):
	'''玉册效果
	'''
	def getEyeNo(self):
		return self.getConfig("效果")["阵眼"]

	def use(self, who):  # override
		'''使用
		'''
		npcObj = npc.getNpcByIdx(10216)
		if not npcObj:
			return
		scene.walkToEtt(who, npcObj)

import npc
import scene