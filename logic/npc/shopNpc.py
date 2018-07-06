# -*- coding: utf-8 -*-

import npc.object

class cNpc(npc.object.cNpc):
	def doLook(self, who):
		chat = self.getChat()
		txtList= []
		selList = []
		if chat:
			txtList.append(chat)
		txtList.append("Q购买")
		selList.append(1)
		content = "\n".join(txtList)
		message.selectBoxNew(who, functor(self.responseLook, selList), content, self)
		
	def responseLook(self, who, selectNo, selList):
		if selectNo < 1 or selectNo > len(selList):
			return
		sel = selList[selectNo-1]
		if sel == 1:
			shop.openShop(who, self.idx)


from common import *
import message
import npc
import shop