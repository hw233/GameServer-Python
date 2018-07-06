# -*- coding: utf-8 -*-
import props.lineupbook

class cProps(props.lineupbook.cProps):
	'''阵法残卷
	'''

	def compound(self, who):
		propsAmount = who.propsCtn.getPropsAmountByNos(self.idx)[0]
		if propsAmount < COMBINE_AMOUNT:
			message.tips(who, "阵法残卷不足#C04%d卷#n，无法合成阵法书！" % COMBINE_AMOUNT)
			return
		
		who.propsCtn.subPropsByNo(self.idx, COMBINE_AMOUNT, "阵法书合成")
		propsNo = propsNoList[rand(len(propsNoList))]
		launch.launchBySpecify(who, propsNo, 1, 0, "合成", None)
		message.tips(who, "合成成功，获得#C02{}×1#n".format(props.getPropsName(propsNo)))
		

COMBINE_AMOUNT = 5 # 合成所需数量
propsNoList = (224001,224002,224003,224004,224005,224006,224007,224008,224009,224010,)

from common import *
import message
import launch
