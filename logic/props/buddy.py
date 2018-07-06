#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

import props.object
class cProps(props.object.cProps):

	@property
	def kind(self):
		'''物品类型
		'''
		return ITEM_BUDDY
		
	def isVisible(self): #是否可视的
		return False

from props.defines import *