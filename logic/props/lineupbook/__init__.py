# -*- coding: utf-8 -*-
from props.defines import *
import props.object

class cProps(props.object.cProps):
	'''阵法书
	'''

	@property
	def kind(self):
		return ITEM_LINEUP_BOOK
	
	def use(self, who):
		#toDo 转到阵法学习界面
		who.endPoint.rpcTips("该功能尚未开放，敬请期待")
		pass