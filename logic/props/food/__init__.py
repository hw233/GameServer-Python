# -*- coding: utf-8 -*-
import props.object

class cProps(props.object.cProps):
	'''食品
	'''

	def onBorn(self,*tArgs,**dArgs):
		props.object.cProps.onBorn(self,*tArgs,**dArgs)
		quality = dArgs.get("quality", 0)
		if quality:
			self.set("quality", quality)
		
	@property
	def quality(self):
		'''品质
		'''
		return self.fetch("quality")

	@property
	def kind(self):
		'''类型
		'''
		return props.defines.ITEM_FOOD

	def use(self, who):
		'''使用
		'''
		if not self.canUse():
			message.tips(who,"此物品只能在战斗中使用")
			return False
		dEffect = self.getEffect()
		if "寿命" in dEffect.keys():
			message.tips(who, "请转至异兽培养界面进行使用")
			return False
		who.propsCtn.addStack(self,-1)
		bRecover = False
		for sKey,iValue in dEffect.iteritems():
			if sKey == "生命":
				bRecover = True
				who.addReserveHp(int(iValue))
				message.tips(who,"生命储备增加#C02{}#n点".format(iValue))
			elif sKey == "真气":
				bRecover = True
				who.addReserveMp(int(iValue))
				message.tips(who,"真气储备增加#C02{}#n点".format(iValue))
			elif sKey == "愤怒2":
				who.addSP(int(iValue))
				message.tips(who,"愤怒增加#C02{}#n点".format(iValue))

		who.recover(bRecover)
		return True

	def useInWar(self, who, att, vic):
		'''战斗中使用
		'''
		if not self.canUseInWar():
			return False
		if vic.isDead():
			return False
		who.propsCtn.addStack(self,-1)
		att.war.rpcWarPerform(att, MAGIC_USE_PROPS, vic, self.no())
		sp = self.getEffect().get("愤怒1")
		if sp:
			vic.addSP(int(sp))
		return True

	def canUse(self):
		'''能否使用
		'''
		return self.getConfig("使用1")

	def canUseInWar(self):
		'''能否在战斗中使用
		'''
		return self.getConfig("使用2")

	def desc(self):
		'''服务器描述
		'''
		sDesc = self.getConfig("服务端描述")
		if not sDesc:
			return ""
		# sDesc = "品质:  %d \n%s" % (self.fetch("quality"),sDesc)
		dEffect = self.getEffect()
		if "$hp" in sDesc: 
			sDesc = sDesc.replace("$hp",str(dEffect["生命"]))
		if "$mp" in sDesc:
			sDesc = sDesc.replace("$mp",str(dEffect["真气"]))
		if "$fn" in sDesc:
			sDesc = sDesc.replace("$fn",str(dEffect["符能"]))
		if "$sp1" in sDesc:
			sDesc = sDesc.replace("$sp1",str(dEffect["愤怒1"]))
		if "$sp2" in sDesc:
			sDesc = sDesc.replace("$sp2",str(dEffect["愤怒2"]))
		if "$life" in sDesc:
			sDesc = sDesc.replace("$life",str(dEffect["寿命"]))
		return sDesc

	def valueInfo(self):
		'''效果信息
		'''
		msg = props_pb2.attrMsg()
		msg.name = 25
		msg.sValue = str(self.fetch("quality"))
		return msg

	def getConfig(self,sKey,uDefault=0):
		return foodData.getConfig(self.iNo,sKey,uDefault)

from common import *
from war.defines import *
import message
import foodData
import props_pb2