# -*- coding: utf-8 -*-
import props.object

class cProps(props.object.cProps):
	def onBorn(self, *tArgs, **dArgs):
		props.object.cProps.onBorn(self, *tArgs, **dArgs)
		#答题物品，只会在周六获得,周六22:30分就失效
		datePart = getDatePart()
		lEndTime = []
		lEndTime.append(datePart["year"])
		lEndTime.append(datePart["month"])
		lEndTime.append(datePart["day"])
		lEndTime.append(22)
		lEndTime.append(30)
		lEndTime.append(0)
		iEndTime = getSecond(*lEndTime)
		self.set("invalidTime", iEndTime)

	def isInvalid(self):
		return getSecond() > self.fetch("invalidTime", 0)

	def use(self,who):#override
		if self.isInvalid():
			#已过失效时间
			who.propsCtn.removeItem(self)
			return
			
		firstExamObj = answer.getAnswerFirstExamObj()
		firstExamObj.useProps(who, self.idx)


from common import *
import answer
