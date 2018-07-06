# -*- coding: utf-8 -*-
'''
异兽经验
'''
import props.virtual

class cProps(props.virtual.cProps):

	def use(self, who):
		petObj = who.getLastFightPet()
		if not petObj:
			return
		val = self.getValue()
		petObj.rewardExp(val, self.name)
