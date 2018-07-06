# -*- coding: utf-8 -*-
'''
门派贡献
'''
import props.virtual


class cProps(props.virtual.cProps):
	def use(self, who):
		val = self.getValue()
		who.addSchoolPoint(val, "虚拟道具")
