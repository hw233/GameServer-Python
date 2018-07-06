#-*-coding:utf-8-*-
import props.object

class cProps(props.object.cProps):
	'''药品
	'''

	def use(self, who):#使用
		who.propsCtn.addStack(self,-1)
		dEffect = self.getEffect()
		for sKey,iValue in dEffect.iteritems():
			if sKey == "生命":
				if "生命储备" in dEffect:
					iValue = dEffect["生命储备"]
				who.addReserveHp(int(iValue))
				message.tips(who,"生命储备增加#C02{}#n点".format(iValue))
			elif sKey == "真气":
				if "真气储备" in dEffect:
					iValue = dEffect["真气储备"]
				who.addReserveMp(int(iValue))
				message.tips(who,"真气储备增加#C02{}#n点".format(iValue))

		who.recover(True)
		return True

	def useInWar(self, who, att, vic):#战斗中使用
		if vic.isDead():
			return False
		self.addStackInWar(who,att)
		att.war.rpcWarPerform(att, MAGIC_USE_PROPS, vic, self.no())
		ratio = 100 + self.getEffectRatio(att,vic)
		hp = self.getEffect().get("生命")
		if hp:
			vic.addHP(int(hp)*ratio/100)
		mp = self.getEffect().get("真气")
		if mp:
			vic.addMP(int(mp)*ratio/100)
		return True
		
	def getEffectRatio(self, att, vic):
		'''效果加成
		'''
		return att.queryApplyAll("使用药品加成") + vic.queryApplyAll("受到药品加成")

	def addStackInWar(self, who, att):
		if att.queryApplyAll("药神") and rand(1,100) <= 15:#15%几率不消耗物品
			return
		who.propsCtn.addStack(self,-1)

	@property
	def kind(self):#类型
		return props.defines.ITEM_MEDICINE

from common import *
from war.defines import *
import message
import props.defines