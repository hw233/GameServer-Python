# -*- coding: utf-8 -*-
'''阵眼兑换
'''
import npc.object
import ctn
import block

needList = {224301:1, 224302:1, 224303:1, 224304:1, 224305:1, 224306:1, 224307:1, 224308:1, 224309:1, 224310:1}  

class cNpc(npc.object.cNpc):
	#self是NPC1 10216， who是我的角色111
	def doLook(self, who):
		
		chat = self.getChat()
		txtList= []
		selList = []
		if chat:
			txtList.append(chat)
		txtList.append("Q兑换阵眼")
		selList.append(1)
		txtList.append("Q购买玉册")
		selList.append(2)
		content ="\n".join(txtList)
		message.selectBoxNew(who, functor(self.responseLook, selList), content, self)
		
	def responseLook(self, who, selectNo, selList):
		if selectNo < 1 or selectNo > len(selList):
			return
		sel = selList[selectNo-1]
		if sel == 1:
			self.exchangeEye(who)
		elif sel == 2:
			self.buyEyeBook(who)

	def exchangeEye(self, who):
		if who.level < 45:
			message.tips(who, "阵眼于#C0445#n级开启,请在那时兑换")
			return
		propsNoListNeeded = needList.keys()
		propsObjList = list(who.propsCtn.getPropsGroupByNo(*propsNoListNeeded))
		propsObjList = props.tidy.sortList(propsObjList)
		propsIdList = [propsObj.id for propsObj in propsObjList]
		
		if not propsIdList:
			self.say(who, "唔，你身上没有任何记载阵眼的玉册，那你找我何事呢？")
			return

		message.popPropsUI(who, self.responsePopPropsUI, "阵眼兑换选择", propsIdList)
	
	def buyEyeBook(self, who):
		if who.level < 45:
			message.tips(who, "#C0445级#n开启#C02阵眼系统#n")
			return
		shop.openShop(who, self.idx)

	def responsePopPropsUI(self, who, propsList):
		propsNoListNeeded = needList.keys()
		for propsId, amount in propsList.iteritems():
			propsObj = who.propsCtn.getItem(propsId)
			if not propsObj:
				message.tips(who, "你身上没有此物品")
				return
			if propsObj.idx not in propsNoListNeeded:
				message.tips(who, "上交的物品错误")
				return
			if amount < 1 or amount > propsObj.stack():
				message.tips(who, "上交的数量不对")
				return

		for propsId, amount in propsList.iteritems():
			propsObj = who.propsCtn.getItem(propsId)
			who.propsCtn.addStack(propsObj, -amount)
			
			eyeNo = propsObj.getEyeNo()
			eyeObj = lineup.addEye(who, eyeNo)
			message.tips(who,"兑换#C01%s#n成功!" % (eyeObj.name))

from common import *
import message
import props
import props.eyeEffect
import props.tidy
import lineup
import shop