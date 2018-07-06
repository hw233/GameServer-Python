# -*-coding:utf-8-*-
# 作者:马昭@曹县闫店楼镇
import props.object

class cProps(props.object.cProps):
	
	def getEffect(self):
		'''效果
		'''
		if hasattr(self, "effect"):  # 等级会变，所以要删除缓存
			del self.effect
		return props.object.cProps.getEffect(self)

	def use(self, who):  # override
		'''使用
		'''
		if who.day.fetch("experience") >= 10:
			message.tips(who, '每天最多可以使用#C0210个#n经验丹')
			return
		
		exp = self.getEffect()["经验"]
		who.propsCtn.addStack(self, -1)
		who.day.add("experience", 1)
		who.rewardExp(exp, self.name)

import message
