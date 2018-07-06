# -*- coding: utf-8 -*-
'''
仙盟贡献
'''
import props.virtual


class cProps(props.virtual.cProps):
	def use(self, who):
		val = self.getValue()
		who.addGuildPoint(val, "虚拟道具")
