# -*- coding: utf-8 -*-
import props.medicine.levelmedicine

#度厄金丹
class cProps(props.medicine.levelmedicine.cProps):

	def use(self, who):#使用
		message.tips(who,"不能在战斗外使用")
		return False

import message