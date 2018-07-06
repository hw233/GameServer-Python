# -*- coding: utf-8 -*-
import makeData.pyMaker.performSchMaker

class PyMaker(makeData.pyMaker.performSchMaker.PyMaker):
	
	def getName(self):
		return "修炼法术"

	def getMainModName(self, idx):
		return "perform.practice.pf%s" % self.transIdx(idx)
