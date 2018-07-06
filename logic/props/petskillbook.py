#coding:utf-8
'''
异兽技能书
'''
import props.object


class cProps(props.object.cProps):
	@property
	def kind(self):
		'''物品类型
		'''
		return props.defines.ITEM_PET_SKILL_BOOK

	def getPetSkill(self):
		'''获取技能ID
		物品编号的后三位是原技能编号，现在改成四位，第一位为5，后面三位保持不变
		'''
		return self.no() % 234000 + 5000


import props.defines
