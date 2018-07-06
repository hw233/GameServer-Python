# -*- coding: utf-8 -*-
'''
活力
'''
import props.virtual


class cProps(props.virtual.cProps):

	def use(self, who):
		val = self.getValue()
		who.addHuoli(val, "虚拟道具")
