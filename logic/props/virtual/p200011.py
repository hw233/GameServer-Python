# -*- coding: utf-8 -*-
'''
人物经验
'''
import props.virtual

class cProps(props.virtual.cProps):

	def use(self, who):
		val = self.getValue()
		who.rewardExp(val, self.name)
