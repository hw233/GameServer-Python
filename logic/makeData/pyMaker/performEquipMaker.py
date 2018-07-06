# -*- coding: utf-8 -*-
import makeData.pyMaker.performSchMaker

class PyMaker(makeData.pyMaker.performSchMaker.PyMaker):
	
	def getName(self):
		return "装备法术"

	def getMainModName(self, idx):
		return "perform.equip.pf%s" % self.transIdx(idx)
