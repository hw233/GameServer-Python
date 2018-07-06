# -*- coding: utf-8 -*-
'''传送npc
'''
import npc.object

class cNpc(npc.object.cNpc):
	
	def doLook(self, who):
		content = self.getChat()
		content += '''跳转地图
Q接引
Q离开'''
		message.selectBoxNew(who, self.responseLook, content, self)
		
	def responseLook(self, who, selectNo):
		if selectNo == 1:
			self.doTransfer(who)
			
	def doTransfer(self, who):
		sceneId, x, y, d = self.getConfig("传送")
		if not scene.tryTransfer(who, sceneId, x, y):
			return
		if d:
			who.d = d
			who.attrChange('d')

from common import *
import scene
import message
