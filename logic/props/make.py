#-*- coding: utf-8 -*-
from props.defines import *
import props.object

class cProps(props.object.cProps):
	'''制造符
	'''

	@property
	def kind(self):
		return ITEM_MAKE
