# -*- coding: utf-8 -*-
from props.defines import *
import props.object

class cProps(props.object.cProps):
	'''重铸石碎片
	'''
	def compound(self, who):
		amountList = who.propsCtn.getPropsAmountByNos(self.idx)
		if sum(amountList) < COMBINE_AMOUNT:
			message.tips(who, "重铸石碎片不足#C04%d个#n，无法合成重铸石！" % COMBINE_AMOUNT)
			return
		if self.stack() >= COMBINE_AMOUNT:
			who.propsCtn.addStack(self, -COMBINE_AMOUNT)
		else:
			amount = self.stack()
			subAmount = COMBINE_AMOUNT - amount
			who.propsCtn.addStack(self, -amount)
			who.propsCtn.subPropsByNo(self.idx, subAmount, "重铸石合成")

		launch.launchBySpecify(who, PropsNo, 1, 0, "合成", None)
		message.tips(who, "合成成功，获得#C02{}×1#n".format(props.getPropsName(PropsNo)))
		
COMBINE_AMOUNT = 5 # 合成所需数量
PropsNo    = 245001

from common import *
import message
import launch