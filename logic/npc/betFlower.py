# -*- coding: utf-8 -*-
import npc.object

#天问初试
class cNpc(npc.object.cNpc):

	def doLook(self, who):
		if who.level < 20:
			self.say(who, '少侠等级太低，请升到#C04 20级#n后再来') 
			return

		betFlowerObj = answer.getBetFlowerObj()
		txtList= []
		selList = []

		bBetTime = betFlowerObj.isInBetTime()
		if bBetTime:
			txtList.append('金章之试献花开始了，快来给中意的玩家献花吧')
		else:
			txtList.append('献花可获得积分，积分可兑换道具。周六20：00-21：00可进行献花')

		#直显示，点击弹出兑换界面
		txtList.append('Q兑换道具')
		selList.append(100)

		if bBetTime:
			txtList.append('Q金章之试献花')
			selList.append(101)

		content = "\n".join(txtList)
		message.selectBoxNew(who, functor(self.responseLook, selList), content, self)
		
	def responseLook(self, who, selectNo, selList):
		if selectNo < 1 or selectNo > len(selList):
			return

		sel = selList[selectNo-1]
		if sel == 100:	#兑换道具
			#弹出兑换界面
			shop.openPropsExchange(who, 200010)

		elif sel == 101:
			betFlowerObj = answer.getBetFlowerObj()
			bBetTime = betFlowerObj.isInBetTime()
			if not bBetTime:
				return
			#弹出献花界面
			answer.betFlower.rpcBetFlowerMainReq(who, None)

from common import *
import message
import answer
import answer.betFlower
import shop