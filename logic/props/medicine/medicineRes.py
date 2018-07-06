#-*-coding:utf-8-*-
import props.object

class cProps(props.object.cProps):
	'''储备药品
	'''

	def use(self, who):#使用
		who.propsCtn.addStack(self,-1)
		for sKey,iValue in self.getConfig("效果",{}).iteritems():
			if sKey == "生命":
				who.addReserveHp(int(iValue))
				message.tips(who,"生命储备增加#C02{}#n点".format(iValue))
			elif sKey == "真气":
				who.addReserveMp(int(iValue))
				message.tips(who,"真气储备增加#C02{}#n点".format(iValue))

		who.recover(True)
		oFightPet = who.petCtn.getFighter()
		if oFightPet:
			oFightPet.recover(True)
		return True

	def useInWar(self,who,att, vic):#战斗中使用
		return False

	@property
	def kind(self):#类型
		return props.defines.ITEM_MEDICINE_RES

import message
import props.defines